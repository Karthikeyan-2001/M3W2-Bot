import discord
import os
import numpy as np
import json
import random
from discord.ext import commands, tasks
from keep_alive import keep_alive
from itertools import cycle
from gamename import games, gifs2

#Prefix
def get_prefix(client,message):
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)

  return prefixes[str(message.guild.id)]

#Initializing Client
client = commands.Bot(command_prefix = get_prefix, help_command=None)

status=cycle(games)

#Prefix on server join
@client.event
async def on_guild_join(guild):
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)

  prefixes[str(guild.id)] = '+'

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes,f, indent=4)

#Prefix delete on leaving server
@client.event
async def on_guild_remove(guild):
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)

  prefixes.pop(str(guild.id))

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes,f, indent=4)


#Client ready
@client.event
async def on_ready():
  change_status.start()
  print('We have logged in as {0.user}'.format(client))


#Change Status
@tasks.loop(minutes=2)
async def change_status():
  await client.change_presence(activity = discord.Game(next(status)))

#Change Prefix
@client.command()
async def changeprefix(ctx, prefix):
  with open('prefixes.json','r') as f:
    prefixes=json.load(f)

  prefixes[str(ctx.guild.id)] = prefix

  with open('prefixes.json', 'w') as f:
    json.dump(prefixes,f, indent=4)

  await ctx.send(f'prefix changed to {prefix}')

#Voice team maker
@client.command()
async def vteam(ctx,notm):

  j,k=0,0
  notm = int(notm)
  cate1 = 'M3W2 Teams'
  chan1 = 'M3W2 Lobby'
  chn=[]
  memlist=list()
  a=ctx.author.id
  for i in ctx.guild.categories:
    if cate1 == i.name:
      k=1
      break
  if k==0:
    await ctx.guild.create_category('M3W2 Teams')
    await ctx.send('Created channel successfully..!')

  for i in ctx.guild.channels:
    if chan1== i.name:
      j=1
      break
  cat = discord.utils.get(ctx.guild.categories, name='M3W2 Teams')
  if j==0:
    await ctx.guild.create_voice_channel(chan1, category=cat, user_limit=None)
    await ctx.send('Join M3W2 Lobby channel and resend the command..!')
    return

  voice_channel = discord.utils.get(ctx.guild.channels, name="M3W2 Lobby")

  await voice_channel.edit(category=cat)

  for c in ctx.guild.voice_channels:
    if str(c).startswith('M3W2 Team - '):
      memid = c.voice_states.keys()
      memlist=list(memid)
      if len(memlist) == 0:
        await c.delete()





#Voice team maker
@client.command()
#@commands.has_role('M3W2')
async def cvteam(ctx):
  chan1 = ctx.author.voice
  if chan1==None:
    await ctx.send("PLEASE JOIN A CHANNEL AND ENTER COMMAND..!")
    return
  memlist=list()
  channel = ctx.author.voice.channel
  for c in ctx.guild.voice_channels:
    if str(c).startswith('M3W2 Team - '):
      memid = c.voice_states.keys()
      memlist=list(memid)
      if len(memlist) == 0:
        await c.delete()



  







#Voice team deleter
@client.command()
async def over(ctx):
  voice_main = discord.utils.get(ctx.guild.channels, name="M3W2 Lobby")
  if voice_main == None:
    await ctx.send('M3W2 Lobby channel not available..!')
    return

  for c in ctx.guild.voice_channels:
    if str(c).startswith('M3W2 Team - '):
      memid = c.voice_states.keys()
      memlist=list(memid)
      if len(memlist) > 0:
        user = await ctx.guild.query_members(user_ids=memlist)
        for user1 in user:
          await user1.move_to(voice_main)
      await c.delete()



#For ping
@client.command()
async def ping(ctx):
  await ctx.send(f'{round(client.latency*1000)} ms')

