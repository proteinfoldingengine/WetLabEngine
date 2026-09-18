# chart_utils.py
# Patch 630: Full Backbone Angular Physics

import matplotlib.pyplot as plt
import numpy as np
import os
from collections import defaultdict

from diagnostics_registry import DIAGNOSTICS_REGISTRY

class FoldingChartEngine:
    def __init__(self, output_dir_base_path='plots', current_patch_id="Unknown_Patch"):
        self.output_dir = output_dir_base_path
        os.makedirs(self.output_dir, exist_ok=True)
        self.common_dpi = 200
        self.current_patch_id = current_patch_id
        self.registry_map = {metric.key: metric for metric in DIAGNOSTICS_REGISTRY}

    def save_and_show_figure(self, fig, report_name="Report"):
        dynamic_filename = f"UQCF_GEM_{self.current_patch_id.replace(' ', '_')}_{report_name}.png"
        filepath = os.path.join(self.output_dir, dynamic_filename)
        try:
            fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        except Exception as e:
            print(f"UserWarning: {e}")
        fig.savefig(filepath, dpi=self.common_dpi)
        print(f"Saved {report_name} to: {filepath}")
        plt.show()
        plt.close(fig)

    def _plot_3d_fold_subplot(self, ax, final_coords_np, native_coords_np, rmsd_val):
        if final_coords_np is None or native_coords_np is None: self._plot_placeholder(ax, "3D Fold"); return
        native_c = native_coords_np - native_coords_np.mean(axis=0)
        final_c = final_coords_np - final_coords_np.mean(axis=0)
        ax.plot(native_c[:,0], native_c[:,1], native_c[:,2], '.-', label='Native', color='blue', alpha=0.5, markersize=3)
        ax.plot(final_c[:,0], final_c[:,1], final_c[:,2], '.-', label=f'Folded', color='red', alpha=0.8, markersize=3)
        ax.set_title(f"Aligned Fold (RMSD: {rmsd_val:.2f} Å)", fontsize=10)
        ax.legend(fontsize='xx-small')

    def _plot_ramachandran_subplot(self, ax, phi_angles, psi_angles):
        # ✅ Bugfix: Added a robust check for None to prevent crashes.
        if phi_angles is None or psi_angles is None or phi_angles.size == 0 or psi_angles.size == 0: 
            self._plot_placeholder(ax, "Ramachandran Plot"); return
        ax.hist2d(phi_angles, psi_angles, bins=60, cmap='viridis', cmin=1)
        ax.set_title("Final Ramachandran Distribution", fontsize=10)
        ax.set_xlabel("φ (rad)", fontsize=8); ax.set_ylabel("ψ (rad)", fontsize=8)
        ax.set_xlim(-np.pi, np.pi); ax.set_ylim(-np.pi, np.pi)

    def _plot_placeholder(self, ax, title):
        ax.text(0.5, 0.5, f'{title}\n(No Data)', ha='center', va='center', fontsize=9, color='gray')
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(title, fontsize=10)

    def _plot_single_timeline(self, ax, logs, metric_def):
        if not logs.get(metric_def.key) or not any(logs[metric_def.key]): self._plot_placeholder(ax, metric_def.name); return
        ax.plot(logs["step"], logs[metric_def.key], label=metric_def.key, color=metric_def.color, linewidth=1)
        ax.set_title(metric_def.name, fontsize=10)
        ax.set_ylabel(metric_def.name, fontsize=8)
        ax.grid(True, linestyle=':')
        ax.set_yscale(metric_def.yscale)

    def _plot_dual_timeline(self, ax, logs, primary_metric, secondary_metric):
        primary_key = primary_metric.key
        title = primary_metric.name
        if not all(k in logs and logs.get(k) for k in [primary_key, "step"]): self._plot_placeholder(ax, title); return
        ax.plot(logs["step"], logs[primary_key], label=primary_metric.name, color=primary_metric.color, linewidth=1)
        ax.set_ylabel(primary_metric.name, fontsize=8, color=primary_metric.color)
        ax.tick_params(axis='y', labelcolor=primary_metric.color)
        ax.set_yscale(primary_metric.yscale)
        if secondary_metric and logs.get(secondary_metric.key):
            title += f" & {secondary_metric.name}"
            ax2 = ax.twinx()
            ax2.plot(logs["step"], logs[secondary_metric.key], label=secondary_metric.name, color=secondary_metric.color, linestyle='--', linewidth=1)
            ax2.set_ylabel(secondary_metric.name, fontsize=8, color=secondary_metric.color)
            ax2.tick_params(axis='y', labelcolor=secondary_metric.color)
            ax2.set_yscale(secondary_metric.yscale)
        ax.set_title(title, fontsize=10)
        ax.grid(True, linestyle=':')

    def _plot_boolean_flag_timeline(self, ax, logs, metric_def):
        if metric_def.key not in logs or not logs.get(metric_def.key): self._plot_placeholder(ax, metric_def.name); return
        ax.fill_between(logs["step"], logs[metric_def.key], step="post", alpha=0.3, color=metric_def.color)
        ax.plot(logs["step"], logs[metric_def.key], drawstyle='steps-post', color=metric_def.color, linewidth=1.0)
        ax.set_title(metric_def.name, fontsize=10)
        ax.set_yticks([0, 1]); ax.set_yticklabels(['Off', 'On'], fontsize=7)

    def _plot_simulation_phase_subplot(self, ax, logs):
        phases = logs.get("current_phase", [])
        if not phases: self._plot_placeholder(ax, "Simulation Phase"); return
        unique_phases = sorted(list(set(phases))) if phases else ["Compaction", "LockIn"]
        phase_map = {name: i for i, name in enumerate(unique_phases)}
        phase_nums = [phase_map.get(p, -1) for p in phases]
        ax.plot(logs["step"], phase_nums, drawstyle='steps-post', color='black', linewidth=1.5, label='Phase')
        ax.set_yticks(list(phase_map.values())); ax.set_yticklabels(list(phase_map.keys()), rotation=45, ha="right", fontsize=7)
        ax.set_ylabel("DAG Phase", fontsize=8)
        ax.set_title("Simulation Phase", fontsize=10)

    def _plot_dag_activation_breakdown(self, ax, logs):
        ax.set_title("DAG Activation Score Breakdown", fontsize=10)
        thresholds = {'gamma_bar': 2.5, 'phi_rms': 1.2, 'betti1_count': 400}
        colors = {'gamma_bar': 'gold', 'phi_rms': 'darkcyan', 'betti1_count': 'darkmagenta'}
        has_data = False
        for key, thresh in thresholds.items():
            if key in logs and logs[key]:
                if key == 'phi_rms':
                    normalized_values = thresh / (np.array(logs[key]) + 1e-9)
                    label = f'{thresh} / φ_RMS'
                else:
                    normalized_values = np.array(logs[key]) / thresh
                    label = f'{key} / {thresh}'
                ax.plot(logs["step"], normalized_values, label=label, color=colors[key], linewidth=1)
                has_data = True
        if not has_data: self._plot_placeholder(ax, "DAG Activation Breakdown"); return
        ax.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='Activation Threshold')
        ax.set_ylabel("Value / Threshold", fontsize=8)
        ax.grid(True, linestyle=':')
        ax.legend(fontsize='xx-small')
        ax.set_ylim(bottom=0)

    def _generate_comprehensive_report(self, **kwargs):
        logs = kwargs.get('logs', {})
        fig_main = plt.figure(figsize=(18, 12))
        fig_main.suptitle(f"UQCF-GEM {self.current_patch_id} - Comprehensive Report", fontsize=24, y=0.98)
        gs_main = fig_main.add_gridspec(2, 3, hspace=0.4, wspace=0.4)
        ax1 = fig_main.add_subplot(gs_main[0, 0], projection='3d')
        self._plot_3d_fold_subplot(ax1, kwargs.get('final_coords_np'), kwargs.get('native_coords_np'), kwargs.get('RMSD'))
        ax2 = fig_main.add_subplot(gs_main[0, 1])
        self._plot_dual_timeline(ax2, logs, self.registry_map['rmsd'], self.registry_map['phi_rms'])
        ax3 = fig_main.add_subplot(gs_main[0, 2])
        self._plot_dual_timeline(ax3, logs, self.registry_map['gamma_bar'], self.registry_map.get('d2S_dt2'))
        ax4 = fig_main.add_subplot(gs_main[1, 0])
        self._plot_simulation_phase_subplot(ax4, logs)
        ax5 = fig_main.add_subplot(gs_main[1, 1])
        self._plot_single_timeline(ax5, logs, self.registry_map['total_loss'])
        ax6 = fig_main.add_subplot(gs_main[1, 2])
        # ✅ Bugfix: Use the correct keys for true dihedral angles.
        self._plot_ramachandran_subplot(ax6, kwargs.get('final_phi_angles'), kwargs.get('final_psi_angles'))
        self.save_and_show_figure(fig_main, report_name="Comprehensive_Report")

    def _generate_diagnostics_report(self, **kwargs):
        logs = kwargs.get('logs', {})
        plot_groups = defaultdict(list)
        for metric in DIAGNOSTICS_REGISTRY:
            if metric.plot_group > 0:
                plot_groups[metric.plot_group].append(metric)
        if not plot_groups: return
        num_cols = 3
        num_rows = (len(plot_groups) + num_cols - 1) // num_cols
        fig_diag = plt.figure(figsize=(18, 5 * num_rows))
        fig_diag.suptitle(f"UQCF-GEM {self.current_patch_id} - Diagnostics Report", fontsize=24, y=0.98)
        
        for i, group_id in enumerate(sorted(plot_groups.keys())):
            ax = fig_diag.add_subplot(num_rows, num_cols, i + 1)
            metrics_in_group = plot_groups[group_id]
            plot_type = metrics_in_group[0].plot_type
            
            if plot_type == 'phase': self._plot_simulation_phase_subplot(ax, logs)
            elif plot_type == 'single': self._plot_single_timeline(ax, logs, metrics_in_group[0])
            elif plot_type == 'boolean': self._plot_boolean_flag_timeline(ax, logs, metrics_in_group[0])
            elif plot_type == 'dag_breakdown': self._plot_dag_activation_breakdown(ax, logs)
            elif plot_type == 'dual_primary':
                primary = metrics_in_group[0]
                secondary = next((m for m in metrics_in_group if m.plot_type == 'dual_secondary'), None)
                self._plot_dual_timeline(ax, logs, primary, secondary)
            elif plot_type == 'dual_secondary': continue
        self.save_and_show_figure(fig_diag, report_name="Diagnostics_Report")

    def generate_all_charts(self, **kwargs):
        print(f"\n--- Generating Reports ({self.current_patch_id}) ---")
        self._generate_comprehensive_report(**kwargs)
        self._generate_diagnostics_report(**kwargs)
