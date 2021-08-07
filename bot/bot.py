import discord
from database import Database
from config.environment import ENV

class GrowthTracker(discord.Client):
  def __init__(self):
    self.database = Database()
    return super().__init__()

  async def on_ready(self) -> None:
    print(await self.database.fetch_guild_snapshots(await self.database.fetch_guild(pk=1)))
    #print(f'{self.user} is running...', await self.database.fetch_all_guilds())

  async def on_member_join(self, member: discord.Member) -> None:
    ...

  async def on_message(self, message: discord.Message) -> None:
    ...

  def run_bot(self) -> None:
    self.run(ENV.get('BOT_TOKEN'))

