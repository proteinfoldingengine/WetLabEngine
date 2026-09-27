# v15.90 — arbitrary inputs and the limit of the Choi ceiling

Parent: 44ca8cf73e39ef1e66fda684ddabdf0ce6a1d5bf. The v15.89 theorem concerns a normalized Choi state, equivalently a maximally entangled input. This bounded extension asks what survives for arbitrary reference/input states. It uses no optimizer, empirical fit, or physical source-law selection.

## Universal arbitrary-input bound

Let Phi be a qubit CPTP channel, with affine Bloch matrix T and delta=s_min(T). v15.89 proves the operator inequality J^Gamma >= -delta I for the unnormalized input-first Choi matrix J (trace 2). For a normalized pure two-qubit input, write

    |psi>=(A tensor I)|Omega>,  |Omega>=(|00>+|11>)/sqrt(2),
    Tr(A^dagger A)=2.

If rho_out=(id tensor Phi)(|psi><psi|), then

    rho_out^Gamma=(A* tensor I)(J^Gamma/2)(A^T tensor I)
                 >= -(delta/2)(A* A^T tensor I).

Consequently lambda_min(rho_out^Gamma)>=-delta lambda_max(rho_reference). A two-qubit partial transpose has at most one negative eigenvalue, so

    N(rho_out) <= delta lambda_max(rho_reference) <= delta.

Here N=sum max(0,-lambda_i(rho^Gamma)) for a normalized density matrix. Do not divide its negativity by 2 again. The factor 1/2 in v15.89 came solely from unnormalized J.

Every pure state of an arbitrary finite-dimensional reference and a qubit has Schmidt rank at most two. A reference isometry reduces its output to the above case without changing nonzero PT eigenvalues. Convexity of negativity then extends the uniform bound to every mixed input/reference state. Also N<=1/2 for any state with a qubit subsystem, by Schmidt decomposition and convexity. Thus

    N((id_R tensor Phi)(rho_RQ)) <= min(delta,1/2).

The pure-state, Schmidt-dependent bound can be tighter. It recovers delta/2 for maximally entangled inputs. This argument does not claim that the uniform bound is the exact maximum for each fixed delta.

## Explicit failure of extending delta/2 to all inputs

Take amplitude damping with q in [0,1], gamma=1-q, T=diag(sqrt(q),sqrt(q),q), t=(0,0,gamma). Its weakest singular value is delta=q. For

    |psi_p>=sqrt(1-p)|00>+sqrt(p)|11>,

one gets

    N_q(p)=(sqrt(gamma^2 p^2+4q p(1-p))-gamma p)/2.

The Choi choice p=1/2 gives q/2. For q>0 the maximum within this aligned one-parameter input family occurs at

    p*=sqrt(q)/(gamma+2sqrt(q)),
    N_q(p*)=q/(gamma+2sqrt(q)).

The stationary equations are N^2+gamma p N-q p(1-p)=0 and gamma N=q(1-2p). The second derivative is -2q^2/(gamma^2 p^2+4q p(1-p))^(3/2), strictly negative in the interior when q>0. This proves the family optimum without numerical fitting. At q=0, use p*=0 and N=0 by the displayed continuous formulas.

For 0<q<1, gamma+2sqrt(q)=2-(1-sqrt(q))^2<2, so N_q(p*)>q/2. The old Choi theorem remains valid; the broader statement is a different proposition and is false.

Moreover N_q(p*)/q=1/(1-q+2sqrt(q)) tends to 1 as q approaches zero from above. Hence no universal inequality N_out<=c delta with constant c<1 can hold for all channels and input states. Constant 1 is optimal as a uniform linear coefficient. This is asymptotic sharpness, not equality with delta at each nonzero delta and not a global optimization over all inputs for a fixed amplitude-damping channel.

## Prior art and interpretation

The advantage of nonmaximally entangled inputs for amplitude damping and negativity/logarithmic negativity is established literature: Streltsov, Augusiak, Demianowicz and Lewenstein, Physical Review A 92, 012335 (2015), Section IV.C, including the same family optimizer in Eq. (67); https://arxiv.org/abs/1412.5885. That paper uses twice our negativity normalization; the input optimizer and ordering are unaffected. Negativity and logarithmic negativity are monotone functions of each other, so the ordering agrees. The present gate reproduces that distinction and derives the weakest-transmission bound from the certified v15.89 operator inequality. No novelty or priority claim is made.

Filtering above is a mathematical representation of the prepared input; it is not a physical postselection operation added to Phi. Canonical amplitude damping is a positive-control channel, not an externally aligned explanation of retained geometry. Native inherited channels are also evaluated directly in their stored coordinates.

This is a conditional qubit-channel consequence. It is not a capacity formula, a source-to-admissible-world law, or a gravity derivation. The original polar-skew source-selection bottleneck remains open. Time remains pruning/ordered recoverability; Genesis Pin and all historical verdicts remain intact.