#Help Embed
@client.command(aliases=['help','HELP','Help-1'])
async def embedhelp(ctx):

  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
    a = prefixes[str(ctx.guild.id)]

  gif=random.choice(gifs2)

  #### Create the initial embed object ####
  embed=discord.Embed(title="HELP", description="These are the list of commands used in this bot", color=0xad1457)

# Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=ctx.author.display_name,  icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url=gif)

  embed.add_field(name=f"{a}help", value="Display all commands of this bot and it's uses", inline=True) 

  embed.add_field(name=f"{a}ping", value="Returns Ping of this bot", inline=True)

  embed.add_field(name=f"{a}changeprefix", value=f"Used to change prefix.\n Syntax: {a}changeprefix [your desired prefix]", inline=False)

  embed.add_field(name=f"{a}Help-2 or {a}help vteam", value=f"Information about {a}vteam command", inline=True)

  embed.add_field(name=f"{a}Help-3 or {a}help over", value=f"Information about {a}over command", inline=True)

  embed.set_footer(text="\nThanks for using my Bot <3 \n Page-1/3")

  await ctx.send(embed=embed)


#Help Embed Vteam
@client.command(aliases=['Help vteam','Help-2'])
async def vteamembed(ctx):

  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
    a = prefixes[str(ctx.guild.id)]

  gif=random.choice(gifs2)

  #### Create the initial embed object ####
  embed=discord.Embed(title="VOICE TEAMER", description="This command is used for teaming up the members in M3W2 Lobby to desired number of teams randomly.\nThis command create required number of teams and move the members randomly to their respective teams.", color=0x2ecc71)

# Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=ctx.author.display_name,  icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url=gif)

  embed.add_field(name="SYNTAX", value=f"{a}vteam [number of team]", inline=True) 

  embed.add_field(name="EXAMPLE", value=f"If you want two team, syntax is {a}vteam 2 ", inline=True)

  embed.add_field(name="INSTRUCTIONS", value=f"1. Create M3W2 Category and channel, enter command {a}vteam 1 \n2. If this command doesn't summon M3W2 Lobby channel, delete the category and retype the command.\n3. please delete M3W2 Team - x channel if not needed by {a}over command. if the M3W2 Team - x channel exist, delete manually. \n4. Enter number of teams less than or equal to number of members in the M3W2 Lobby channel. \n5. You and all members must be in M3W2 Lobby channel to summon and seperate teams", inline=False)

  embed.add_field(name=f"{a}Help-1 or {a}help", value=f"Information about all commands", inline=False)

  embed.add_field(name=f"{a}Help-3 or {a}Help over", value=f"Information about {a}over command", inline=True)

  embed.set_footer(text="\nThanks for using my Bot <3 \n Page-2/3")

  await ctx.send(embed=embed)


#Help Embed
@client.command(aliases=['Help over','Help-3'])
async def embedover(ctx):

  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
    a = prefixes[str(ctx.guild.id)]

  gif=random.choice(gifs2)

  #### Create the initial embed object ####
  embed=discord.Embed(title="OVER", description="If you finished the game, use this command to move all the members from all teams to M3W2 Lobby and delete all teams", color=0xf1c40f)

# Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=ctx.author.display_name,  icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url=gif)

  embed.add_field(name="SYNTAX", value=f"{a}over", inline=False) 

  embed.add_field(name="EXAMPLE", value=f"If your game is over and want all members back to lobby, use command {a}over ", inline=False)

  embed.add_field(name=f"{a}Help-1 or {a}help", value=f"Information about all commands", inline=False)

  embed.add_field(name=f"{a}Help-2 or {a}Help vteam", value=f"Information about {a}vteam command", inline=False)

  embed.add_field(name=f"{a}Help-3 or {a}Help over", value=f"Information about {a}over command", inline=False)

  embed.set_footer(text="\nThanks for using my Bot <3 \n Page-3/3")

  await ctx.send(embed=embed)




keep_alive()
client.run(os.environ['Token'])
