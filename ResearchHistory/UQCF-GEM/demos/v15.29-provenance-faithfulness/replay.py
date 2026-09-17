#!/usr/bin/env python3
from __future__ import annotations

import argparse
from functools import lru_cache
import json
from pathlib import Path

import fiber_model as fm
import provenance_equivalence as pe
import provenance_inventory as inv
import source_extension_gate as gate

ROOT = Path(__file__).resolve().parent


def _sparse(vector) -> list[list[int]]:
    return [[i, int(value)] for i, value in enumerate(vector) if int(value) != 0]


def _fiber_record(key: str, representative, root, relation_status: str) -> dict:
    diff = tuple(a - b for a, b in zip(representative.edge_vector, root.edge_vector))
    return {
        'key': key,
        'same_q_as_root': representative.q == root.q,
        'edge_nonzero': _sparse(representative.edge_vector),
        'q_nonzero': _sparse(representative.q),
        'difference_from_root_nonzero': _sparse(diff),
        'provenance_relation_to_root': relation_status,
    }


@lru_cache(None)
def payload() -> dict:
    evidence = inv.frozen_inventory(inv.REPO_ROOT)
    root = fm.root_fixture()
    face = fm.face_shift(root, face_index=0, coefficient=1)
    cycle = fm.cycle_shift(root, fm.canonical_cycle_basis()[7])

    root_relation = 'REFERENCE_REPRESENTATIVE'
    face_relation = pe.classify_pair(root, face, evidence).status
    cycle_relation = pe.classify_pair(root, cycle, evidence).status

    data = {
        'version': 'v15.29',
        'audit': gate.audit(),
        'fibers': [
            _fiber_record('root', root, root, root_relation),
            _fiber_record('face-boundary-shift', face, root, face_relation),
            _fiber_record('cycle-shift', cycle, root, cycle_relation),
        ],
        'notices': [
            'Microscopic difference is not automatically physical source difference',
            'Playback is not physical time',
            'No coupling member or gravity observable is evaluated in this replay',
        ],
    }
    return data


def write_html(data: dict, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(
        data, separators=(',', ':'), sort_keys=True, allow_nan=False
    ).replace('<', '\\u003c')
    template = (ROOT / 'viewer.html').read_text(encoding='utf-8')
    if '__DATA__' not in template:
        raise ValueError('viewer template lacks embedded-data marker')
    path.write_text(template.replace('__DATA__', encoded), encoding='utf-8')


def movie(path: Path, fps: int = 10) -> None:
    if type(fps) is not int or fps <= 0:
        raise ValueError('positive playback fps required')

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter, writers

    if not writers.is_available('ffmpeg'):
        raise RuntimeError('FFmpeg required for MP4 only')

    data = payload()
    audit = data['audit']
    fibers = data['fibers']
    shifted = fibers[1:]

    scenes = [
        (
            '1  COARSE q QUOTIENT',
            [
                'q = B1 s is the inherited coarse source control',
                'The quotient remains exact; no representative is preferred',
            ],
        ),
        (
            '2  ONE q-FIBER, MULTIPLE REPRESENTATIVES',
            [
                f"Exact examples shown: {len(fibers)}",
                f"q preserved for both shifted controls: {all(x['same_q_as_root'] for x in shifted)}",
            ],
        ),
        (
            '3  FROZEN PROVENANCE RELATION',
            [
                'Raw edge inequality is not provenance evidence',
                'Real-archive pair status: PROVENANCE_RELATION_UNSPECIFIED',
            ],
        ),
        (
            '4  GAUGE / RELABELING / ACTION BOUNDARY',
            [
                f"Natural provenance action certified: {audit['natural_action_certified']}",
                f"Representation ready: {audit['representation_ready']}",
            ],
        ),
        (
            '5  COUNTERMODEL / EXTENSION ADJUDICATION',
            [
                f"Countermodels survive: {audit['countermodels_survive']}",
                'Collapsed and distinguishing expansions share one frozen reduct',
            ],
        ),
        (
            '6  FINAL STATUS / NEXT REQUIRED OBJECT',
            [
                audit['status'],
                audit['next_required_object'],
            ],
        ),
    ]

    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    ax = fig.add_axes([0.08, 0.13, 0.84, 0.72])
    writer = FFMpegWriter(
        fps=fps,
        codec='libx264',
        bitrate=1600,
        extra_args=[
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            '-preset', 'fast',
        ],
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with writer.saving(fig, str(path), dpi=100):
        for title, lines in scenes:
            ax.clear()
            ax.set_axis_off()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.text(
                0.02, 0.90,
                'UQCF–GEM / v15.29 / PROVENANCE FAITHFULNESS',
                fontsize=11, weight='bold',
            )
            ax.text(0.02, 0.69, title, fontsize=25, weight='bold')
            for i, line in enumerate(lines):
                ax.text(0.02, 0.52 - i * 0.10, line, fontsize=15)
            ax.text(
                0.02, 0.08,
                'Microscopic difference is not automatically physical source difference.  '
                'Playback is not physical time.',
                fontsize=10,
            )
            for _ in range(4 * fps):
                writer.grab_frame()
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / 'outputs')
    parser.add_argument('--video', action='store_true')
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    data = payload()
    write_html(data, args.out / 'provenance_faithfulness.html')
    (args.out / 'replay_data.json').write_text(
        json.dumps(data, separators=(',', ':'), sort_keys=True, allow_nan=False) + '\n',
        encoding='utf-8',
    )
    gate.write_audit(args.out)
    if args.video:
        movie(args.out / 'provenance_faithfulness.mp4')
    print('v15.29 gravity-blind provenance replay generated; no coupling or gravity gate executed.')


if __name__ == '__main__':
    main()
