
import math
from pathlib import Path
import numpy as np

def paulis():
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.array([[1,0],[0,-1]],complex)
    return sx,sy,sz

def _comm(A,B):
    return A@B-B@A

def _unitary(axis, angle):
    sx,sy,sz=paulis()
    amap={"x":sx,"y":sy,"z":sz}
    A=amap[axis]
    return math.cos(angle/2)*np.eye(2)-1j*math.sin(angle/2)*A

def density_state(lam):
    # Fixed mixed seed, swept through an ordered family of unitary relational transforms.
    rho0=np.array([[0.72,0.11-0.04j],[0.11+0.04j,0.28]],complex)
    # enforce exact Hermiticity/trace; seed is positive.
    rho0=0.5*(rho0+rho0.conj().T)
    rho0=rho0/np.trace(rho0)
    U=_unitary("z",0.55*lam)@_unitary("y",0.35*lam)@_unitary("x",0.20*lam)
    rho=U@rho0@U.conj().T
    return rho

def moment_map(rho,A):
    return float(np.real(np.trace(rho@A)))

def kks_bracket(rho,A,B):
    return float(np.real(-1j*np.trace(rho@_comm(A,B))))

def exact_closure_residual(rho):
    sx,sy,sz=paulis()
    lhs=kks_bracket(rho,sx,sy)
    rhs=2.0*moment_map(rho,sz)
    return abs(lhs-rhs)

def broken_closure_residual(rho):
    sx,sy,sz=paulis()
    lhs=kks_bracket(rho,sx,sy)
    # Deliberately wrong public control: incorrect structure coefficient + contamination.
    rhs=1.25*moment_map(rho,sz)+0.15*moment_map(rho,sx)
    return abs(lhs-rhs)

def sweep_records(n_steps=121):
    sx,sy,sz=paulis()
    rows=[]
    for i,lam in enumerate(np.linspace(0,2*np.pi,n_steps)):
        rho=density_state(float(lam))
        Cx=moment_map(rho,sx)
        Cy=moment_map(rho,sy)
        Cz=moment_map(rho,sz)
        exact_bracket=kks_bracket(rho,sx,sy)
        exact_rhs=2.0*Cz
        broken_rhs=1.25*Cz+0.15*Cx
        rows.append({
            "step":int(i),
            "lambda":float(lam),
            "Cx":Cx,
            "Cy":Cy,
            "Cz":Cz,
            "exact_bracket":exact_bracket,
            "exact_rhs":exact_rhs,
            "exact_residual":abs(exact_bracket-exact_rhs),
            "broken_rhs":broken_rhs,
            "broken_residual":abs(exact_bracket-broken_rhs),
            "purity":float(np.real(np.trace(rho@rho))),
        })
    return rows

def bloch_vector(rho):
    sx,sy,sz=paulis()
    return np.array([moment_map(rho,sx),moment_map(rho,sy),moment_map(rho,sz)],float)


def export_csv(rows, path):
    import csv
    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields=list(rows[0].keys())
    with path.open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return str(path)

def render_static_plot(rows, path):
    import matplotlib.pyplot as plt
    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lam=np.array([r["lambda"] for r in rows])
    exact=np.array([r["exact_residual"] for r in rows])
    broken=np.array([r["broken_residual"] for r in rows])

    fig, ax=plt.subplots(figsize=(9,5))
    ax.plot(lam, exact, label="Exact quantum closure residual")
    ax.plot(lam, broken, label="Broken-control residual")
    ax.set_xlabel("Ordered relational sweep parameter λ (not physical time)")
    ax.set_ylabel("Closure residual")
    ax.set_title("v12.41 Quantum Moment-Map Closure")
    ax.set_yscale("symlog", linthresh=1e-14)
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return str(path)

