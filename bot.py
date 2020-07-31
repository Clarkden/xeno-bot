import requests
import discord
import os
import asyncio
import typing
from datetime import datetime, timedelta    
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandNotFound, CommandOnCooldown)
from discord.utils import get

on_cooldown = {}
on_cooldown2 = {}
move_cooldown = 14400
move_cooldown2 = 60
client = commands.Bot(command_prefix = '$')

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d hours %02d minutes %02d seconds" % (hour, minutes, seconds) 
      

@client.event
async def on_ready():
    print('Bot is ready.')
    
@client.event
async def on_reaction_add(reaction, user):
    Channel = client.get_channel(694013033521086554)
    if reaction.message.channel.id != Channel:
        return
    if reaction.emoji == ":white_check_mark:":
      Role = discord.utils.get(user.server.roles, name="Intern")
      await discord.Member.add_roles(user, Role)

@client.command(pass_context=True)
@commands.has_role('Dev/Owner')
async def clear(ctx, number):
    number = int(number)
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=number):
              messages.append(message)
    embed = discord.Embed(description=f":white_check_mark: | {number} messages were deleted", color=discord.Color.green())
    await channel.delete_messages(messages)
    await ctx.send(embed=embed)

@client.command()
@commands.has_role('User')
#@cooldown(1, 14400, BucketType.user)
async def reset(ctx, *, string):
    author = ctx.author.id
    
    try:
        # calculate the amount of time since the last (successful) use of the command
        last_move = datetime.now() - on_cooldown[author]
    except KeyError:
        last_move = None
        on_cooldown[author] = datetime.now()
    if last_move is None or last_move.seconds > move_cooldown:
        r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY'], 'license': f'{string}'})
        if 'true' in r.text:
            embed = discord.Embed(description = 'HWID RESET', color = discord.Color.green())
            embed.set_author(name=f'{ctx.author.name}')
            embed.add_field(name = 'Reset', value = 'Success')
            embed.set_footer(text = '4 hour cool down before using this command again')
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=1):
                    messages.append(message)
            await channel.delete_messages(messages)
            await ctx.send(embed=embed)
            requests.post('https://api.c0gnito.cc/reset-hwid', data={'privateKey':os.environ['PRIVATE_KEY'], 'license': f'{string}'})
        else:  
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=1):
                    messages.append(message)
            await channel.delete_messages(messages)
            embed = discord.Embed(description = 'Error', color = discord.Color.red())
            embed.set_author(name=f'{ctx.author.name}')
            embed.set_footer(text = 'Key does not exist or is expired')
            await ctx.send(embed=embed)
    else:
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=1):
                messages.append(message)
        await channel.delete_messages(messages)
        embed = discord.Embed(description = 'Error', color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}')
        cooldown_count = move_cooldown - last_move.seconds
        real_coold_count = convert(cooldown_count)
        embed.set_footer(text = f'You are still on cooldown for {real_coold_count}')
        await ctx.send(embed=embed)
 
@client.command()
@commands.has_role('Premium')
#@cooldown(1, 14400, BucketType.user)
async def premium_reset(ctx, *, string):
    author = ctx.author.id
    
    try:
        # calculate the amount of time since the last (successful) use of the command
        last_move = datetime.now() - on_cooldown[author]
    except KeyError:
        last_move = None
        on_cooldown[author] = datetime.now()
    if last_move is None or last_move.seconds > move_cooldown:
        r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY_PREMIUM'], 'license': f'{string}'})
        if 'true' in r.text:
            embed = discord.Embed(description = 'PREMIUM HWID RESET', color = discord.Color.green())
            embed.set_author(name=f'{ctx.author.name}')
            embed.add_field(name = 'Reset', value = 'Success')
            embed.set_footer(text = '4 hour cool down before using this command again')
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=1):
                    messages.append(message)
            await channel.delete_messages(messages)
            await ctx.send(embed=embed)
            requests.post('https://api.c0gnito.cc/reset-hwid', data={'privateKey':os.environ['PRIVATE_KEY_PREMIUM'], 'license': f'{string}'})
        else:   
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=1):
                    messages.append(message)
            await channel.delete_messages(messages)
            embed = discord.Embed(description = 'Error', color = discord.Color.red())
            embed.set_author(name=f'{ctx.author.name}')
            embed.set_footer(text = 'Key does not exist or is expired')
            await ctx.send(embed=embed)
    else:
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=1):
                messages.append(message)
        await channel.delete_messages(messages)
        embed = discord.Embed(description = 'Error', color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}')
        cooldown_count = move_cooldown - last_move.seconds
        real_coold_count = convert(cooldown_count)
        embed.set_footer(text = f'You are still on cooldown for {real_coold_count}')
        await ctx.send(embed=embed)

