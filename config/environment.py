import dotenv
from pathlib import Path
from .exceptions import EnvNotFoundError

BASE_PATH = Path(__file__).resolve().parent.parent

if not (ENV := dotenv.dotenv_values(BASE_PATH / '.env')):
  raise EnvNotFoundError()

DISCORD_API_ROOT = 'https://discord.com/api/v8/'

DISCORD_OAUTH_ROOT = DISCORD_API_ROOT + 'oauth2/'
