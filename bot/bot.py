import discord

class GrowthTracker(discord.Client):
  async def on_ready(self) -> None:
    print(f'{self.user} is running...')

  async def on_member_join(self, member: discord.Member) -> None:
    pass

