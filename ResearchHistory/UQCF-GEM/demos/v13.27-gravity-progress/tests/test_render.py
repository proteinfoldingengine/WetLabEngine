import matplotlib
matplotlib.use("Agg")
from uqcf_demo.simulation import run_telemetry, default_config
from uqcf_demo.render import render_frame


def test_render_frame_uses_rescoped_methods_and_obstruction_labels():
    data = run_telemetry(default_config(frames=5))
    fig = render_frame(data, frame_index=2)
    titles = [ax.get_title() for ax in fig.axes[:4]]
    assert len(fig.axes) >= 4
    assert "Fixed quantum-relational model" in titles[0]
    assert "BKM metrics + polar transport diagnostics" in titles[1]
    assert "Balanced graph current + projective source ray" in titles[2]
    assert "Response + DeWitt-like quadratic-form diagnostics" in titles[3]
    all_text = "\n".join(titles + [fig._suptitle.get_text()] + [text.get_text() for text in fig.texts])
    assert "not physical time" in fig._suptitle.get_text()
    assert "ADM-like" not in all_text
    assert "metric-affine" not in all_text
    assert "gravity-progress" not in all_text.lower()
