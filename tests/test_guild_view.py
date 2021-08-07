from django.test import RequestFactory
from django.utils import timezone
from tracker.models import Guild, DiscordUser
from tracker.views import ServerView
from config.environment import BOT_CLIENT_TOKEN
from .utils import route, ViewTest

PAYLOAD = {
  'field_1': 'foo',
  'field_2': True,
  'field_3': 98.3,
  'field_4': 'bar',
  'field_5': 'baz',
}

class ServerViewTest(ViewTest):
  @classmethod
  def setUpTestData(cls) -> None:
    cls.factory = RequestFactory()
    cls.user = DiscordUser.create_user(
      access_token='rdtyruvh76f5ty3c564sertxycu',
      token_type=DiscordUser.TokenType.BEARER,
      expiration=timezone.now() + timezone.timedelta(days=1),
      refresh_token='tfyugtdr64s5s6rxyct78u'
    )
    cls.guild = Guild.create_guild(
      name='My Server',
      guild_id='testing_guild_id',
      icon='dtfcygvuhjbkk',
      permissions='1234567890',
      members=None
    )
    cls.payload = PAYLOAD

  @route('patch', '/servers/testing_guild_id', view=ServerView, headers={ 'Authorization': BOT_CLIENT_TOKEN }, data=PAYLOAD, logged_in=True)
  def test_1(self, response):
    self.assertEqual(response.status_code, 200)
    self.assertTrue(isinstance(response.content, (str, bytes)), f'response type invalid: {type(response.content)}')
