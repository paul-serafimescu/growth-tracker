from . import RequestModule, raise_on_error, Any
from config.environment import DISCORD_API_ROOT

class UserManager(RequestModule):
  def __init__(self, token: str, token_type: str = 'Bearer'):
    super().__init__(token, token_type)

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} {self.token}>'

  @raise_on_error
  def get_current_user(self) -> list[dict[str, Any]]:
    return self.get('{}users/@me'.format(DISCORD_API_ROOT))

  @raise_on_error
  def fetch_user(self, id: str) -> dict[str, Any]:
    return self.get('{}users/{}'.format(DISCORD_API_ROOT, id))
