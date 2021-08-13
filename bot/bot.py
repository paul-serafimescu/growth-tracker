import discord
from database import Database
from database.base import Guild
from config.environment import ENV
from typing import Union

class GrowthTracker(discord.Client):
  def __init__(self):
    self.database = Database()
    super().__init__(intents=discord.Intents.all())
    return self.run()

  def __corresponding_discord_guild(self, guild_id: str) -> Union[discord.Guild, None]:
    for guild in self.guilds:
      if str(guild.id) == guild_id:
        return guild
    return None

  async def __corresponding_db_guild(self, guild_id: int) -> Union[Guild, None]:
    return await self.database.fetch_guild(guild_id=str(guild_id))

  async def on_ready(self) -> None:
    for existing_guild in (await self.database.convert_guild_objects(self.guilds)):
      existing_guild.members = self.__corresponding_discord_guild(existing_guild.guild_id).member_count
      await existing_guild.async_save()
    print(f'{self.user} is running...')

  async def on_member_join(self, member: discord.Member) -> None:
    await self.database.add_guild_member(str(member.guild.id))

  async def on_guild_join(self, guild: discord.Guild) -> None:
    if (_guild := await self.__corresponding_db_guild(guild)) is None:
      return await Guild(
        name=guild.name,
        guild_id=str(guild.id),
        icon=guild.icon,
        permissions='143985544769', # TODO: figure out why I included permissions
        members=guild.member_count,
      ).async_save()
    _guild.members = guild.member_count
    await _guild.async_save()

  async def on_member_remove(self, member: discord.Member) -> None:
    await self.database.remove_guild_member(str(member.guild.id))

  def run(self) -> None:
    super().run(ENV.get('BOT_TOKEN'))