@client.command()
@commands.has_role('User')
async def expiration(ctx, *, string):
    author = ctx.author.id
    try:
        # calculate the amount of time since the last (successful) use of the command
        last_move = datetime.now() - on_cooldown2[author]
    except KeyError:
        last_move = None
        on_cooldown2[author] = datetime.now()
    if last_move is None or last_move.seconds > move_cooldown2:
        r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY'], 'license': f'{string}'})   
        keyword = '\"expiresIn\":\"'
        before_keyword, keyword, after_keyword = r.text.partition(keyword)
        expiration = after_keyword.replace('\"', '')
        real_expiration = expiration.replace('}', '')
        embed = discord.Embed(description = 'EXPIRATION CHECK', color = discord.Color.green())
        embed.set_author(name=f'{ctx.author.name}')
        embed.add_field(name = 'Key Expires in', value = f'{real_expiration}')
        embed.set_footer(text = '60 second cooldown before using this command again')
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=1):
                messages.append(message)
        await channel.delete_messages(messages)
        await ctx.send(embed=embed)
    else:
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=1):
                messages.append(message)
        await channel.delete_messages(messages)
        embed = discord.Embed(description = 'Error', color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}')
        cooldown_count = move_cooldown2 - last_move.seconds
        real_coold_count = convert(cooldown_count)
        embed.set_footer(text = f'You are still on cooldown for {real_coold_count}')
        await ctx.send(embed=embed)

@client.command()
@commands.has_role('Dev/Owner')
async def kick(ctx, member : discord.Member, *, reason=None):
    author = ctx.author
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
            messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(description=f":white_check_mark: | {member} has been kicked for {reason}", color=discord.Color.blue())
    await ctx.send(embed=embed)
    await member.kick(reason=reason)

@client.command()
@commands.has_role('Dev/Owner')
async def ban(ctx, member : discord.Member, *, reason=None):
    author = ctx.author
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
            messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(description=f":white_check_mark: | {member} has been banned for {reason}", color=discord.Color.blue())
    await ctx.send(embed=embed)
    await member.ban(reason=reason)


@client.command()
@commands.has_role('User')
async def suggest(ctx, *, sug):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
        messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(description=f"Suggestion provided by {ctx.author.mention}: {sug}\n\nReact down below to leave your opinion! ⬇️", color=discord.Color.green())
    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    channel = client.get_channel(738536411317272666)
    poo = await channel.send(embed=embed)
    await poo.add_reaction("☑️")
    await poo.add_reaction("🚫")
    embed1 = discord.Embed(description=f"{ctx.author.mention} made a suggestion", color=discord.Color.green())
    embed1.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    channel1 = client.get_channel(694061907291930664)
    await channel1.send(embed=embed1)

@client.command()
@commands.has_role('Dev/Owner')
async def embed(ctx, *, string):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
              messages.append(message)
    embed = discord.Embed(description=f"{string}", color=discord.Color.green())
    await channel.delete_messages(messages)
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_role('Dev/Owner')
async def announcement(ctx, *, string):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
              messages.append(message)
    embed = discord.Embed(description=f"**Announcement from {ctx.author.mention}**: \n{string}\n", color=discord.Color.red())
    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    await channel.delete_messages(messages)
    await ctx.send('||@everyone||')
    await ctx.send(embed=embed)

@client.command()
async def applymod(ctx, member: discord.Member = None):

    #if not member else member
    member = ctx.author if not member else member
    def checkmsg(m):
        return m.author == member

    def checkreact(reaction, user):
        return user.id == member.id and str(reaction.emoji) in ['✅', '❌']
    try:
        doodoo = discord.Embed(title="Application will start soon...",
                                description="Remember to be 100% Honest and provide good answers!\nThe Questions will be sent shortly...", color=discord.Color.dark_orange())
        await member.send(embed=doodoo)
        async with member.typing():
            await asyncio.sleep(5)
        await member.send("What's your Minecraft IGN + Discord Username?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        first = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("How old are you? (If you feel uncomfortable saying this, just confirm if you're at least a teenager)")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        second = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active)")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        third = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("Why do you want to be Moderator? Isn't it fun to play without any responsibilites?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        fourth = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("What will you do for the Discord Server?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        fifth = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("Anything else you want to say?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        sixth = msg.content

    except asyncio.TimeoutError:
        await member.send("You took too long to write in a response :(")
    else:
        channel = client.get_channel(694061907291930664)
        poo = await member.send("Are you sure you want to submit this application?")
        await poo.add_reaction('✅')
        await poo.add_reaction('❌')
        reaction, user = await client.wait_for("reaction_add", timeout=60.0, check=checkreact)
        if str(reaction.emoji) == '✅':
            async with member.typing():
                await asyncio.sleep(3)
            await member.send('Thank you for applying! Your application will be sent to the Owner soon')
            await asyncio.sleep(3)
            poopoo = discord.Embed(
                title='Application Answers', description=f"1) What\'s your Minecraft IGN + Discord Username?\n{first}, \n2) How old are you? (If you're not comfortable saying this at least confirm if you're a teenager)\n{second}, \n3) What Time Zone do you live in? (So I know when you're online, and gives me a reason if you're not too active)\n{third}, \n4)Why do you want to be Moderator? Isn\'t it fun to play without any responsibilites?\n{fourth}, \n5) What will you do for the Discord Server?\n{fifth}, \n6) Anything else you want to say?\n{sixth}", color=discord.Color.dark_orange())
            poopoo.set_author(
                name=f"Application taken by: {member}", icon_url=f"{member.avatar_url}")
            poopoo.set_footer(text=f"{member}")
            poopoo.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=poopoo)
        else:
            if str(reaction.emoji) == '❌':
                await member.send('Application won\'t be sent')

client.run(os.environ['DISCORD_TOKEN'])
