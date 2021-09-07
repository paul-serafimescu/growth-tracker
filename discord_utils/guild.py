from . import RequestModule, raise_on_error, Any
from config.environment import DISCORD_API_ROOT

class GuildManager(RequestModule):
  def __init__(self, token: str, token_type: str = 'Bearer'):
    super().__init__(token, token_type)

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} {self.token}>'

  @raise_on_error
  def get_user_guilds(self) -> list[dict[str, Any]]:
    return self.get('{}users/@me/guilds'.format(DISCORD_API_ROOT))

  @raise_on_error
  def fetch_guild(self, id: str) -> dict[str, Any]:
    return self.get('{}guilds/{}'.format(DISCORD_API_ROOT, id))
