from pathlib import Path


ROOT = Path(__file__).absolute().parent
SETTINGS_DIR = ROOT / "settings"
PRESETS_SETTINGS_DIR = SETTINGS_DIR / "presets"
DEFAULT_SETTINGS_PATH = SETTINGS_DIR / "defaults.json"

DEFAULT_WORKSPACE = "cfport_package"
DEFAULT_CONFIG_FILE = "cfport.json"
