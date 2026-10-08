# C3 observation-fiber theorem — notation clarification

Date: 2026-10-08.
Status: REPORTING ADDENDUM following independent mathematical ACCEPTED review abc3eacd359d4bfabb0d595dbe5ea6835943e910.

To avoid identifying commitment provenance with post-state support, let Y(x,a) be a finite set of OUTCOME RECORDS. Define an explicit post-state projection
    pi:Y(x,a)->X_adm.
The observation O:Y->R may factor through pi, e.g. O=O_state composed with pi, while the commitment predicate c:Y->{0,1} is defined on the outcome record. Thus pi(y)=pi(y') need not imply c(y)=c(y'). All factorization, fiber, and minimal-partition statements in the frozen proof use Y as this outcome-record domain. In the C3 two-outcome example, the post-states happen to differ, but the more general statement allows equal post-states with different provenance.

This clarification changes no accepted theorem or mathematical scope and supplies no physical observer or measurement mechanism.
