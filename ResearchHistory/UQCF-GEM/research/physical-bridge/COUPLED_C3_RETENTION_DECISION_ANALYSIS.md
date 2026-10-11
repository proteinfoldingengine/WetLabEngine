# Retention decision from declared lineage observables

Date: 2026-10-11. Inspected parent: 58cffdf4fb9ab45c800f8106f5c6f3f062a18fb2.
Status: analytical working result, not a certified scientific campaign or physical pruning law. The deductions below were obtained before any numerical campaign; none has been launched.

## Question and declared domain

Does recoverability alone choose which lineage vertices survive?

Use the inherited finite rooted prefix tree X. A retained set Y is nonempty, prefix closed, contains the root, and is a subset of X. Its canonical retraction r_Y maps each vertex to its longest retained prefix. This r_Y is already derived once Y is given.

Supply a finite family of vertex observables f_j:X->A_j, with arbitrary codomains having equality, and write F(v)=(f_j(v))_j. The preservation contract here is exactly

    F(v)=F(r_Y(v)) for every v in X.

Equivalently each observable descends along r_Y; evaluating at retained vertices forces the descended observable to equal its restriction. The empty observable family is allowed and has constant empty signature.

This is a contract on individual lineage vertices. It is NOT preservation of arbitrary extensive source arrays, complete quantum instruments, a native accessible C3 record, or a physical observer. It does not identify those distinct constructions. F and the preservation requirement are declared inputs, not acquired information or a new physical primitive adopted here.

## Exact classification

For each nonroot vertex v let p(v) be its parent. Define the required-change vertices

    D_F={v != root : F(v) != F(p(v))}.

Let Y_min be the prefix closure of {root} union D_F. Then the complete sufficient-retention family is

    {Y : Y is prefix closed and Y_min subseteq Y subseteq X}.

In particular a unique least sufficient retained set exists for this declared contract.

### Necessity

If v is not retained, prefix closure implies r_Y(v)=r_Y(p(v)). Preservation at v and its parent then implies F(v)=F(p(v)). Consequently every v in D_F must be retained. Prefix closure forces all its ancestors to be retained as well, so Y_min subseteq Y.

### Sufficiency

Suppose Y contains Y_min. Along the path from r_Y(v) to v, every vertex after r_Y(v) is unretained. None belongs to D_F, because D_F subseteq Y. Its signature therefore equals its parent's signature. Chaining these equalities gives F(v)=F(r_Y(v)). Thus all declared observables are preserved.

No cardinality optimization, metric, probability, or elapsed-time parameter is needed for this classification. It follows from prefix retention and equality of the specified observables.

## What this does and does not select

The classification derives a LEAST sufficient object. It does not assert that the system actually chooses it. X itself always satisfies preservation. Therefore:

1. If Y_min=X, the only sufficient retained set is X: this contract forbids any vertex deletion.
2. If Y_min is a proper subset of X, at least Y_min and X are sufficient: preservation alone does not choose a unique retained set.

Thus these preservation requirements alone never uniquely force a nontrivial pruning. Imposing 'always choose the least sufficient set' would add a selection principle. We do not adopt it as physical dynamics, even though its mathematical output is well defined. Nor do we assume that pruning must happen, or add a maximal-deletion objective.

The constant-signature case gives Y_min={root}; it permits maximal pruning but does not demand it. If F distinguishes every parent-child pair, Y_min=X. Distinguishing every vertex identity is a sufficient special case of that condition. Conversely, some equal-signature edges may still have to survive because they lie above a later required-change vertex: equality on an edge alone does not justify removing its parent or child while retaining descendants.

## Explicit branching example

Let X={root,a,b,c}, with parent(a)=root, parent(b)=a, parent(c)=root, and F(root)=0, F(a)=F(b)=1, F(c)=0. Then D_F={a}, Y_min={root,a}, and exactly four retained subsets satisfy this contract:

    {root,a}, {root,a,b}, {root,a,c}, {root,a,b,c}.

On the least set, b retracts to a and c retracts to root, preserving F. The other three also preserve F. This example is a direct analytical illustration, not an executed enumeration or a new empirical result.

## Connection to the inspected event-retention source

The v15.22 source gives a related but differently typed boundary. For a supplied sharp next-event instrument it constructs a most-forgetful sufficient conditional expectation E_e; identity is also sufficient. Under its particular open two-event, all-input, full-branch-output contract, only identity is sufficient. It explicitly derives neither the next event nor an actual outcome. The lineage result above uses no quantum carrier or imported quantum theorem and does not establish a cross-domain identification.

The physical lesson is limited but precise: knowing which distinctions a contract requires can determine what must survive; this does not by itself cause a deletion or choose an actual record. For the present lineage contract the complete choice set is now explicit. The remaining upstream inputs are the physically justified observable/obligation family and an inherited actual-update mechanism. Neither is derived by replacing 'sufficient' with 'minimal'.

## Research decision

Do not launch a numerical physics campaign around choosing Y_min. That would test a supplied minimum-retention policy, not derive it. Preserve this analytical classification and its review as a bounded answer to the approved retention-selection investigation. It is not a new numbered stage, a certified no-go for all retention mechanisms, or a physical closure claim. No scientific-test total changes. Native record production/access, enforcement, actual selection, progress and broad C3/C4-C6 remain OPEN.

## Immutable source anchors

- [Canonical prefix retraction](https://github.com/proteinfoldingengine/WetLabEngine/blob/58cffdf4fb9ab45c800f8106f5c6f3f062a18fb2/ResearchHistory/UQCF-GEM/demos/v15.56-response-selector-obstruction/pruning_morphism.py).
- [Event-specific retention argument and limits](https://github.com/proteinfoldingengine/WetLabEngine/blob/58cffdf4fb9ab45c800f8106f5c6f3f062a18fb2/ResearchHistory/UQCF-GEM/demos/v15.22-event-sufficient-retention/README.md).
- [Event-specific implementation](https://github.com/proteinfoldingengine/WetLabEngine/blob/58cffdf4fb9ab45c800f8106f5c6f3f062a18fb2/ResearchHistory/UQCF-GEM/demos/v15.22-event-sufficient-retention/event_sufficiency.py): effects and retention depend on the supplied instrument; actual_record_selected remains None.
- [Partial pruning implementation](https://github.com/proteinfoldingengine/WetLabEngine/blob/58cffdf4fb9ab45c800f8106f5c6f3f062a18fb2/ResearchHistory/UQCF-GEM/demos/v15.16-partial-pruning/recoverability.py): the record mask and encoding are supplied inputs.
