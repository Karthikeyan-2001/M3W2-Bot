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
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


#Initializing Client
client = commands.Bot(command_prefix=get_prefix, help_command=None)

status = cycle(games)


#Prefix on server join
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '+'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(
                'Hey..! Thanks for adding me <3 \n Initial prefix is "+", type +help for more commands..!'
            )
        break


#Prefix delete on leaving server
@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


#Client ready
@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))


#Change Status
@tasks.loop(minutes=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


#Change Prefix
@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'prefix changed to {prefix}')


#Voice team maker
@client.command()
async def vteam(ctx, notm):

    ch = ctx.author.voice
    if ch == None:
        await ctx.send('Connect to voice channel..!')
        return
    chnw = ctx.author.voice.channel
    if str(chnw).startswith('M3W2 Team - '):
        await ctx.send(
            'You can\'t use this command in Team voice channel, use "over" command instead..!'
        )
        return

    isadmin = False

    if "M3W2" in [y.name.upper() for y in ctx.author.roles]:
        isadmin = True

    j, k = 0, 0
    notm = int(notm)
    cate1 = 'M3W2 Teams'
    chan1 = 'M3W2 Lobby'
    chn = []
    memlist = list()

    for c in ctx.guild.voice_channels:
        if str(c).startswith('M3W2 Team - '):
            memid = c.voice_states.keys()
            memlist = list(memid)
            if len(memlist) == 0:
                await c.delete()

    a = ctx.author.id
    for i in ctx.guild.categories:
        if cate1 == i.name:
            k = 1
            break
    if k == 0:
        await ctx.guild.create_category('M3W2 Teams')
        await ctx.send('Created channel successfully..!')

    for i in ctx.guild.channels:
        if chan1 == i.name:
            j = 1
            break
    cat = discord.utils.get(ctx.guild.categories, name='M3W2 Teams')
    if j == 0:
        await ctx.guild.create_voice_channel(chan1,
                                             category=cat,
                                             user_limit=None)
        if isadmin == False:
            await ctx.send('Join M3W2 Lobby channel and resend the command..!')
            return

    voice_channel = discord.utils.get(ctx.guild.channels, name="M3W2 Lobby")

    await voice_channel.edit(category=cat)

    ch1 = ctx.author.voice.channel

    if isadmin:
        memid = ch1.voice_states.keys()
        cat = ctx.author.voice.channel.category
    else:
        memid = voice_channel.voice_states.keys()

    memlist = list(memid)

    if a not in memlist and not isadmin:
        await ctx.send(
            'Join M3W2 Lobby channel and resend the command or you don\'t have ..! M3W2 Role..!'
        )
        return

    if notm > len(memlist):
        await ctx.send('Specify No. of teams less than members..!')
        return

    random.shuffle(memlist)
    memlist = np.array_split(memlist, notm)
    for i in range(0, notm):
        chanT = 'M3W2 Team - ' + str(i + 1)
        chn = await ctx.guild.create_voice_channel(chanT,
                                                   category=cat,
                                                   user_limit=memlist[i].size)
        ids = memlist[i]
        for j in range(0, len(ids)):
            user = await ctx.guild.query_members(user_ids=int(ids[j]))
            await user[0].move_to(chn)


#Voice team deleter
@client.command()
async def over(ctx):

    ch = ctx.author.voice
    if ch == None:
        await ctx.send("User not in any voice channel..!")
        return

    autca = ctx.author.voice.channel.category
    voice_main = discord.utils.get(ctx.guild.channels, name="M3W2 Lobby")

    if "M3W2" in [y.name.upper()
                  for y in ctx.author.roles] and autca != voice_main.category:
        for c in ctx.guild.voice_channels:
            if str(c).startswith(
                    'M3W2 Team - ') == False and c.category == autca:
                ch1 = c
                break

        if ch1 == None:
            await ctx.send(
                'No channel exist to move Members in this category..!')
            return

        for c in ctx.guild.voice_channels:
            if str(c).startswith(
                    'M3W2 Team - ') and c.category == ch1.category:
                memid = c.voice_states.keys()
                memlist = list(memid)
                if len(memlist) > 0:
                    user = await ctx.guild.query_members(user_ids=memlist)
                    for user1 in user:
                        await user1.move_to(ch1)
                await c.delete()
        return

    if autca != voice_main.category:
        await ctx.send('You\'re not in M3W2 Teams category..!')
        return

    if voice_main == None:
        await ctx.send('M3W2 Lobby channel not available..!')
        return

    for c in ctx.guild.voice_channels:
        if str(c).startswith('M3W2 Team - ') and autca == voice_main.category:
            memid = c.voice_states.keys()
            memlist = list(memid)
            if len(memlist) > 0:
                user = await ctx.guild.query_members(user_ids=memlist)
                for user1 in user:
                    await user1.move_to(voice_main)
            await c.delete()


