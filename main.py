from distutils.log import error
from pydoc import cli
from queue import Empty
import sys
from turtle import color
import discord 
from discord.ext import tasks
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
from discord.utils import get
import random

intents = discord.Intents.default()
intents.members = True
intents.all()

client = commands.Bot(command_prefix = "f", intents = intents, help_command = None)
#Playing -> activity = discord.Game(name="!help")
#Streaming -> activity = discord.Streaming(name="!help", url="twitch_url_here")
#Listening -> activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
#Watching -> activity = discord.Activity(type=discord.ActivityType.watching, name="!help")

@client.event
async def on_ready():
    print("User Current Version:-", sys.version)
    print("finished...")

#------------------------------------ping------------------------------------
@client.command()
async def ping(ctx):
    embed = discord.Embed(title = f'Pong! Latency: {round(client.latency * 1000)}ms', color=0x1e5e31)
    await ctx.send(embed = embed)


#------------------------------------ban------------------------------------
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} got banned!') 

#------------------------------------unban------------------------------------
@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user

    await ctx.guild.unban(user)
    await ctx.send(f'User {member} was unbanned!') 

#------------------------------------assign Role------------------------------------
@client.command()
@commands.has_permissions(administrator=True)
async def assignRole(ctx, roleId : discord.Role):
    server = client.get_guild(SERVER_ID)
    role2 = discord.utils.get(server.roles, id = ROLE_ID) #Rolle, which gets assigned
    print("Role assigned to:")
    await ctx.send("done")
    for guild in client.guilds:
        for member in guild.members:
            if roleId in member.roles:
                print(member.name)
                await member.add_roles(role2) 

#------------------------------------help------------------------------------
@client.command()
async def help(ctx):
    embed = discord.Embed(title="HELP", description=f"Here you find a full list of all bot commands sorted by permissions:", color=0x1e5e31)
    embed.add_field(name= "PRÄFIX", value= "PREFIX", inline=False)
    embed.add_field(name= "ADMIN", value= "ban, unban, rules, assignRole", inline=False)
    embed.add_field(name= "MODERATOR", value= "kick, purge", inline=False)
    embed.add_field(name= "MEMBER", value= "ping, avatar, invite", inline=False)
    embed.set_footer(text="for any help or feedback contact OWNER_DISOCRD_TAG")

    await ctx.send(embed=embed)

#------------------------------------kick------------------------------------
@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'User {member} got kicked')  
    except: 
        return

#------------------------------------on member join------------------------------------
@client.event
async def on_member_join(member):
    server = client.get_guild(SERVER_ID)
    channel = client.get_channel(CHANNEL_ID)
    guild = member.guild

#------------------------------------autoroles------------------------------------
    role1 = discord.utils.get(server.roles, id = ROLE_ID)
    role2 = discord.utils.get(server.roles, id = ROLE_ID)
    role3 = discord.utils.get(server.roles, id = ROLE_ID) 
    await member.add_roles(role1)
    await member.add_roles(role2)
    await member.add_roles(role3)

#------------------------------------welcome message------------------------------------
    embed=discord.Embed(title=f"Welcome {member.name} to {member.guild.name}", description=f"If you have any questions feel free to ping/dm <@OWNER_ID>", color=0x547141) 
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_image(url="IMAGE_URL")
    embed.set_footer(text = f"We are now {guild.member_count} member")

    await channel.send("<@&WELCOME_CHANNEL_ID>")
    await channel.send(embed=embed)

#------------------------------------return prefix on ping------------------------------------
@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        if len(message.clean_content) <= 8:
            embed=discord.Embed(title="**Prefix: PREFIX**", color=0x547141)
            embed.set_footer(text = f"requested by {message.author.name}")
            await message.channel.send(embed=embed)

    await client.process_commands(message)
    
#------------------------------------invite link------------------------------------
@client.command()
async def invite(ctx):
    embed=discord.Embed(title="INVITE_LINK", color=0x547141)
    embed.set_footer(text = f"requested by {ctx.author.name}")
    await ctx.send(embed = embed)
            
#------------------------------------purge------------------------------------
@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f"{limit} messages cleared by {ctx.author.mention}")
    await ctx.message.delete()

#------------------------------------output rules as embed------------------------------------
@client.command() 
@commands.has_permissions(administrator=True)
async def rules(ctx):
    embed=discord.Embed(title="Rules of「SERVER_NAME」", color=0x547141)
    embed.add_field(name="General Rules:", value="⸺⸺⸺⸺⸺⸺", inline=False)
    embed.add_field(name="Treat everyone with respect and be friendly when talking to others!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="We DO NOT tolerate any form of homophobia, transphobia, racism, sexism etc. here and try to create a safe space for everyone!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name=" Do not promote any other server, website, youtube channel etc. anywhere in the server except you got permissions from an admin", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="No Alts or bot-accounts are allowed in the server!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Keep in mind that some bots have special rules, so make sure to inform yourself before you use them!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Follow the Discord-TOS [https://discord.com/terms] !", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Voice Rules: ", value="⸺⸺⸺⸺⸺⸺", inline=False)
    embed.add_field(name="Do not abuse your mic!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Avoid streaming / showing NSFW or offensive content in any ways!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Admins are allowed to join any voice chats at any time to moderate them!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Text Rules:", value="⸺⸺⸺⸺⸺⸺", inline=False)
    embed.add_field(name="Use bot commands only in the corresponding channels", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Ecchi content is allowed to an extend! NSFW only in NSFW channels", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Only use english, since this is the only language we can moderate!", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Avoid sensitive topics like politics", value="ˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎˏ⸉ˋ‿̩͙‿̩̩̽‿̩͙ ‿̩̥̩‿̩̩̽‿̩͙ˊ⸊ˎ", inline=False)
    embed.add_field(name="Breaking the rules can result in mute, kick or ban!", value="For any questions ping <@746697061222580295>", inline=False)
    await ctx.send(embed=embed)  

#------------------------------------avatar------------------------------------
@client.command()
async def avatar(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author

    memberAvatar = member.avatar_url

    embed=discord.Embed(title=f"{member.name}´s avatar", color=0x547141) 
    embed.set_image(url=memberAvatar)
    embed.set_footer(text = f"requested by {ctx.author.name}")

    await ctx.send(embed=embed)

#------------------------------------error------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.mention} You dont have permissions to do that!")
    else:
        print(error)

#------------------------------------token------------------------------------       
client.run("TOKEN")
