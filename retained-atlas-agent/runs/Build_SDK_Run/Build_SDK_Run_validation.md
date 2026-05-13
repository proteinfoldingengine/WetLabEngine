# Build_SDK_Run — Scientific Execution Validation

## Overall Status
pass

## Interpretation Allowed
True

## Selected Regime Present
True

## Row Counts
- valid_row_count: 5
- total_row_count: 342
- valid_controller_row_count: 0
- total_controller_row_count: 0

## Failures
- None

## Warnings
- None

## Row Checks

### all_candidates_0
- path: all_candidates[0]
- row_interpretable: False
- bad_rate: 0.25
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 2.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_1
- path: all_candidates[1]
- row_interpretable: False
- bad_rate: 0.25
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 2.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_2
- path: all_candidates[2]
- row_interpretable: False
- bad_rate: 0.125
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 1.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_3
- path: all_candidates[3]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_4
- path: all_candidates[4]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_5
- path: all_candidates[5]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.6428571428571428
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_6
- path: all_candidates[6]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.7857142857142857
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_7
- path: all_candidates[7]
- row_interpretable: False
- bad_rate: 0.0
- trigger_rate: 0.125
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 0.0
- valid_for_interpretation: False
- failures: ['bad_rate_zero', 'phase_counts_bad_zero', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_8
- path: all_candidates[8]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_9
- path: all_candidates[9]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.8333333333333333
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_10
- path: all_candidates[10]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_11
- path: all_candidates[11]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.75
- auc: 0.9333333333333333
- balanced_accuracy: 0.8
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_12
- path: all_candidates[12]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.8
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_13
- path: all_candidates[13]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.7857142857142857
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_14
- path: all_candidates[14]
- row_interpretable: False
- bad_rate: 0.0
- trigger_rate: 0.125
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 0.0
- valid_for_interpretation: False
- failures: ['bad_rate_zero', 'phase_counts_bad_zero', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_15
- path: all_candidates[15]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_16
- path: all_candidates[16]
- row_interpretable: False
- bad_rate: 0.25
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 2.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_17
- path: all_candidates[17]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.9
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_18
- path: all_candidates[18]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_19
- path: all_candidates[19]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.7857142857142857
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_20
- path: all_candidates[20]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_21
- path: all_candidates[21]
- row_interpretable: False
- bad_rate: 0.125
- trigger_rate: 0.25
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 1.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_22
- path: all_candidates[22]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_23
- path: all_candidates[23]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_24
- path: all_candidates[24]
- row_interpretable: False
- bad_rate: 0.125
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 1.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 1.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_25
- path: all_candidates[25]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.7142857142857143
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_26
- path: all_candidates[26]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.7142857142857143
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_27
- path: all_candidates[27]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_28
- path: all_candidates[28]
- row_interpretable: False
- bad_rate: 0.25
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 2.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_29
- path: all_candidates[29]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 1.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_30
- path: all_candidates[30]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.6
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_31
- path: all_candidates[31]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_32
- path: all_candidates[32]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_33
- path: all_candidates[33]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_34
- path: all_candidates[34]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_35
- path: all_candidates[35]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_36
- path: all_candidates[36]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_37
- path: all_candidates[37]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.8
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_38
- path: all_candidates[38]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 1.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_39
- path: all_candidates[39]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.9166666666666667
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_40
- path: all_candidates[40]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_41
- path: all_candidates[41]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_42
- path: all_candidates[42]
- row_interpretable: False
- bad_rate: 0.125
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 1.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_43
- path: all_candidates[43]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.6
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_44
- path: all_candidates[44]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.5833333333333334
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_45
- path: all_candidates[45]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_46
- path: all_candidates[46]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_47
- path: all_candidates[47]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_48
- path: all_candidates[48]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_49
- path: all_candidates[49]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_50
- path: all_candidates[50]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_51
- path: all_candidates[51]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_52
- path: all_candidates[52]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_53
- path: all_candidates[53]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.8571428571428572
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_54
- path: all_candidates[54]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_55
- path: all_candidates[55]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_56
- path: all_candidates[56]
- row_interpretable: False
- bad_rate: 0.125
- trigger_rate: 0.125
- auc: 1.0
- balanced_accuracy: 1.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 1.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_57
- path: all_candidates[57]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.6666666666666666
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_58
- path: all_candidates[58]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_59
- path: all_candidates[59]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.6428571428571428
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_60
- path: all_candidates[60]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_61
- path: all_candidates[61]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_62
- path: all_candidates[62]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_63
- path: all_candidates[63]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_64
- path: all_candidates[64]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.375
- auc: 1.0
- balanced_accuracy: 0.6666666666666666
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_65
- path: all_candidates[65]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_66
- path: all_candidates[66]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 1.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_67
- path: all_candidates[67]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_68
- path: all_candidates[68]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_69
- path: all_candidates[69]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_70
- path: all_candidates[70]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_71
- path: all_candidates[71]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.6666666666666666
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_72
- path: all_candidates[72]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.8571428571428572
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_73
- path: all_candidates[73]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.9285714285714286
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_74
- path: all_candidates[74]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_75
- path: all_candidates[75]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_76
- path: all_candidates[76]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_77
- path: all_candidates[77]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.6666666666666666
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_78
- path: all_candidates[78]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_79
- path: all_candidates[79]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_80
- path: all_candidates[80]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_81
- path: all_candidates[81]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_82
- path: all_candidates[82]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_83
- path: all_candidates[83]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_84
- path: all_candidates[84]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_85
- path: all_candidates[85]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_86
- path: all_candidates[86]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.8333333333333333
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_87
- path: all_candidates[87]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_88
- path: all_candidates[88]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_89
- path: all_candidates[89]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_90
- path: all_candidates[90]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_91
- path: all_candidates[91]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero', 'balanced_accuracy_at_chance']

### all_candidates_92
- path: all_candidates[92]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.8333333333333333
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_93
- path: all_candidates[93]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.1875
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_94
- path: all_candidates[94]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_95
- path: all_candidates[95]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.1875
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_96
- path: all_candidates[96]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_97
- path: all_candidates[97]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_98
- path: all_candidates[98]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.6
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_99
- path: all_candidates[99]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.625
- auc: 1.0
- balanced_accuracy: 0.875
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_100
- path: all_candidates[100]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_101
- path: all_candidates[101]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_102
- path: all_candidates[102]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_103
- path: all_candidates[103]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_104
- path: all_candidates[104]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_105
- path: all_candidates[105]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.5
- auc: 1.0
- balanced_accuracy: 0.8333333333333333
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_106
- path: all_candidates[106]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 1.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_107
- path: all_candidates[107]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.8571428571428572
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_108
- path: all_candidates[108]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_109
- path: all_candidates[109]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_110
- path: all_candidates[110]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_111
- path: all_candidates[111]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_112
- path: all_candidates[112]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.5714285714285714
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_113
- path: all_candidates[113]
- row_interpretable: False
- bad_rate: 0.5
- trigger_rate: 0.75
- auc: 0.9375
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 4.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_114
- path: all_candidates[114]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.8571428571428572
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_115
- path: all_candidates[115]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_116
- path: all_candidates[116]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_117
- path: all_candidates[117]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_118
- path: all_candidates[118]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_119
- path: all_candidates[119]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.8
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_120
- path: all_candidates[120]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.9166666666666667
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_121
- path: all_candidates[121]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.7857142857142857
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_122
- path: all_candidates[122]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.1875
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_123
- path: all_candidates[123]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_124
- path: all_candidates[124]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_125
- path: all_candidates[125]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_126
- path: all_candidates[126]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_127
- path: all_candidates[127]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.6666666666666666
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_128
- path: all_candidates[128]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 0.8571428571428571
- balanced_accuracy: 0.8571428571428572
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_129
- path: all_candidates[129]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_130
- path: all_candidates[130]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_131
- path: all_candidates[131]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_132
- path: all_candidates[132]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_133
- path: all_candidates[133]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.75
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_134
- path: all_candidates[134]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.9166666666666667
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_135
- path: all_candidates[135]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.7857142857142857
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_136
- path: all_candidates[136]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_137
- path: all_candidates[137]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_138
- path: all_candidates[138]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_139
- path: all_candidates[139]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_140
- path: all_candidates[140]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.9166666666666667
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_141
- path: all_candidates[141]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.7857142857142857
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_142
- path: all_candidates[142]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_143
- path: all_candidates[143]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_144
- path: all_candidates[144]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_145
- path: all_candidates[145]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_146
- path: all_candidates[146]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_147
- path: all_candidates[147]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_148
- path: all_candidates[148]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_149
- path: all_candidates[149]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_150
- path: all_candidates[150]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_151
- path: all_candidates[151]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_152
- path: all_candidates[152]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_153
- path: all_candidates[153]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_154
- path: all_candidates[154]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.1875
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_155
- path: all_candidates[155]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_156
- path: all_candidates[156]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_157
- path: all_candidates[157]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_158
- path: all_candidates[158]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_159
- path: all_candidates[159]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_160
- path: all_candidates[160]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_161
- path: all_candidates[161]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.8571428571428572
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_162
- path: all_candidates[162]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_163
- path: all_candidates[163]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.1875
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_164
- path: all_candidates[164]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_165
- path: all_candidates[165]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_166
- path: all_candidates[166]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_167
- path: all_candidates[167]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_168
- path: all_candidates[168]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.75
- auc: 1.0
- balanced_accuracy: 0.8
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_169
- path: all_candidates[169]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_170
- path: all_candidates[170]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_171
- path: all_candidates[171]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_172
- path: all_candidates[172]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_173
- path: all_candidates[173]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_174
- path: all_candidates[174]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_175
- path: all_candidates[175]
- row_interpretable: False
- bad_rate: 0.625
- trigger_rate: 0.875
- auc: 1.0
- balanced_accuracy: 0.8
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 5.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_176
- path: all_candidates[176]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.8571428571428572
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_177
- path: all_candidates[177]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_178
- path: all_candidates[178]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_179
- path: all_candidates[179]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_180
- path: all_candidates[180]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_181
- path: all_candidates[181]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_182
- path: all_candidates[182]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 1.0
- balanced_accuracy: 0.7142857142857143
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_183
- path: all_candidates[183]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_184
- path: all_candidates[184]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_185
- path: all_candidates[185]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_186
- path: all_candidates[186]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_187
- path: all_candidates[187]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_188
- path: all_candidates[188]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_189
- path: all_candidates[189]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_190
- path: all_candidates[190]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_191
- path: all_candidates[191]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_192
- path: all_candidates[192]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_193
- path: all_candidates[193]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_194
- path: all_candidates[194]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_195
- path: all_candidates[195]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_196
- path: all_candidates[196]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.3125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_197
- path: all_candidates[197]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_198
- path: all_candidates[198]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_199
- path: all_candidates[199]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_200
- path: all_candidates[200]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_201
- path: all_candidates[201]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_202
- path: all_candidates[202]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_203
- path: all_candidates[203]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_204
- path: all_candidates[204]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_205
- path: all_candidates[205]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_206
- path: all_candidates[206]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_207
- path: all_candidates[207]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_208
- path: all_candidates[208]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_209
- path: all_candidates[209]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_210
- path: all_candidates[210]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_211
- path: all_candidates[211]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_212
- path: all_candidates[212]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_213
- path: all_candidates[213]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_214
- path: all_candidates[214]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_215
- path: all_candidates[215]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_216
- path: all_candidates[216]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_217
- path: all_candidates[217]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_218
- path: all_candidates[218]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_219
- path: all_candidates[219]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_220
- path: all_candidates[220]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_221
- path: all_candidates[221]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_222
- path: all_candidates[222]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_223
- path: all_candidates[223]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_224
- path: all_candidates[224]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_225
- path: all_candidates[225]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_226
- path: all_candidates[226]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_227
- path: all_candidates[227]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_228
- path: all_candidates[228]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_229
- path: all_candidates[229]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_230
- path: all_candidates[230]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_231
- path: all_candidates[231]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_232
- path: all_candidates[232]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_233
- path: all_candidates[233]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_234
- path: all_candidates[234]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_235
- path: all_candidates[235]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_236
- path: all_candidates[236]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_237
- path: all_candidates[237]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_238
- path: all_candidates[238]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_239
- path: all_candidates[239]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_240
- path: all_candidates[240]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_241
- path: all_candidates[241]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_242
- path: all_candidates[242]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_243
- path: all_candidates[243]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_244
- path: all_candidates[244]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_245
- path: all_candidates[245]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_246
- path: all_candidates[246]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_247
- path: all_candidates[247]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_248
- path: all_candidates[248]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_249
- path: all_candidates[249]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_250
- path: all_candidates[250]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_251
- path: all_candidates[251]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_252
- path: all_candidates[252]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_253
- path: all_candidates[253]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_254
- path: all_candidates[254]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_255
- path: all_candidates[255]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_256
- path: all_candidates[256]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_257
- path: all_candidates[257]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_258
- path: all_candidates[258]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_259
- path: all_candidates[259]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_260
- path: all_candidates[260]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_261
- path: all_candidates[261]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_262
- path: all_candidates[262]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_263
- path: all_candidates[263]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_264
- path: all_candidates[264]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_265
- path: all_candidates[265]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_266
- path: all_candidates[266]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_267
- path: all_candidates[267]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_268
- path: all_candidates[268]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_269
- path: all_candidates[269]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_270
- path: all_candidates[270]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_271
- path: all_candidates[271]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_272
- path: all_candidates[272]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_273
- path: all_candidates[273]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_274
- path: all_candidates[274]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_275
- path: all_candidates[275]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_276
- path: all_candidates[276]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_277
- path: all_candidates[277]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_278
- path: all_candidates[278]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_279
- path: all_candidates[279]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_280
- path: all_candidates[280]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_281
- path: all_candidates[281]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_282
- path: all_candidates[282]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_283
- path: all_candidates[283]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_284
- path: all_candidates[284]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_285
- path: all_candidates[285]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_286
- path: all_candidates[286]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_287
- path: all_candidates[287]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_288
- path: all_candidates[288]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_289
- path: all_candidates[289]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_290
- path: all_candidates[290]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_291
- path: all_candidates[291]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_292
- path: all_candidates[292]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_293
- path: all_candidates[293]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0004657758497160036
- horizon_width: 0.03125
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: True
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one']
- warnings: ['auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_294
- path: all_candidates[294]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.4375
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance']

### all_candidates_295
- path: all_candidates[295]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_296
- path: all_candidates[296]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_297
- path: all_candidates[297]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_298
- path: all_candidates[298]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_299
- path: all_candidates[299]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_300
- path: all_candidates[300]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_301
- path: all_candidates[301]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_302
- path: all_candidates[302]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_303
- path: all_candidates[303]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_304
- path: all_candidates[304]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_305
- path: all_candidates[305]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_306
- path: all_candidates[306]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_307
- path: all_candidates[307]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_308
- path: all_candidates[308]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_309
- path: all_candidates[309]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_310
- path: all_candidates[310]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_311
- path: all_candidates[311]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_312
- path: all_candidates[312]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_313
- path: all_candidates[313]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_314
- path: all_candidates[314]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_315
- path: all_candidates[315]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_316
- path: all_candidates[316]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_317
- path: all_candidates[317]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_318
- path: all_candidates[318]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_319
- path: all_candidates[319]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_320
- path: all_candidates[320]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_321
- path: all_candidates[321]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_322
- path: all_candidates[322]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_323
- path: all_candidates[323]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_324
- path: all_candidates[324]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_325
- path: all_candidates[325]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_326
- path: all_candidates[326]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_327
- path: all_candidates[327]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_328
- path: all_candidates[328]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0016869769739494794
- horizon_width: 0.078125
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: True
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one']
- warnings: ['auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_329
- path: all_candidates[329]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_330
- path: all_candidates[330]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_331
- path: all_candidates[331]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_332
- path: all_candidates[332]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_333
- path: all_candidates[333]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero', 'auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_334
- path: all_candidates[334]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.000662699456690748
- horizon_width: 0.046875
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: True
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one']
- warnings: ['auc_at_chance', 'balanced_accuracy_at_chance']

### all_candidates_335
- path: all_candidates[335]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.002675187836599823
- horizon_width: 0.140625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: True
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one']
- warnings: ['auc_at_chance', 'balanced_accuracy_at_chance']

### controller_rows
- path: controller_rows
- row_interpretable: True
- bad_rate: None
- trigger_rate: None
- auc: None
- balanced_accuracy: None
- horizon_area: None
- horizon_width: None
- score_var: None
- phase_counts_bad: None
- valid_for_interpretation: None
- failures: []
- warnings: ['bad_rate_missing', 'trigger_rate_missing', 'auc_missing_or_undefined', 'balanced_accuracy_missing', 'validity_gate_missing_or_no_valid_for_interpretation']

### notes
- path: notes
- row_interpretable: True
- bad_rate: None
- trigger_rate: None
- auc: None
- balanced_accuracy: None
- horizon_area: None
- horizon_width: None
- score_var: None
- phase_counts_bad: None
- valid_for_interpretation: None
- failures: []
- warnings: ['bad_rate_missing', 'trigger_rate_missing', 'auc_missing_or_undefined', 'balanced_accuracy_missing', 'validity_gate_missing_or_no_valid_for_interpretation']

### selected_regime
- path: selected_regime
- row_interpretable: True
- bad_rate: None
- trigger_rate: None
- auc: None
- balanced_accuracy: None
- horizon_area: None
- horizon_width: None
- score_var: None
- phase_counts_bad: None
- valid_for_interpretation: None
- failures: []
- warnings: ['bad_rate_missing', 'trigger_rate_missing', 'auc_missing_or_undefined', 'balanced_accuracy_missing', 'validity_gate_missing_or_no_valid_for_interpretation']

### selected_regime_summary
- path: selected_regime_summary
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5
- balanced_accuracy: 0.5
- horizon_area: 0.002675187836599823
- horizon_width: 0.140625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: True
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one']
- warnings: ['auc_at_chance', 'balanced_accuracy_at_chance']

### validity_gate
- path: validity_gate
- row_interpretable: True
- bad_rate: None
- trigger_rate: None
- auc: None
- balanced_accuracy: None
- horizon_area: None
- horizon_width: None
- score_var: None
- phase_counts_bad: None
- valid_for_interpretation: None
- failures: []
- warnings: ['bad_rate_missing', 'trigger_rate_missing', 'auc_missing_or_undefined', 'balanced_accuracy_missing', 'validity_gate_missing_or_no_valid_for_interpretation']

### selected_regime
- path: selected_regime
- row_interpretable: True
- bad_rate: None
- trigger_rate: None
- auc: None
- balanced_accuracy: None
- horizon_area: None
- horizon_width: None
- score_var: None
- phase_counts_bad: None
- valid_for_interpretation: None
- failures: []
- warnings: ['bad_rate_missing', 'trigger_rate_missing', 'auc_missing_or_undefined', 'balanced_accuracy_missing', 'validity_gate_missing_or_no_valid_for_interpretation']
