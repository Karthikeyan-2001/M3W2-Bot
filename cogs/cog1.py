import discord
from discord.ext import commands

class jk1(commands.cogs):

  def __init__(self,client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('We have logged in as {0.user}'.format(self.client))

  @commands.command()
  async def Hello(self,ctx):
    await ctx.send('Hii..!')

def setup(client):
  client.add_cog(jk1(client))