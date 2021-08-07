import dotenv
from pathlib import Path
from .exceptions import EnvKeyNotFoundError, EnvNotFoundError

BASE_PATH = Path(__file__).resolve().parent.parent

if not (ENV := dotenv.dotenv_values(BASE_PATH / '.env')):
  raise EnvNotFoundError()

if not (BOT_CLIENT_TOKEN := ENV.get((key := 'BOT_CLIENT_TOKEN'))):
  raise EnvKeyNotFoundError(key)

DISCORD_API_ROOT = 'https://discord.com/api/v8/'

DISCORD_OAUTH_ROOT = DISCORD_API_ROOT + 'oauth2/'

DATABASE_PATH = BASE_PATH / 'db.sqlite3'
