"""Read the baseline without writing, veto the final release, or substitute verified moves."""
import inspect
import sys
from functools import cache
from historical import local, move


@cache
def commit_line(function):
    lines, first = inspect.getsourcelines(function)
    positions = [first + i for i, line in enumerate(lines)
                 if line == "            path.append(current[:])\n"]
    result, = positions
    return result


def continuing(lib, tree, q, start, site, replacement):
    """None is passive profiling. An empty tuple vetoes. Otherwise use the specified successors."""
    p = lib.p
    record = {"calls": [], "guards": []}
    prior_trace, prior_profile = sys.gettrace(), sys.getprofile()
    def watch(frame, event, arg):
        f = frame.f_locals
        if event == "call" and frame.f_code is p.require_exact_parent.__code__:
            parent = frame.f_back
            if parent.f_code.co_name == "child_call" and parent.f_back.f_locals["t"] == tree:
                record["guards"].append([parent.f_locals["c"], p.coordinate(f["state"], f["nodes"][0]), f["q"]])
        if event == "call" and frame.f_code is p.normalize.__code__:
            parent = frame.f_back
            if parent.f_code.co_name == "child_call" and parent.f_back.f_locals["t"] == tree:
                record["calls"].append([parent.f_locals["c"], list(parent.f_locals["labels"]), list(f["state"])])

    def observe_commit(frame, event, arg):
        if event != "line" or frame.f_lineno != commit_line(p.lift_root_path):
            return observe_commit
        f = frame.f_locals
        if f["step"] is not f["root_path"][-1] or f["child"] != site or f["add"]:
            return observe_commit
        before, after = tuple(f["path"][-1]), tuple(f["current"])
        donor, _, _ = move(before, after)
        assert lib.verify_cut(tree, before, donor, site)[0] == after
        assert "source" not in record
        record["source"] = [before, after, donor]
        if replacement is not None:
            wanted = replacement[-1] if replacement else before
            f["current"][:] = wanted
        return observe_commit

    def global_trace(frame, event, arg):
        if event == "call" and frame.f_code is p.lift_root_path.__code__ and frame.f_locals["tree"] == tree:
            return observe_commit
        return None

    if replacement is not None:
        sys.settrace(global_trace)
    sys.setprofile(watch)
    try:
        try:
            result = p.normalize(list(start), tree, len(start), list(q))
            record["outcome"] = "returned"
        except p.ConstructionFailure as error:
            result = error.path
            record["outcome"] = str(error.original)
    finally:
        sys.setprofile(prior_profile)
        sys.settrace(prior_trace)
    return tuple(map(tuple, result)), record


def shortest_repairs(lib, tree, q, before, donor, site):
    all_moves = lib.moves(tree, before)
    only = [(action, st) for action, st in all_moves.items() if lib.profile(tree, st) == q]
    assert len(only) == 1 and only[0][0] == (donor, site, -1)
    assert [op for op in all_moves if op[2] < 0] == [(donor, site, -1)]
    out = []
    for op1, s1 in all_moves.items():
        if not s1[donor] & (1<<site):
            continue
        for op2, s2 in lib.moves(tree, s1).items():
            if s2[donor] & (1<<site) and lib.profile(tree, s2) == q:
                out.append((op1,op2,s1,s2))
    singletons = [c for c in lib.p.layout(tree)[0] if not lib.p.layout(tree)[c]]
    expected = {((r,t,1),(donor,t,-1)) for r in range(len(before)) if r!=donor for t in singletons}
    assert {(a,b) for a,b,_,_ in out} == expected and len(out)==4
    return out


def controls(lib, tree, q, start, site, positive, index, donor, receiver):
    observed, base = continuing(lib, tree, q, start, site, None)
    assert observed == positive and base["outcome"] == "returned"
    before, after = positive[index-1:index+1]
    veto, removed = continuing(lib, tree, q, start, site, ())
    assert removed["source"] == [before,after,donor]
    assert removed["outcome"] == "recursive call requires exact parent"
    assert removed["guards"][-1][1:] == [1,2]
    assert len(removed["calls"]) == 4 and len(base["calls"]) == 8
    assert len(removed["guards"]) == 5 and len(base["guards"]) == 8
    assert veto[:index] == positive[:index] and veto[index:] == (before,)
    actual = local(positive[index:], receiver)
    tests = []
    for op1,op2,s1,s2 in shortest_repairs(lib,tree,q,before,donor,site):
        trial, watched = continuing(lib,tree,q,start,site,(s1,s2))
        assert watched["source"] == [before,after,donor] and watched["outcome"]=="returned"
        assert trial[:index]==positive[:index] and trial[index]==s2
        assert len(watched["calls"])==8 and all(t[1]==t[2] for t in watched["guards"])
        # The historical logger sees the new state at its recording instruction. Insert the separate first atom.
        reconstructed = trial[:index] + (s1,) + trial[index:]
        # One additional original call closes the alternative to the SAME endpoint, after all observations.
        extension = lib.normalize(tree,q,reconstructed[-1])
        lib.check_path(tree,q,reconstructed+extension[1:])
        assert reconstructed[-1]!=lib.endpoint(tree, len(start), q)
        cpath = local(trial[index:],receiver)
        clean = op1[0] != receiver
        if clean:
            assert s1[receiver] == s2[receiver] == before[receiver] == after[receiver]
        alt_after, alt_receipt = lib.verify_cut(tree, s1, donor, op2[1])
        assert alt_after == s2 and alt_receipt == (1, 2, 0, True)
        tests.append({"actions":[op1,op2], "cut_fields":alt_receipt,"clean_prior":clean,"source_kept":bool(s2[donor] & (1<<site)),
                      "second_input":watched["calls"][-1],"state_before_read":s2,"after_read":trial[index:],
                      "complete_at_first_return":False,"closing_moves":len(extension)-1,"receiver":cpath})
    return {"live_receiver":actual,"base_calls":base["calls"],"base_guards":base["guards"],
            "veto_guard":removed["guards"][-1],"veto_outcome":removed["outcome"],"bypasses":tests}
