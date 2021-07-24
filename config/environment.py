import dotenv
from pathlib import Path
from .exceptions import EnvNotFoundError

BASE_PATH = Path(__file__).resolve().parent.parent

if not (ENV := dotenv.dotenv_values(BASE_PATH / '.env')):
  raise EnvNotFoundError()
