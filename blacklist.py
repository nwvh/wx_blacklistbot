# ┬  ┌┬┐  ┌─┐  ┌─┐  ┬─┐  ┌┬┐  ┌─┐
# │  │││  ├─┘  │ │  ├┬┘   │   └─┐
# ┴  ┴ ┴  ┴    └─┘  ┴└─   ┴   └─┘

import discord
import json
import time
import pystyle
import os
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext import tasks
from pystyle import *
from datetime import datetime

# ┬  ┬  ┌─┐  ┬─┐  ┬  ┌─┐  ┌┐   ┬    ┌─┐  ┌─┐
# └┐┌┘  ├─┤  ├┬┘  │  ├─┤  ├┴┐  │    ├┤   └─┐
#  └┘   ┴ ┴  ┴└─  ┴  ┴ ┴  └─┘  ┴─┘  └─┘  └─┘

bot = commands.Bot()

banner = """
┬ ┬  ─┐ ┬       ┌┐   ┬    ┌─┐  ┌─┐  ┬┌─  ┬    ┬  ┌─┐  ┌┬┐    ┌┐   ┌─┐  ┌┬┐
│││  ┌┴┬┘  ───  ├┴┐  │    ├─┤  │    ├┴┐  │    │  └─┐   │     ├┴┐  │ │   │ 
└┴┘  ┴ └─       └─┘  ┴─┘  ┴ ┴  └─┘  ┴ ┴  ┴─┘  ┴  └─┘   ┴     └─┘  └─┘   ┴ 
"""

# Colors

r = Colors.red
g = Colors.green
b = Colors.blue
m = Colors.purple
w = Colors.white

with open ('config.json','r') as f:
    config = json.loads(f.read())
with open ('db/database.json','r') as f:
    database = json.loads(f.read())

# ┌─┐  ┬ ┬  ┌┐┌  ┌─┐  ┌┬┐  ┬  ┌─┐  ┌┐┌  ┌─┐
# ├┤   │ │  │││  │     │   │  │ │  │││  └─┐
# └    └─┘  ┘└┘  └─┘   ┴   ┴  └─┘  ┘└┘  └─┘

def clear(): # Clear the console
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        

def log(type,message): # Function for logging
    if type == 'warning':
        type = f"{w}[{Colors.yellow}WARNING{w}]"  
    elif type == 'error':
        type = f"{w}[{Colors.red}ERROR{w}]"
    elif type == 'success':
        type = f"{w}[{Colors.green}SUCCESS{w}]"
    elif type == 'info':
        type = f"{w}[{Colors.light_blue}INFO{w}]"
    else:
        type = f"{w}[{r}UNKNOWN{w}]"
    logtime = time.strftime("%H:%M:%S")
    print(f"{type} [{g}{logtime}{w}] {message}")
    if not os.path.exists('logs/blacklist.log'):
        open('logs/blacklist.log', 'a+').close()
        with open('logs/blacklist.log','w',encoding='utf-8') as logfile:
            logfile.write(
"""
┬    ┌─┐  ┌─┐    ┌─┐  ┬  ┬    ┌─┐
│    │ │  │ ┬    ├┤   │  │    ├┤ 
┴─┘  └─┘  └─┘    └    ┴  ┴─┘  └─┘

Here will be saved every console log, so you can check the bot's every action even after clearing the console.
"""
)
        log('warning',"File logs/blacklist.log doesn't exist or is corrupted. Creating a new one for you...")
    with open('logs/blacklist.log','a') as logfile:
        logfile.write(f"[{logtime}] {message}\n")

def writeToDB(blacklist, filename='db/database.json'): # Function for updating the .json database
    with open(filename,'r+') as file:
        fdata = json.load(file)
        fdata["blacklist"].append(blacklist)
        file.seek(0)
        json.dump(fdata, file, indent = 4)

def addToDB(userid,username,reason,admin): # Function that verifies if userid is not in the database, if not, write into it
    if not isBlacklisted(userid):
        blacklist = {"userid":f"{userid}",
            "username": f"{username}",
            "reason": f"{reason}",
            "admin": f"{admin}"
            }
        writeToDB(blacklist)
        return True
    else:
        return False

