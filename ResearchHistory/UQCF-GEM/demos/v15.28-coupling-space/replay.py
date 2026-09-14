#!/usr/bin/env python3
from __future__ import annotations
import argparse
from functools import lru_cache
import json
from pathlib import Path
import coupling_gate as gate

ROOT = Path(__file__).resolve().parent

@lru_cache(None)
def payload():
    audit = gate.audit()
    return {
        'version': 'v15.28',
        'audit': audit,
        'notice': 'Representation and coupling-space inspection only. No gravity observable was used to choose the coupling. Scale unresolved.',
    }


def write_html(data, path: Path):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(data, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')
    path.write_text((ROOT / 'viewer.html').read_text().replace('__DATA__', encoded), encoding='utf-8')


def movie(path: Path, fps: int = 10):
    if type(fps) is not int or fps <= 0:
        raise ValueError('positive playback fps required')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter, writers
    if not writers.is_available('ffmpeg'):
        raise RuntimeError('FFmpeg required for MP4 only')
    data = payload()['audit']; q = data['q_control']; candidates = data['candidates']
    scenes = [
        ('FROZEN INVENTORY', ['Hash-pinned representation carriers', 'No candidate admitted by convenience']),
        ('EXACT SYMMETRY', ['392 torus automorphisms', 'Integer / rational rank adjudication']),
        ('SOLVER CONTROLS', ['Synthetic coupling spaces: 0, 1, >1', 'Basis changes preserve exact dimension']),
        ('SOURCE QUOTIENT CONTROL', [f"d_eta = {q['dimension']}", 'Baseline control — not a physical candidate']),
        ('PROVENANCE AUDIT', [f"Blocked candidates: {data['blocked_candidate_count']}", f"Eligible physical candidates: {data['eligible_candidate_count']}"]),
        ('PREREGISTERED VERDICT', [data['status'], 'No unique physical coupling form frozen']),
    ]
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    ax = fig.add_axes([.08, .13, .84, .72])
    writer = FFMpegWriter(fps=fps, codec='libx264', bitrate=1600,
                          extra_args=['-pix_fmt','yuv420p','-movflags','+faststart','-preset','fast'])
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with writer.saving(fig, str(path), dpi=100):
        for title, lines in scenes:
            ax.clear(); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
            ax.text(.02,.90,'UQCF–GEM / v15.28 / PRE-TIME COUPLING SPACE',fontsize=11,weight='bold')
            ax.text(.02,.69,title,fontsize=26,weight='bold')
            for i, line in enumerate(lines):
                ax.text(.02,.52-i*.10,line,fontsize=15)
            ax.text(.02,.08,'No gravity observable selected the coupling. Playback is not physical time.',fontsize=10)
            for _ in range(4*fps):
                writer.grab_frame()
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(); p.add_argument('--out', type=Path, default=ROOT/'outputs'); p.add_argument('--video', action='store_true')
    a = p.parse_args(); a.out.mkdir(parents=True, exist_ok=True); data = payload()
    write_html(data, a.out/'coupling_space.html')
    (a.out/'replay_data.json').write_text(json.dumps(data, separators=(',', ':'), allow_nan=False)+'\n')
    gate.write_results(a.out/'verification.json', data['audit'])
    if a.video: movie(a.out/'coupling_space.mp4')
    print('v15.28 gravity-blind coupling-space replay generated; no gravity canary executed.')

if __name__ == '__main__':
    main()
