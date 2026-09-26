"""Reproduce the certified 9x243 response matrix visualization."""
import pathlib, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import independent_hidden_fixture as F
import response_quotient_rank as R

OUT=pathlib.Path("artifacts_response_quotient"); OUT.mkdir(exist_ok=True)
rho=F.state(.10,.08,.04)
A=R.matrix(rho)
s=np.linalg.svd(A,compute_uv=False)
np.savetxt(OUT/"response_matrix_9x243.csv",A,delimiter=",")
np.savetxt(OUT/"singular_values.csv",s,delimiter=",")

fig,ax=plt.subplots(figsize=(14,5))
im=ax.imshow(A,aspect="auto",interpolation="nearest")
ax.set_xlabel("Hidden x source basis direction (243)")
ax.set_ylabel("Response matrix entry (9)")
ax.set_yticks(range(9),[f"K{i+1}{j+1}" for i in range(3) for j in range(3)])
ax.set_title("Closed-form 9 x 243 response operator — frozen fixture m=.10, d=.08, a=.04")
fig.colorbar(im,ax=ax,label="Closed-form response coefficient")
fig.tight_layout();fig.savefig(OUT/"response_matrix_heatmap.png",dpi=180);plt.close(fig)

fig,ax=plt.subplots(figsize=(8,5))
ax.semilogy(range(1,10),np.maximum(s,1e-16),"o-")
ax.set_xlabel("Singular-value index");ax.set_ylabel("Singular value (log scale)")
ax.set_xticks(range(1,10));ax.set_title("Response quotient singular spectrum: 243 inputs -> rank 3")
fig.tight_layout();fig.savefig(OUT/"singular_spectrum.png",dpi=180);plt.close(fig)

print("shape",A.shape)
print("singular_values",s.tolist())
print("rank_1e-10",int(np.sum(s>s[0]*1e-10)))
