from typing import Union, Any
from . import raise_on_error, ResponseError
from config.environment import (
  DISCORD_OAUTH_ROOT,
  ENV,
)
from config.exceptions import EnvKeyNotFoundError
import requests

class Refresh:
  def __init__(self, refresh_token: str, _: Union[str, None] = None):
    self.refresh_token = refresh_token

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} {self.refresh_token}>'

  @raise_on_error
  def __call__(self) -> dict[str, Any]:
    if (client_id := ENV.get('CLIENT_ID')) is None:
      raise EnvKeyNotFoundError('CLIENT_ID')
    if (client_secret := ENV.get('CLIENT_SECRET')) is None:
      raise EnvKeyNotFoundError('CLIENT_SECRET')
    data = {
      'client_id': client_id,
      'client_secret': client_secret,
      'grant_type': 'refresh_token',
      'refresh_token': self.refresh_token
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    return requests.post(f'{DISCORD_OAUTH_ROOT}token', data=data, headers=headers).json()
