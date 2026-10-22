# metrics_history.py
# Patch ID: 622.0 (Betti-Driven Activation)

from collections import deque

class MetricsHistory:
    """Manages historical data for rolling calculations and stateful forces."""
    def __init__(self, memory_window: int, global_constants: dict):
        self.history_window = 100
        self.entropy_history = deque(maxlen=memory_window)
        # Ensure the Betti history can accommodate the lifetime check window
        self.betti_history = deque(maxlen=global_constants.get('BETTI_LIFETIME_WINDOW', 100) + 20)
        self.rmsd_history = deque(maxlen=self.history_window)
        self.phi_rms_history = deque(maxlen=self.history_window)
        self.gamma_bar_history = deque(maxlen=self.history_window)
        self.d2S_dt2_history = deque(maxlen=self.history_window)
        self.df_value_history = deque(maxlen=50)
        self.ddf_dt_history = deque(maxlen=global_constants.get('DF_STAGNATION_WINDOW', 50))
        self.betti1_delta_history = deque(maxlen=global_constants.get('CONTACT_STABILITY_WINDOW', 100))
        self.betti1_delta_is_stable_history = deque(maxlen=50)

    def get_betti1_lifetime(self, threshold: int = 8) -> int:
        """
        Returns how many of the recent steps in history the Betti₁ count
        has been at or above the specified threshold.
        """
        return sum(1 for b in self.betti_history if b >= threshold)
