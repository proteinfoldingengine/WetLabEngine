import matplotlib
matplotlib.use("Agg")
from uqcf_demo.simulation import run_telemetry, default_config
from uqcf_demo.render import render_frame


def test_render_frame_has_four_panels_and_non_time_label():
    data = run_telemetry(default_config(frames=5))
    fig = render_frame(data, frame_index=2)
    titles = [ax.get_title() for ax in fig.axes[:4]]
    assert len(fig.axes) >= 4
    assert "Pre-time quantum relations" in titles[0]
    assert "Retained metric-affine geometry" in titles[1]
    assert "Source/current + projective" in titles[2]
    assert "ADM-like diagnostics + claim ledger" in titles[3]
    assert "not physical time" in fig._suptitle.get_text()
