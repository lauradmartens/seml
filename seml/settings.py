import imp
from munch import munchify
from pathlib import Path

from seml.utils import merge_dicts

__all__ = ("SETTINGS",)

SETTINGS = munchify(
    {
        # Location of user-specific settings.py file containing a SETTINGS dict.
        # With this dict you can change anything that is set here, conveniently from your home directory.
        # Default: $HOME/.config/seml/settings.py
        "USER_SETTINGS_PATH": Path.home() / ".config/seml/settings.py",

        "DATABASE": {
            # location of the MongoDB config. Default: $HOME/.config/seml/monogdb.config
            "MONGODB_CONFIG_PATH": Path.home() / ".config/seml/mongodb.config"
        },
        "SLURM_DEFAULT": {
            'experiments_per_job': 1,
            'sbatch_options': {
                'time': '0-08:00',
                'nodes': 1,
                'cpus-per-task': 1,
                'mem': 8000,
                },
        },
        "SBATCH_OPTIONS_TEMPLATES": {
            # This is a special template used for `seml jupyter`
            "JUPYTER": {
                'cpus-per-task': 2,
                'mem': 16000,
                'gres': "gpu:1",
                'qos': 'interactive',
                'job-name': 'jupyter',
                'output': 'jupyter-%j.out',
            },
            # Extend this with your custom templates.
            "GPU": {
                'cpus-per-task': 2,
                'mem': 16000,
                'gres': "gpu:1",
            },
        },
        "STATES": {
            "STAGED": ["STAGED", "QUEUED"],  # QUEUED for backward compatibility
            "PENDING": ["PENDING"],
            "RUNNING": ["RUNNING"],
            "FAILED": ["FAILED"],
            "KILLED": ["KILLED"],
            "INTERRUPTED": ["INTERRUPTED"],
            "COMPLETED": ["COMPLETED"],
        },
        "SLURM_STATES": {
            "PENDING": ["PENDING", "CONFIGURING", "REQUEUE_FED", "REQUEUE_HOLD", "REQUEUED", "RESIZING"],
            "RUNNING": ["RUNNING", "SUSPENDED"],
        },
        "VALID_SEML_CONFIG_VALUES": ['executable', 'name', 'output_dir',
                                     'conda_environment', 'project_root_dir'],
        "VALID_SLURM_CONFIG_VALUES": ['experiments_per_job', 'max_jobs_per_batch',
                                      'sbatch_options_template', 'sbatch_options'],

        "OBSERVERS": {
            "NEPTUNE": {
                "AUTH_TOKEN": "YOUR_AUTH_TOKEN",
            },
            "SLACK": {
                "WEBHOOK": "YOUR_WEBHOOK",
            },
            "MATTERMOST": {
                "WEBHOOK": "YOUR_WEBHOOK",
                "DEFAULT_CHANNEL": "YOUR_DEFAULT_CHANNEL",
            }
        },
    },
)

# Load user settings
if SETTINGS.USER_SETTINGS_PATH.exists():
    user_settings_source = imp.load_source('SETTINGS', str(SETTINGS.USER_SETTINGS_PATH))
    SETTINGS = munchify(merge_dicts(SETTINGS, user_settings_source.SETTINGS))