def render_animation(rows, mp4_path, gif_path=None, fps=24):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

    mp4_path=Path(mp4_path)
    mp4_path.parent.mkdir(parents=True, exist_ok=True)
    gif_path=Path(gif_path) if gif_path is not None else None

    lam=np.array([r["lambda"] for r in rows])
    Cx=np.array([r["Cx"] for r in rows])
    Cy=np.array([r["Cy"] for r in rows])
    Cz=np.array([r["Cz"] for r in rows])
    exact=np.array([r["exact_residual"] for r in rows])
    broken=np.array([r["broken_residual"] for r in rows])

    fig=plt.figure(figsize=(12,4.8))
    ax1=fig.add_subplot(131, projection="3d")
    ax2=fig.add_subplot(132)
    ax3=fig.add_subplot(133)

    maxb=max(1.0, np.max(np.sqrt(Cx**2+Cy**2+Cz**2))*1.15)
    for ax in [ax1]:
        ax.set_xlim(-maxb,maxb); ax.set_ylim(-maxb,maxb); ax.set_zlim(-maxb,maxb)
        ax.set_xlabel("Cx"); ax.set_ylabel("Cy"); ax.set_zlabel("Cz")
        ax.set_title("Relational quantum state\n(Bloch / moment-map coordinates)")

    ax2.set_xlim(lam.min(),lam.max())
    vals=np.concatenate([Cx,Cy,Cz])
    pad=max(0.2,0.1*(vals.max()-vals.min()+1e-9))
    ax2.set_ylim(vals.min()-pad,vals.max()+pad)
    ax2.set_xlabel("Ordered sweep λ")
    ax2.set_ylabel("Moment maps")
    ax2.set_title(r"$C_A(\rho)=\mathrm{Tr}(\rho A)$")
    ax2.grid(True,alpha=0.25)

    ymax=max(0.1,broken.max()*1.15)
    ax3.set_xlim(lam.min(),lam.max())
    ax3.set_ylim(-0.01*ymax,ymax)
    ax3.set_xlabel("Ordered sweep λ")
    ax3.set_ylabel("Closure residual")
    ax3.set_title("Exact vs deliberately broken")
    ax3.grid(True,alpha=0.25)

    point,=ax1.plot([],[],[],"o",markersize=8)
    trail,=ax1.plot([],[],[],linewidth=1.2)
    lx,=ax2.plot([],[],label="Cx")
    ly,=ax2.plot([],[],label="Cy")
    lz,=ax2.plot([],[],label="Cz")
    ax2.legend(loc="upper right")
    le,=ax3.plot([],[],label="Exact")
    lb,=ax3.plot([],[],label="Broken")
    ax3.legend(loc="upper right")
    status=fig.text(0.5,0.01,"",ha="center",va="bottom",fontsize=10)

    def update(i):
        sl=slice(0,i+1)
        point.set_data([Cx[i]],[Cy[i]])
        point.set_3d_properties([Cz[i]])
        trail.set_data(Cx[sl],Cy[sl])
        trail.set_3d_properties(Cz[sl])
        lx.set_data(lam[sl],Cx[sl]); ly.set_data(lam[sl],Cy[sl]); lz.set_data(lam[sl],Cz[sl])
        le.set_data(lam[sl],exact[sl]); lb.set_data(lam[sl],broken[sl])
        status.set_text(
            f"λ={lam[i]:.3f}   exact Δ={exact[i]:.3e}   broken Δ={broken[i]:.3e}   "
            "λ indexes ordered relational transformations — not physical time"
        )
        return point,trail,lx,ly,lz,le,lb,status

    ani=FuncAnimation(fig,update,frames=len(rows),interval=1000/fps,blit=False)
    wrote_mp4=False
    try:
        writer=FFMpegWriter(fps=fps, bitrate=2200)
        ani.save(mp4_path, writer=writer)
        wrote_mp4=True
    except Exception:
        wrote_mp4=False

    if gif_path is not None:
        ani.save(gif_path, writer=PillowWriter(fps=max(8,min(fps,20))))

    plt.close(fig)
    return {
        "mp4": str(mp4_path) if wrote_mp4 and mp4_path.exists() else None,
        "gif": str(gif_path) if gif_path is not None and gif_path.exists() else None,
    }

def run_public_simulation(outdir, n_steps=121, fps=24):
    outdir=Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows=sweep_records(n_steps)

    max_exact=max(r["exact_residual"] for r in rows)
    max_broken=max(r["broken_residual"] for r in rows)
    min_eig=min(float(np.linalg.eigvalsh(density_state(r["lambda"])).min()) for r in rows)

    assert max_exact < 1e-12, f"exact closure failed: {max_exact}"
    assert max_broken > 0.05, f"broken control too weak: {max_broken}"
    assert min_eig >= -1e-12, f"invalid density matrix: {min_eig}"

    csv_path=export_csv(rows,outdir/"v1241_public_simulation_diagnostics.csv")
    png_path=render_static_plot(rows,outdir/"v1241_public_simulation_verification.png")
    anim=render_animation(
        rows,
        outdir/"v1241_public_simulation.mp4",
        outdir/"v1241_public_simulation.gif",
        fps=fps,
    )

    log=outdir/"v1241_public_simulation_run.log"
    log.write_text(
        "UQCF-GEM v12.41 public simulation\n"
        f"steps={n_steps}\n"
        f"max_exact_closure_residual={max_exact:.18e}\n"
        f"max_broken_closure_residual={max_broken:.18e}\n"
        f"minimum_density_eigenvalue={min_eig:.18e}\n"
        f"mp4={anim['mp4']}\n"
        f"gif={anim['gif']}\n"
        "sweep_semantics=ordered relational transformations; not physical time\n"
    )
    return {
        "csv":csv_path,
        "png":png_path,
        "mp4":anim["mp4"],
        "gif":anim["gif"],
        "log":str(log),
        "max_exact_closure_residual":max_exact,
        "max_broken_closure_residual":max_broken,
        "minimum_density_eigenvalue":min_eig,
    }

if __name__=="__main__":
    result=run_public_simulation(Path(__file__).resolve().parent/"outputs")
    print(result)