def removeFromDB(userid): # Function that removes the user from the database using only the userid
    with open('db/database.json') as file:
        j = json.loads(file.read())
        toSearch = [f"{userid}"] or [userid]
        for element in j['blacklist']:
            if element['userid'] in toSearch:
                j['blacklist'].remove(element)
                
    with open('db/database.json', 'w') as file:
        file.write(json.dumps(j, indent=4))

def clearDB(): # Function that removes EVERYONE from the database
    if blacklistedUsers() >= 1:
        with open('db/database.json') as file:
            j = json.loads(file.read())
            with open(f'backups/database-BACKUP-{random.randint(1111,9999)}.json','w+') as backup:
                backup.write(json.dumps(j, indent=4))
            file.close()

        with open('db/database.json', 'w') as file:
            file.write("""{
        "blacklist": []
}
    """)
        log('success',"Database has been cleared!")
        return True
    else:
        return False

def blacklistedUsers(): # Function that returns the count of users (elements) in the .json database
    users = 0
    with open('db/database.json') as file:
        j = json.loads(file.read())
        for element in j['blacklist']:
            users += 1
    return(users)

def isBlacklisted(userid): # Function that returns if userid is in the database
    with open('db/database.json') as file:
        j = json.loads(file.read())
        toSearch = [f"{userid}"] or [userid]
        for element in j['blacklist']:
            if element['userid'] in toSearch:
                return True

def getBlacklistReason(userid): # Function that returns the reason for being blacklisted
    with open('db/database.json') as file:
        j = json.loads(file.read())
        toSearch = [f"{userid}"] or [userid]
        for element in j['blacklist']:
            if element['userid'] in toSearch:
                return(element['reason'])
                break

def getBlacklistAdmin(userid): # Function that returns the admin that put player on the blacklist
    with open('db/database.json') as file:
        j = json.loads(file.read())
        toSearch = [f"{userid}"] or [userid]
        for element in j['blacklist']:
            if element['userid'] in toSearch:
                return(element['admin'])
                break
            
# ┌─┐  ┬  ┬  ┌─┐  ┌┐┌  ┌┬┐  ┌─┐
# ├┤   └┐┌┘  ├┤   │││   │   └─┐
# └─┘   └┘   └─┘  ┘└┘   ┴   └─┘

OS = 'Unknown'
if os.name == 'nt':
    OS = 'Windows'
elif os.name == 'darwin':
    OS = 'Mac OS'
else:
    OS = 'Linux / Unix-Like'

@tasks.loop(seconds=5) # Updating the database user count every 5 seconds
async def randomstatus():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{blacklistedUsers()} user(s) in blacklist... | 🛸"))

@bot.event
async def on_ready(): # Let the user know that the bot is online and print some info about him
    clear()
    print(Colorate.Horizontal(Colors.red_to_purple,Center.XCenter(Box.DoubleCube(banner)),1))
    print(Colorate.Horizontal(Colors.red_to_purple,Center.XCenter(Box.DoubleCube(f"Bot: {bot.user}\nUID: {bot.user.id}\nServer Count: {len(bot.guilds)}\nBlacklisted users: {blacklistedUsers()}\n\nOperating System: {OS}")),1))
    log('success','Bot has been started!')
    randomstatus.start()

# ┌─┐  ┌─┐  ┌┬┐  ┌┬┐  ┌─┐  ┌┐┌  ┌┬┐  ┌─┐
# │    │ │  │││  │││  ├─┤  │││   ││  └─┐
# └─┘  └─┘  ┴ ┴  ┴ ┴  ┴ ┴  ┘└┘  ─┴┘  └─┘

