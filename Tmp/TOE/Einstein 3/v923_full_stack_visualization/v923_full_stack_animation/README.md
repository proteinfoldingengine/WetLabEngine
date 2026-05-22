# V923 Full-Stack MP4 Animation

This is the actual Python simulation/animation script. It loads the V921 full-stack endpoint data, recomputes the V923 lift ladder, and outputs an MP4 animation.

## Run

```bash
python v923_full_stack_geometry_information_animation.py
```

Fast preview:

```bash
python v923_full_stack_geometry_information_animation.py --duration 8 --fps 18 --dpi 110 --max-points 600
```

High quality:

```bash
python v923_full_stack_geometry_information_animation.py --duration 18 --fps 24 --dpi 150
```

Optional GIF fallback:

```bash
python v923_full_stack_geometry_information_animation.py --gif
```

## Default output folder

```text
/mnt/data/v923_full_stack_animation_run/
```

## Claim boundary

The Z-axis is a discrete source-role information index, not physical space/time. This is not a GR, EFE, CMB, black-hole, or 1/f ledger claim.
