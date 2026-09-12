#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

from uqcf_demo.simulation import default_config, run_telemetry
from uqcf_demo.render import save_final_frame, save_animation


def write_outputs(data, output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    records = data["records"]
    csv_path = out / "telemetry.csv"
    scalar_keys = [
        "frame", "lambda_source", "state_min_eigenvalue", "bkm_min_eigenvalue",
        "mean_nonmetricity", "mean_correlation", "mean_cycle_angle", "max_cycle_angle",
        "source_norm", "current_norm", "balance_residual", "conditional_response_residual",
        "cycle_rank", "cycle_dim", "projective_direction_change", "qmar_jet_norm",
        "dewitt_diagnostic",
    ]
    list_keys = [
        "local_z", "node_source", "edge_current", "edge_correlation",
        "edge_nonmetricity", "node_geometry_score", "cycle_angles",
    ]
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=scalar_keys + list_keys)
        writer.writeheader()
        for rec in records:
            row = {k: rec[k] for k in scalar_keys}
            row.update({k: json.dumps(rec[k], separators=(",", ":")) for k in list_keys})
            writer.writerow(row)

    frame_path = out / "final_frame.png"
    save_final_frame(data, frame_path)
    return {"summary": str(summary_path), "telemetry": str(csv_path), "final_frame": str(frame_path)}


def main():
    p = argparse.ArgumentParser(description="UQCF-GEM v13.27 full-stack gravity-progress simulation")
    p.add_argument("--frames", type=int, default=25)
    p.add_argument("--quick", action="store_true", help="use 9 frames")
    p.add_argument("--source-scale", type=float, default=1.0)
    p.add_argument("--output-dir", default="outputs")
    p.add_argument("--fps", type=int, default=8)
    p.add_argument("--no-video", action="store_true")
    p.add_argument("--gif-only", action="store_true")
    args = p.parse_args()

    frames = 9 if args.quick else args.frames
    cfg = default_config(frames=frames)
    cfg["source_scale"] = args.source_scale
    data = run_telemetry(cfg)
    written = write_outputs(data, args.output_dir)
    if not args.no_video:
        written.update(save_animation(data, args.output_dir, fps=args.fps, make_gif=True, make_mp4=not args.gif_only))

    print("V13.27 GRAVITY PROGRESS SIMULATION")
    print("telemetry_hash:", data["telemetry_hash"])
    print("min_state_eigenvalue:", f"{data['summary']['min_state_eigenvalue']:.6e}")
    print("min_bkm_eigenvalue:", f"{data['summary']['min_bkm_eigenvalue']:.6e}")
    print("max_source_balance_residual:", f"{data['summary']['max_source_balance_residual']:.6e}")
    print("max_projective_direction_change:", f"{data['summary']['max_projective_direction_change']:.6e}")
    print("RGCL:", data["summary"]["RGCL"])
    print("physical_Einstein_closure:", data["summary"]["physical_Einstein_closure"])
    for k, v in written.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