# Command that adds the user to the blacklist. Supports both mentions and user ids, so you can blacklist users that aren't in the server
@bot.slash_command(name="addblacklist",description="Adds user to blacklist")
async def addblacklist(ctx,user: discord.Option(discord.SlashCommandOptionType.user),reason: discord.Option(discord.SlashCommandOptionType.string)):
    if ctx.author.guild_permissions.kick_members: # Verify that the user that runs the command has appropriate permissions
        embed = discord.Embed(title="",description=f"<:success:1132284744374177923> <@{user.id}> ({user.name}) has been added to blacklist for: **{reason}**",color=discord.Colour.red())
        embed2 = discord.Embed(
            title="",
            # title="You have been BLACKLISTED!",
            description=f"Hello, **{user.name}**! You have been blacklisted from the server **{ctx.guild}**!\n\nReason: **{reason}**\nAdmin, that blacklisted you: **{ctx.author.name}**\n\nYou can appeal in our ticket system.",
            color=discord.Colour.red(),
        )
        # embed2.add_field(name="Server from where you've been blacklisted", value=f"**{ctx.guild}**", inline=False)
        # embed2.add_field(name="Admin that gave you the blacklist", value=f"**{ctx.author.name}**", inline=False)
        # embed2.add_field(name="Reason", value=f"**{reason}**", inline=False)
        embed2.set_footer(text=f"🕑 | {datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}") # footers can have icons too
        embed2.set_author(name="WX Blacklist", icon_url="https://cdn.discordapp.com/attachments/1124446695841865792/1132030438282641478/standard_1.gif")
        embed2.set_image(url="https://cdn.discordapp.com/attachments/1124446695841865792/1132029387726925895/standard.gif")

        if addToDB(user.id,user.name,reason,ctx.author.name) == False: # Checks if the player is on the blacklist already
            alreadyBlacklisted = discord.Embed(
                title="",
                description=f"<:error:1132284040372822038> <@{user.id}> ({user.name}) is already blacklisted!",
                color=discord.Colour.red(),
            )
            log('error',f"{ctx.author.name} tried to add {user} to blacklist, but he's already there!")
            await ctx.respond(embed=alreadyBlacklisted)
        else:
            await ctx.respond(embed=embed)
            log('success',f"{ctx.author.name} added {user} to the blacklist")
            role = ctx.guild.get_role(1132032190679617768)
            await user.send(embed=embed2)
            await user.add_roles(role)
    else:
        noPerms = discord.Embed(
        title="",
        description=f"<:error:1132284040372822038> You don't have permission to use this command!",
        color=discord.Colour.red(),
        )
        await ctx.respond(embed=noPerms)
        log('warning',f"User {ctx.author.name} ({ctx.author.id}) has tried to use /addblacklist without admin role!")

@bot.slash_command(name="removeblacklist",description="Removes user from blacklist")
async def removeblacklist(ctx,user: discord.Option(discord.SlashCommandOptionType.user)):
    if ctx.author.guild_permissions.kick_members:
        if isBlacklisted(user.id):
            embed = discord.Embed(
            title="",
            description=f"<:success:1132284744374177923> <@{user.id}> ({user.name}) has been **removed** from the blacklist",
            color=discord.Colour.green(),
            )
            removed = discord.Embed(
                title="You have removed from the blacklist!",
                description=f"",
                color=discord.Colour.red(),
            )
            removed.add_field(name="Server from where you've been blacklisted", value=f"**{ctx.guild}**", inline=False)
            removed.add_field(name="Admin that removed you from the blacklist", value=f"**{ctx.author.name}**", inline=False)
        
            removed.set_footer(text=f"🕑 | {datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}") # footers can have icons too
            removed.set_author(name="WX Blacklist", icon_url="https://cdn.discordapp.com/attachments/1124446695841865792/1132030438282641478/standard_1.gif")
            # embed.set_thumbnail(url="https://example.com/link-to-my-thumbnail.png")
            removed.set_image(url="https://cdn.discordapp.com/attachments/1124446695841865792/1132050366708592711/standard_2.gif")
            removeFromDB(user.id)
            await user.send(embed=removed)
            log('success',f"{ctx.author.name} removed {user} from the blacklist")
            await ctx.respond(embed=embed)
            role = ctx.guild.get_role(config['blacklistRoleID'])
            await user.remove_roles(role)
        else:
            embed5 = discord.Embed(
            title="",
            description=f"<:error:1132284040372822038> <@{user.id}> ({user.name}) is not blacklisted!",
            color=discord.Colour.red(),
            )
            await ctx.respond(embed=embed5)
    else:
        noPerms = discord.Embed(
        title="",
        description=f"<:error:1132284040372822038> You don't have permission to use this command!",
        color=discord.Colour.red(),
        )
        await ctx.respond(embed=noPerms)
        log('warning',f"User {ctx.author.name} ({ctx.author.id}) has tried to use /removeblacklist without admin role!")

