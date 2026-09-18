# config_loader.py
#
# Module for loading and managing experiment configurations from YAML files.

import yaml
import copy
import os

def load_config(config_path: str, base_constants: dict) -> dict:
    """
    Loads a YAML config file and merges it with the base physics constants.
    """
    print(f"--- Loading configuration from: {config_path} ---")
    if not os.path.exists(config_path):
        print(f"FATAL: Configuration file not found at {config_path}")
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    config = copy.deepcopy(base_constants)

    with open(config_path, 'r') as f:
        try:
            experiment_config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"FATAL: Error parsing YAML file: {e}")
            raise

    def _recursive_update(base, update):
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = _recursive_update(base.get(key, {}), value)
            else:
                base[key] = value
        return base

    config = _recursive_update(config, experiment_config)
    
    # --- Flatten nested keys for easier access ---
    if 'learning_rates' in config:
        config['LEARNING_RATE_COORDS'] = config['learning_rates']['coords']
        config['LEARNING_RATE_GAMMA'] = config['learning_rates']['gamma']

    if 'tunable_forces' in config:
        for key, value in config['tunable_forces'].items():
            config[key] = value
    
    if 'coherence_well' in config:
        for key, value in config['coherence_well'].items():
            config[key] = value
            
    # ✅ Patch 623.0: Flatten torsional penalty params
    if 'torsional_penalty_params' in config:
        for key, value in config['torsional_penalty_params'].items():
            config[key] = value

    print("Configuration loaded and merged successfully.")
    return config
