import yaml
import dotenv
from pathlib import Path

main_folder = Path("$HOME/Desktop/telegram-bot")
config_dir = Path(main_folder / "config")

# load yaml config
with open(main_folder / config_dir / "config.yml", 'r') as f:
    config_yaml = yaml.safe_load(f)

# load .env config
config_env = dotenv.dotenv_values(config_dir / "config.env")

# config parameters
telegram_token = config_yaml["telegram_token"]
gemini_api = config_yaml["gemini_api"]
chatgpt_api = config_yaml["chatgpt_api"]
chatgpt_model = config_yaml["chatgpt_model"]
allowed_telegram_usernames = config_yaml["allowed_telegram_usernames"]
new_dialog_timeout = config_yaml["new_dialog_timeout"]
enable_message_streaming = config_yaml.get("enable_message_streaming", True)
n_chat_modes_per_page = config_yaml.get("n_chat_modes_per_page", 5)