@bot.slash_command(name="status",description="Check if user is blacklisted") # Command for checking blacklist status of the user
async def status(ctx,user: discord.Option(discord.SlashCommandOptionType.user)):
    if ctx.author.guild_permissions.kick_members:
        if isBlacklisted(user.id) == True:
            embed = discord.Embed(
            title="",
            description=f"<:success:1132284744374177923> <@{user.id}> ({user.name}) is blacklisted for: {getBlacklistReason(user.id)}.",
            color=discord.Colour.red(),
            )
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
            title="",
            description=f"<:error:1132284040372822038> <@{user.id}> ({user.name}) is **not** blacklisted.",
            color=discord.Colour.green(),
            )

            await ctx.respond(embed=embed)
    else:
        noPerms = discord.Embed(
        title="",
        description=f"<:error:1132284040372822038> You don't have permission to use this command!",
        color=discord.Colour.red(),
        )
        await ctx.respond(embed=noPerms)
        log('warning',f"User {ctx.author.name} ({ctx.author.id}) has tried to use /status without admin role!")
@bot.slash_command(name="blacklisted",description="Checks how many users are in the blacklist")
async def blacklisted(ctx):
    if ctx.author.guild_permissions.kick_members:
        embed = discord.Embed(
        title=f"There are {blacklistedUsers()} users in blacklist",
        description=f"",
        color=discord.Colour.red(),
        )
        with open('db/database.json') as file:
            j = json.loads(file.read())
            for element in j['blacklist']:
                embed.add_field(name="", value=f"**{element['username']}** - **{element['reason']}** (Added by **{element['admin']}**)", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1124446695841865792/1132239082400006204/standard_3.gif")

        await ctx.respond(embed=embed)
    else:
        noPerms = discord.Embed(
        title="",
        description=f"<:error:1132284040372822038> You don't have permission to use this command!",
        color=discord.Colour.red(),
        )
        await ctx.respond(embed=noPerms)
        log('warning',f"User {ctx.author.name} ({ctx.author.id}) has tried to use /blacklisted without admin role!")
@bot.slash_command(name="cleardatabase",description="Clears the database of blacklisted users")
async def clean(ctx):
    if ctx.author.guild_permissions.kick_members:
        embed = discord.Embed(
        title="",
        description=f"Attempting to clear database of {blacklistedUsers()} user(s)...",
        color=discord.Colour.red(),
        )
        await ctx.respond(embed=embed)
        if clearDB() == True:
            embed = discord.Embed(
            title="",
            description=f"<:success:1132284744374177923> Database has been cleared! Backup has been saved, just in case!",
            color=discord.Colour.red(),
            )
            for usr in ctx.guild.members:
                role = ctx.guild.get_role(config['blacklistRoleID'])
                await usr.remove_roles(role)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
            title="",
            description=f"<:error:1132284040372822038> Database is already empty!",
            color=discord.Colour.red(),
            )
            await ctx.respond(embed=embed)
    else:
        noPerms = discord.Embed(
        title="",
        description=f"<:error:1132284040372822038> You don't have permission to use this command!",
        color=discord.Colour.red(),
        )
        await ctx.respond(embed=noPerms)
        log('warning',f"User {ctx.author.name} ({ctx.author.id}) has tried to use /cleardatabase without admin role!")

@bot.event
async def on_member_join(member): # If member joins, the script checks if his user id is in the blacklist, if it is there, put back his blacklisted role. This prevents blacklisted users to leaving and joining back to get rid of the blacklisted role
    log('info',f"joined")
    role = discord.utils.get(member.guild.roles, id=config['blacklistRoleID'])
    if isBlacklisted(member.id):
        await member.add_roles(role)
        log('warning',f"{member.name} ({member.id}) has joined with an active blacklist, adding the role back...")
    else:
        return
try:
    bot.run(config['botToken'])
except:
    log('error',"Your token is invalid! Please check your config.json")