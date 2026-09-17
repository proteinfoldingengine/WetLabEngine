from __future__ import annotations

from dataclasses import asdict
from functools import lru_cache
from pathlib import Path
import argparse
import json

import definability_gate as gate
import exact_fiber as ef
import frozen_inputs as fi
import typed_carrier_graph as tc

ROOT = Path(__file__).resolve().parent


def _sparse(vector) -> list[list[int]]:
    return [[i, int(value)] for i, value in enumerate(vector) if int(value) != 0]


@lru_cache(None)
def payload() -> dict:
    candidates = fi.candidate_inventory(fi.REPO_ROOT)
    graph, _ = tc.build_real_graph()
    fibers = ef.canonical_fiber_cases()
    audit = gate.audit()

    typed_graph = {
        'nodes': list(graph.nodes()),
        'edges': [asdict(edge) for edge in graph.edges()],
    }
    fiber_rows = [
        {
            'key': case.key,
            'same_q_as_root': ef.same_q_exact(fibers[0], case),
            'edge_nonzero': _sparse(case.edge_vector),
            'q_nonzero': _sparse(case.q),
        }
        for case in fibers
    ]
    candidate_rows = [
        {
            'key': candidate.key,
            'domain': candidate.domain,
            'claim_boundary': candidate.claim_boundary,
            'transformation_source': candidate.transformation_source,
        }
        for candidate in candidates
    ]

    return {
        'version': 'v15.30',
        'candidates': candidate_rows,
        'typed_graph': typed_graph,
        'fibers': fiber_rows,
        'audit': audit,
        'notices': [
            'Microscopic difference is not automatically provenance difference.',
            'Playback is not physical time.',
            'No coupling member or gravity observable is evaluated.',
        ],
    }


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
        raise RuntimeError('FFmpeg required for MP4 delivery')

    data = payload()
    audit = data['audit']
    candidates = data['candidates']
    fibers = data['fibers']
    graph = data['typed_graph']

    scenes = [
        (
            '1  FOUR FROZEN CANDIDATE ORIGINS',
            [
                f"Candidate origins fixed before execution: {len(candidates)}",
                'History lineage · ternary role · retained source/current · Genesis 6-D',
            ],
        ),
        (
            '2  TYPED COMMON-CARRIER GRAPH / GATE A',
            [
                f"Certified graph nodes: {len(graph['nodes'])}",
                f"Real common-carrier candidates: {audit['common_carrier_count']}",
            ],
        ),
        (
            '3  ONE EXACT q-FIBER / MULTIPLE MICROSCOPIC REPRESENTATIVES',
            [
                f"Exact representatives shown: {len(fibers)}",
                f"All share root q exactly: {all(row['same_q_as_root'] for row in fibers)}",
            ],
        ),
        (
            '4  FROZEN-DATA AUTOMORPHISM / DEFINABILITY BOUNDARY',
            [
                'A distinction must survive the certified symmetries of its frozen data.',
                f"Real natural relations reaching this gate: {audit['natural_relation_count']}",
            ],
        ),
        (
            '5  UNIQUENESS OR COUNTERMODEL ADJUDICATION',
            [
                f"Countermodels survive: {audit['countermodels_survive']}",
                f"Canonical provenance relation certified: {audit['canonical_relation_certified']}",
            ],
        ),
        (
            '6  FINAL v15.30 STATUS / NEXT REQUIRED OBJECT',
            [
                audit['status'],
                audit['next_required_object'],
            ],
        ),
    ]

    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    ax = fig.add_axes([0.07, 0.12, 0.86, 0.76])
    writer = FFMpegWriter(
        fps=fps,
        codec='libx264',
        bitrate=1600,
        extra_args=['-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-preset', 'fast'],
    )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    footer = (
        'Microscopic difference is not automatically provenance difference.  '
        'Playback is not physical time.\n'
        'No coupling member or gravity observable is evaluated.'
    )

    with writer.saving(fig, str(path), dpi=100):
        for title, lines in scenes:
            ax.clear()
            ax.set_axis_off()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.text(0.02, 0.92, 'UQCF–GEM / v15.30 / PROVENANCE–FIBER DEFINABILITY',
                    fontsize=11, weight='bold')
            ax.text(0.02, 0.70, title, fontsize=24, weight='bold')
            for i, line in enumerate(lines):
                ax.text(0.02, 0.52 - i * 0.11, line, fontsize=14)
            ax.text(0.02, 0.08, footer, fontsize=9.5, linespacing=1.5)
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
    write_html(data, args.out / 'provenance_fiber_definability.html')
    (args.out / 'replay_data.json').write_text(
        json.dumps(data, separators=(',', ':'), sort_keys=True, allow_nan=False) + '\n',
        encoding='utf-8',
    )
    gate.write_audit(args.out)
    if args.video:
        movie(args.out / 'provenance_fiber_definability.mp4')
    print('v15.30 gravity-blind definability replay generated; no coupling or gravity gate executed.')


if __name__ == '__main__':
    main()
