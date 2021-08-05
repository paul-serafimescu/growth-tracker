from django.test import RequestFactory
from django.utils import timezone
from tracker.models import Guild, DiscordUser
from tracker.views import ServerView
from .utils import route, ViewTest

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
      permissions='1234567890'
    )
    cls.payload = {
      'field_1': 'foo',
      'field_2': True,
      'field_3': 98.3,
      'field_4': 'bar',
      'field_5': 'baz',
    }

  @route('patch', '/servers/testing_guild_id', view=ServerView, logged_in=False)
  def test_1(self, response):
    self.assertEqual(response.status_code, 200)
    self.assertTrue(isinstance(response.content, (str, bytes)), f'response type invalid: {type(response.content)}')
    self.assertEqual(response.content.decode('utf-8') if isinstance(response.content, bytes) else response.content, 'testing...')
