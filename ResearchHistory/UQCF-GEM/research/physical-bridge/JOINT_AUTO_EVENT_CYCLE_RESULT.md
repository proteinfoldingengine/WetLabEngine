# Joint automatic event-cycle and temporary-incidence bypass theorem

Date: 2026-10-06 (America/Phoenix).
Status: ANALYTICAL RESULT CANDIDATE WITH COMPLETE ARGUMENT.
Scope freeze: JOINT_AUTO_EVENT_CYCLE_SCOPE.md at 19847a5e7e0f75563e4933cd7dda96446687cff0.
Evidence: written mathematics only.

## 1. Carrier

Palette P={x,y,z,w}.

Three labelled roots, all original floors1.

Source:
    r1={x},
    r2={y},
    r3={z}.

Exact target:
    r1*={y},
    r2*={x},
    r3*={z}.

Source and target each consist of three disjoint singleton requirements, so
    tau(source)=tau(target)=3.

Endpoint-differing events are:
    A1 = Add(r1,y),
    D1 = Delete(r1,x),
    A2 = Add(r2,x),
    D2 = Delete(r2,y).

Label w is absent from both endpoints.

The upper condition tau<=4 is trivial throughout any three-root state with nonempty roots; in particular H={x,y,z} covers both endpoints. The obstruction is floor plus lower pair-witness protection.

## 2. Automatic lower edge for Kx={x,z}

At source r2={y} misses Kx, so select r2 as old witness.

At target r1={y} misses Kx, so select r1 as new witness.

New witness r1 begins with x in Kx and target removes it. Automatic lower preparation derives
    D1 -> rho_x.

Old witness r2 begins Kx-free and target gains x. Automatic old-witness hold derives
    rho_x -> A2.

Therefore
    D1 -> rho_x -> A2.

## 3. Automatic lower edge for Ky={y,z}

At source r1={x} misses Ky, so select r1 as old witness.

At target r2={x} misses Ky, so select r2 as new witness.

The automatic rule derives
    D2 -> rho_y -> A1.

Thus
    D2 -> rho_y -> A1.

## 4. Exact floor edges

r1 begins at its floor1. Deleting x before adding y would produce the empty root, violating the original floor.

Therefore endpoint-only floor safety requires
    A1 -> D1.

Similarly
    A2 -> D2.

These are not merely sufficient all-add-before-delete choices; in this singleton-to-singleton replacement they are necessary for any endpoint-only floor-safe execution.

## 5. Combined automatic event cycle

Combining Sections2-4 gives

    A1
      -> D1
      -> rho_x
      -> A2
      -> D2
      -> rho_y
      -> A1.

This is a directed cycle in the joint floor+lower retained event graph.

Hence the automatically selected endpoint certificate admits no topological execution.

Neither constituent channel cycles alone:
- lower edges alone run deletion -> marker -> addition;
- floor edges alone run addition -> deletion.
The obstruction is created by their alternating composition.

## 6. Stronger endpoint-only impossibility

For this carrier, the cycle reflects an actual endpoint-only native deadlock, not just a poor witness selection.

At the source:

### D1 or D2 first

Either deletion empties a singleton root and violates floor1.

### A1 first

State becomes
    {x,y}, {y}, {z}.

Pair {y,z} hits all three roots, so tau=2. The protected lower bound fails.

### A2 first

State becomes
    {x}, {x,y}, {z}.

Pair {x,z} hits all three roots, so tau=2.

Thus NONE of the four endpoint-differing native events is legal from the source.

Therefore no endpoint-only native path can leave the source while preserving floor1 and tau>=3.

This is stronger than selected-certificate cyclicity, but it is scoped only to endpoint-only events in this carrier.

## 7. Temporary-incidence native bypass

Allow the off-endpoint label w temporarily.

Execute:

1. Add(r1,w):
       {x,w}, {y}, {z}.

2. Delete(r1,x):
       {w}, {y}, {z}.

3. Add(r2,x):
       {w}, {x,y}, {z}.

4. Delete(r2,y):
       {w}, {x}, {z}.

5. Add(r1,y):
       {w,y}, {x}, {z}.

6. Delete(r1,w):
       {y}, {x}, {z}.

The final state is exactly the target.

## 8. Exact hitting numbers along the bypass

Every displayed state has tau=3.

Step1:
roots {x,w},{y},{z}. Singleton y,z force y,z and a third label x or w is required for r1. Three labels suffice.

Step2:
{w},{y},{z} are disjoint singleton requirements. tau=3.

Step3:
{w},{x,y},{z}. w,z are forced and one of x,y is required. tau=3.

Step4:
{w},{x},{z} are disjoint singleton requirements. tau=3.

Step5:
{w,y},{x},{z}. x,z are forced and one of w,y is required. tau=3.

Step6:
{y},{x},{z} are disjoint singleton requirements. tau=3.

No state can have tau<3 by the forced-label arguments, and the exhibited triples are covers.

All roots remain nonempty, so every floor1 constraint holds.

Thus the temporary-incidence path is a protected native bypass.

## 9. What w actually supplies

The temporary label does two jobs in sequence.

First, Add(r1,w) gives r1 one unit of capacity so x can be deleted without emptying the root.

After deleting x, r1={w} becomes a new witness for every pair not containing w, including the pair constraints that would have been destroyed by directly adding y.

That frees r2 to acquire x and then lose y.

Finally r1 can acquire its target y and discard w.

So w provides:
- temporary root-capacity slack;
- a temporary witness identity outside the endpoint pair structure.

It breaks the alternating cycle without changing the exact endpoint.

This is a mathematical auxiliary-incidence mechanism, not a physical particle or field.

## 10. Relation to earlier cycle results

The earlier macro-cycle carrier was endpoint-only connected but required partial macro interleaving.

The present carrier is stronger in a different direction:
- endpoint-only native repair is impossible from the source;
- one temporary off-endpoint incidence family restores connectivity.

Thus there are now two distinct cycle-breaking mechanisms:

    coarse macro cycle
        -> expose endpoint event interleaving;

    joint endpoint-event cycle
        -> enlarge the admissible event alphabet temporarily.

These should not be conflated.

## 11. Next frontier

The next theorem should characterize auxiliary cycle breaking without hard-coding label w.

A natural target is:

Given an alternating directed cycle produced by
    floor/capacity edges
and
    lower-witness transfer edges,

derive sufficient conditions for one temporary auxiliary incidence to break the cycle, preserve tau>=3 and floors, and be removed at the exact destination.

Questions:
1. When is one auxiliary label enough?
2. Can one auxiliary incidence break several coupled cycles?
3. What retained information is required to choose its host root?
4. Can the auxiliary be eliminated from the final theorem by interpreting it as temporary retained capacity rather than a new primitive?

No physical force, geometry, energy, observer field or fundamental time is inferred.
