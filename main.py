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


  memid= voice_channel.voice_states.keys()
  memlist=list(memid)

  if a not in memlist:
    await ctx.send('Join M3W2 Lobby channel and resend the command..!')
    return
  
  if notm>len(memlist):
    await ctx.send('Specify No. of teams less than members..!')
    return
  
  random.shuffle(memlist)
  memlist= np.array_split(memlist, notm)
  for i in range(0,notm):
    chanT = 'M3W2 Team - '+str(i+1)
    chn = await ctx.guild.create_voice_channel(chanT, category=cat, user_limit=memlist[i].size)
    ids=memlist[i]
    for j in range(0,len(ids)):
      user = await ctx.guild.query_members(user_ids=int(ids[j]))
      await user[0].move_to(chn)


#Voice team deleter
@client.command()
async def over(ctx):

  ch=ctx.author.voice
  if ch == None:
    await ctx.send("User not in any voice channel..!")
    return  

  autca = ctx.author.voice.channel.category

  if "M3W2" in [y.name.upper() for y in ctx.author.roles]:
    for c in ctx.guild.voice_channels:
      if str(c).startswith('M3W2 Team - ') == False and c.category == autca:
        ch1 = c

    if ch1 == None:
      await ctx.send('No channel exist to move Members in this category..!')
      return
    
    for c in ctx.guild.voice_channels:
      if str(c).startswith('M3W2 Team - ') and c.category == autca:
       memid = c.voice_states.keys()
       memlist=list(memid)
       if len(memlist) > 0:
          user = await ctx.guild.query_members(user_ids=memlist)
          for user1 in user:
            await user1.move_to(ch1)
       await c.delete()
       return

  voice_main = discord.utils.get(ctx.guild.channels, name="M3W2 Lobby")

  if autca != voice_main.category:
    await ctx.send('You\'re not in M3W2 Teams category..!')
    return

  if voice_main == None:
    await ctx.send('M3W2 Lobby channel not available..!')
    return

  for c in ctx.guild.voice_channels:
    if str(c).startswith('M3W2 Team - ') and autca == voice_main.category:
      memid = c.voice_states.keys()
      memlist=list(memid)
      if len(memlist) > 0:
        user = await ctx.guild.query_members(user_ids=memlist)
        for user1 in user:
          await user1.move_to(voice_main)
      await c.delete()
      return

  
    


    


@client.command()
#@commands.has_role('RoleName')
async def cvteam(ctx,notm):
  ch=ctx.author.voice
  if ch==None:
    await ctx.send('Connect to voice channel..!' )
    return
  notm = int(notm)
  memlist=list()
  chn1=ctx.author.voice.channel
  memid= chn1.voice_states.keys()
  memlist=list(memid)

  if notm>len(memlist):
    await ctx.send('Specify No. of teams less than members..!')
    return

  for c in ctx.guild.voice_channels:
    if str(c).startswith('M3W2 Team - '):
      memid = c.voice_states.keys()
      memlist=list(memid)
      if len(memlist) == 0:
        await c.delete()
  
  random.shuffle(memlist)
  memlist= np.array_split(memlist, notm)
  for i in range(0,notm):
    chanT = 'M3W2 Team - '+str(i+1)
    chn = await ctx.guild.create_voice_channel(chanT, category=chn1.category, user_limit=memlist[i].size)
    ids=memlist[i]
    for j in range(0,len(ids)):
      user = await ctx.guild.query_members(user_ids=int(ids[j]))
      await user[0].move_to(chn)




#For ping
@client.command()
async def ping(ctx):
  await ctx.send(f'{round(client.latency*1000)} ms')

#Help Embed
@client.command(aliases=['Help','help','HELP'])
async def embed(ctx):

  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
    a = prefixes[str(ctx.guild.id)]

  gif=random.choice(gifs2)

  #### Create the initial embed object ####
  embed=discord.Embed(title="HELP", description="These are the list of commands used in this bot", color=0xad1457)

# Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=ctx.author.display_name,  icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url=gif)

  embed.add_field(name=f"{a}Help", value="Display all commands of this bot and it's uses", inline=False) 
  embed.add_field(name=f"{a}ping", value="Returns Ping of this bot", inline=True)
  embed.add_field(name=f"{a}changeprefix", value=f"Used to change prefix.\n Syntax: {a}changeprefix [your desired prefix]", inline=False)

  embed.set_footer(text="Thanks for using my Bot <3")

  await ctx.send(embed=embed)


client.run(os.environ['Token'])