@client.event
async def on_command_error(ctx, error):
    """A global error handler cog."""

    if isinstance(error, commands.CommandNotFound):
        return  # Return because we don't want to show an error for every command not found
    elif isinstance(error, commands.CommandOnCooldown):
        message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
    elif isinstance(error, commands.MissingPermissions):
        message = "You are missing the required permissions to run this command!"
    elif isinstance(error, commands.UserInputError):
        message = "Something about your input was wrong, please check your input and try again!"
    else:
        message = "Oh no! Something went wrong while running the command!"
    await ctx.send(message, delete_after=5)
    await ctx.message.delete(delay=5)


#For ping
@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} ms')


#Help Embed
@client.command(aliases=['help','HELP', 'Help-1'])
async def embed(ctx):

  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
    a = prefixes[str(ctx.guild.id)]

  gif=random.choice(gifs2)

  embed=discord.Embed(title="HELP", description="These are the list of commands used in this bot", color=0xad1457)
# Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=ctx.author.display_name,  icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url=gif)
  embed.add_field(name=f"{a}Help", value="Display all commands of this bot and it's uses", inline=False) 
  embed.add_field(name=f"{a}ping", value="Returns Ping of this bot", inline=True)
  embed.add_field(name=f"{a}changeprefix", value=f"Used to change prefix.\n Syntax: {a}changeprefix [your desired prefix]", inline=False)

  embed.add_field(name=f"{a}Help-2 or {a}Helpvteam", value=f"Information about {a}vteam command", inline=True)

  embed.add_field(name=f"{a}Help-3 or {a}Helpover", value=f"Information about {a}over command", inline=True)

  embed.set_footer(text="\nThanks for using my Bot <3 \n Page-1/3")
  await ctx.send(embed=embed)

  



#Help Embed Vteam
@client.command(aliases=['Helpvteam','Help-2'])
async def vteamembed(ctx):

  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
    a = prefixes[str(ctx.guild.id)]

  gif=random.choice(gifs2)

  #### Create the initial embed object ####
  embed=discord.Embed(title="VOICE TEAMER", description="This command is used for teaming up the members in M3W2 Lobby to desired number of teams randomly.\n If you want to form team in other voice channel category.. create a role 'M3W2' and assign it. \nThis command create required number of teams and move the members randomly to their respective teams.", color=0x2ecc71)

# Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=ctx.author.display_name,  icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url=gif)

  embed.add_field(name="SYNTAX", value=f"{a}vteam [number of team]", inline=True) 

  embed.add_field(name="EXAMPLE", value=f"If you want two team, syntax is {a}vteam 2 ", inline=True)

  embed.add_field(name="INSTRUCTIONS", value=f"1. Create M3W2 Category and channel, enter command {a}vteam 1 \n2. If this command doesn't summon M3W2 Lobby channel, delete the category and retype the command.\n3. please delete M3W2 Team - x channel if not needed by {a}over command. if the M3W2 Team - x channel exist, delete manually. \n4. Enter number of teams less than or equal to number of members in the M3W2 Lobby channel. \n5. You and all members must be in M3W2 Lobby channel to summon and seperate teams", inline=False)

  embed.add_field(name="Privilaged M3W2", value=f"If you want to form team other than M3W2 Teams category or M3W2 Lobby, create a role 'M3W2' and assign it to you..!\n This role helps you to form teams from other voice channels and has special {a}over command access to delete the created teams channel", inline=False)

  embed.add_field(name=f"{a}Help-1 or {a}help", value=f"Information about all commands", inline=False)

  embed.add_field(name=f"{a}Help-3 or {a}Helpover", value=f"Information about {a}over command", inline=True)

  embed.set_footer(text="\nThanks for using my Bot <3 \n Page-2/3")

  await ctx.send(embed=embed)



#Help Embed
@client.command(aliases=['Helpover','Help-3'])
async def embedover(ctx):

  with open('prefixes.json','r') as f:
    prefixes=json.load(f)
    a = prefixes[str(ctx.guild.id)]

  gif=random.choice(gifs2)

  #### Create the initial embed object ####
  embed=discord.Embed(title="OVER", description="If you finished the game, use this command to move all the members from all created teams to M3W2 Lobby and delete all teams in that category..!", color=0xf1c40f)

# Add author, thumbnail, fields, and footer to the embed
  embed.set_author(name=ctx.author.display_name,  icon_url=ctx.author.avatar_url)

  embed.set_thumbnail(url=gif)

  embed.add_field(name="SYNTAX", value=f"{a}over", inline=True) 

  embed.add_field(name="EXAMPLE", value=f"If your game is over and want all members back to lobby, use command {a}over ", inline=True)

  embed.add_field(name="Special Access..!", value="if you have role 'M3W2', you can delete the created team channel in that category and return to any voice channel in that particular category..!", inline=False)

  embed.add_field(name=f"{a}Help-1 or {a}help", value=f"Information about all commands", inline=True)

  embed.add_field(name=f"{a}Help-2 or {a}Helpvteam", value=f"Information about {a}vteam command", inline=False)


  embed.set_footer(text="\nThanks for using my Bot <3 \n Page-3/3")

  await ctx.send(embed=embed)



keep_alive()
client.run(os.environ['Token'])
