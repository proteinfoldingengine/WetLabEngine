# V312_LAB_CONTEXT_TEST — Scientific Execution Validation

## Overall Status
pass

## Interpretation Allowed
True

## Selected Regime Present
False

## Row Counts
- valid_row_count: 2
- total_row_count: 152
- valid_controller_row_count: 0
- total_controller_row_count: 0

## Failures
- None

## Warnings
- No selected/chosen regime found.

## Row Checks

### all_candidates_0
- path: all_candidates[0]
- row_interpretable: False
- bad_rate: 0.125
- trigger_rate: 0.5
- auc: 0.7657004022172739
- balanced_accuracy: 0.875
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 1.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_1
- path: all_candidates[1]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 0.875
- auc: 0.7260812751379881
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_2
- path: all_candidates[2]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 1.0
- auc: 0.673273758238148
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_3
- path: all_candidates[3]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.6104566385477967
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_4
- path: all_candidates[4]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5391719159083757
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_5
- path: all_candidates[5]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4966681090327391
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_6
- path: all_candidates[6]
- row_interpretable: False
- bad_rate: 0.375
- trigger_rate: 1.0
- auc: 0.7124647093238817
- balanced_accuracy: 0.625
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 3.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_7
- path: all_candidates[7]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 1.0
- auc: 0.6457187528556939
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_8
- path: all_candidates[8]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.6065128670920688
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_9
- path: all_candidates[9]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5401921516949841
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_10
- path: all_candidates[10]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4664778707382587
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_11
- path: all_candidates[11]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4258097228259043
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_12
- path: all_candidates[12]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 0.6308372000257458
- balanced_accuracy: 0.125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_13
- path: all_candidates[13]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5472312347174693
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_14
- path: all_candidates[14]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5271505066780195
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_15
- path: all_candidates[15]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4343692494780402
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_16
- path: all_candidates[16]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.37022762372071216
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_17
- path: all_candidates[17]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3545167620544121
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_18
- path: all_candidates[18]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5423166155100082
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_19
- path: all_candidates[19]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4904056676109591
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_20
- path: all_candidates[20]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4418972805933089
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_21
- path: all_candidates[21]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3734708892050006
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_22
- path: all_candidates[22]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.33733920629681385
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_23
- path: all_candidates[23]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2985079571599487
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_24
- path: all_candidates[24]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5047621705224785
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_25
- path: all_candidates[25]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4374631399384912
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_26
- path: all_candidates[26]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.35499569109993956
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_27
- path: all_candidates[27]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.31712845232237263
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_28
- path: all_candidates[28]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.21706838637990783
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_29
- path: all_candidates[29]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.21270364566234304
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_30
- path: all_candidates[30]
- row_interpretable: False
- bad_rate: 0.75
- trigger_rate: 1.0
- auc: 0.6495211351528619
- balanced_accuracy: 0.25
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 6.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_31
- path: all_candidates[31]
- row_interpretable: False
- bad_rate: 0.875
- trigger_rate: 1.0
- auc: 0.6023879379052879
- balanced_accuracy: 0.125
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 7.0
- valid_for_interpretation: False
- failures: ['trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_32
- path: all_candidates[32]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5607948116817851
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_33
- path: all_candidates[33]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4849288456828592
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_34
- path: all_candidates[34]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4346500341672971
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_35
- path: all_candidates[35]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3928860915089487
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_36
- path: all_candidates[36]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.6014944636074488
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_37
- path: all_candidates[37]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5477349171864808
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_38
- path: all_candidates[38]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.47965474683863346
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_39
- path: all_candidates[39]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.411525574846793
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_40
- path: all_candidates[40]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.36818962805823563
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_41
- path: all_candidates[41]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.30590437979758905
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_42
- path: all_candidates[42]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5116686171697598
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_43
- path: all_candidates[43]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.46498616966945694
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_44
- path: all_candidates[44]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.40762540269941244
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_45
- path: all_candidates[45]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.32507061677382726
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_46
- path: all_candidates[46]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.27699072923621554
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_47
- path: all_candidates[47]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2668192410277129
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_48
- path: all_candidates[48]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.43262359059562805
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_49
- path: all_candidates[49]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3946806831520167
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_50
- path: all_candidates[50]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3424269163270946
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_51
- path: all_candidates[51]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.27395418741023714
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_52
- path: all_candidates[52]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.22130304185785643
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_53
- path: all_candidates[53]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.22602780834847597
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_54
- path: all_candidates[54]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.36789791239615044
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_55
- path: all_candidates[55]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.30595794181852615
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_56
- path: all_candidates[56]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2951152640542472
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_57
- path: all_candidates[57]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.23676617445928622
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_58
- path: all_candidates[58]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.17944256884677623
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_59
- path: all_candidates[59]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.15052474646913094
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_60
- path: all_candidates[60]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.5255818477944726
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_61
- path: all_candidates[61]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4749548905691045
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_62
- path: all_candidates[62]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4041794162651096
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_63
- path: all_candidates[63]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3551860400949066
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_64
- path: all_candidates[64]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3097026254751082
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_65
- path: all_candidates[65]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2687372918082277
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_66
- path: all_candidates[66]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4528412107183744
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_67
- path: all_candidates[67]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.4127577007691475
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_68
- path: all_candidates[68]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3407375749909621
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_69
- path: all_candidates[69]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.27527398955654264
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_70
- path: all_candidates[70]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2532697339046463
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_71
- path: all_candidates[71]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.20483516431340865
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_72
- path: all_candidates[72]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3878709557108897
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_73
- path: all_candidates[73]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.348276976147819
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_74
- path: all_candidates[74]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2652458282790961
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_75
- path: all_candidates[75]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.20036765374437007
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_76
- path: all_candidates[76]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.19085285279797753
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_77
- path: all_candidates[77]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.14182051999803905
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_78
- path: all_candidates[78]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.31536250888098366
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_79
- path: all_candidates[79]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.25502215506515324
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_80
- path: all_candidates[80]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.22308698666426002
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_81
- path: all_candidates[81]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.17177911649514868
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_82
- path: all_candidates[82]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1481653300822711
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_83
- path: all_candidates[83]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1314849289257369
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_84
- path: all_candidates[84]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.26986383863450425
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_85
- path: all_candidates[85]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2076012883806154
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_86
- path: all_candidates[86]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.17486154282638858
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_87
- path: all_candidates[87]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.14135252123217174
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_88
- path: all_candidates[88]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1306638262165439
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_89
- path: all_candidates[89]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.09326768943938302
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_90
- path: all_candidates[90]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3858042795611827
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_91
- path: all_candidates[91]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3472634593228318
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_92
- path: all_candidates[92]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2763402439334462
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_93
- path: all_candidates[93]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2616467274969466
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_94
- path: all_candidates[94]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1927688524325397
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_95
- path: all_candidates[95]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1731057130653902
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_96
- path: all_candidates[96]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.3207457341428679
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_97
- path: all_candidates[97]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.27489395000441724
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_98
- path: all_candidates[98]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.23927008512633804
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_99
- path: all_candidates[99]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.19220697067942447
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_100
- path: all_candidates[100]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.15611740276139904
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_101
- path: all_candidates[101]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1258524415857008
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_102
- path: all_candidates[102]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.27361470816108585
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_103
- path: all_candidates[103]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.21708137399553723
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_104
- path: all_candidates[104]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.16482744431938162
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_105
- path: all_candidates[105]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1454773120300186
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_106
- path: all_candidates[106]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.10553900698746238
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_107
- path: all_candidates[107]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.10416467864112114
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_108
- path: all_candidates[108]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.19757167632798522
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_109
- path: all_candidates[109]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1930515193855877
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_110
- path: all_candidates[110]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1572730051155623
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_111
- path: all_candidates[111]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.12516489902810635
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_112
- path: all_candidates[112]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.08223735200720765
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_113
- path: all_candidates[113]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.08654292130855538
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_114
- path: all_candidates[114]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.17617981888955664
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_115
- path: all_candidates[115]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.1410488576732809
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_116
- path: all_candidates[116]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.11349361233729252
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_117
- path: all_candidates[117]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.08399839580449762
- balanced_accuracy: 0.0
- horizon_area: 0.0001454401329822239
- horizon_width: 0.015625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_118
- path: all_candidates[118]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.07278999849231839
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_119
- path: all_candidates[119]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.06395909662633577
- balanced_accuracy: 0.0
- horizon_area: 6.75916320822497e-05
- horizon_width: 0.015625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_120
- path: all_candidates[120]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.2623244524881043
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_121
- path: all_candidates[121]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.218418858107882
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_122
- path: all_candidates[122]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.188546604912048
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_123
- path: all_candidates[123]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.15879879307934971
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_124
- path: all_candidates[124]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.12629006084727734
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_125
- path: all_candidates[125]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.09816348808128009
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_126
- path: all_candidates[126]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.20469675922391664
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_127
- path: all_candidates[127]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.17134508531499346
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_128
- path: all_candidates[128]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.14671501306545356
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_129
- path: all_candidates[129]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.11859198918020708
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_130
- path: all_candidates[130]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.09233761448773159
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_131
- path: all_candidates[131]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.06924341832661965
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_132
- path: all_candidates[132]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.16497901758938444
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_133
- path: all_candidates[133]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.13397257451285655
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_134
- path: all_candidates[134]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.09909476505210252
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_135
- path: all_candidates[135]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.09010600794653977
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_136
- path: all_candidates[136]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.06799051133378596
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_137
- path: all_candidates[137]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.05439546916659146
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_138
- path: all_candidates[138]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.13459751385862762
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_139
- path: all_candidates[139]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.11419499482424586
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_140
- path: all_candidates[140]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.08619609036219988
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_141
- path: all_candidates[141]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.07497825926135028
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_142
- path: all_candidates[142]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.05857494420010364
- balanced_accuracy: 0.0
- horizon_area: 0.00032052501488214575
- horizon_width: 0.015625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_143
- path: all_candidates[143]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.044025700425275004
- balanced_accuracy: 0.0
- horizon_area: 0.0011914896748888423
- horizon_width: 0.046875
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_144
- path: all_candidates[144]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.09198201950924546
- balanced_accuracy: 0.0
- horizon_area: 3.715279517868368e-05
- horizon_width: 0.015625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_145
- path: all_candidates[145]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.08012576762432566
- balanced_accuracy: 0.0
- horizon_area: 0.0
- horizon_width: 0.0
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: ['horizon_metrics_zero']

### all_candidates_146
- path: all_candidates[146]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.05703296334174069
- balanced_accuracy: 0.0
- horizon_area: 2.680582879742866e-05
- horizon_width: 0.015625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_147
- path: all_candidates[147]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.05077468136619085
- balanced_accuracy: 0.0
- horizon_area: 0.0002737902730126781
- horizon_width: 0.03125
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_148
- path: all_candidates[148]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.04275668462826849
- balanced_accuracy: 0.0
- horizon_area: 0.0011911658857232444
- horizon_width: 0.015625
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### all_candidates_149
- path: all_candidates[149]
- row_interpretable: False
- bad_rate: 1.0
- trigger_rate: 1.0
- auc: 0.03687348773988462
- balanced_accuracy: 0.0
- horizon_area: 0.0005518441033783832
- horizon_width: 0.03125
- score_var: None
- phase_counts_bad: 8.0
- valid_for_interpretation: False
- failures: ['bad_rate_saturated_one', 'trigger_rate_saturated_one', 'validity_gate_false']
- warnings: []

### controllers
- path: controllers
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
