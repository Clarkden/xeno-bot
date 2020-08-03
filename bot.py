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
#hi
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
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel
    if 'auth' in message:
        if 'failed' in message:
            auth_failed = discord.Embed(title='Auth Failed', description='**Some causes of auth failed:**\n1. Entering wrong key or opening premium instead of regular.\n2.Not running as administrator.\n3.Computer\Internet is blocking the connection. Try opening script with vpn.\n4.Hwid needs to be reset. Depending on your subcription use the command $reset or $premium_reset followed by your key. For exmaple, $reset 1234.', color=discord.Color.purple())
            auth_failed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=auth_failed)
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="Please pass in all required arguments", color=discord.Color.red())
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRole):
        embed = discord.Embed(description="Role is insufficient", color=discord.Color.red())
        await ctx.send(embed=embed)
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(description="Command not found", color=discord.Color.red())
        await ctx.send(embed=embed)  

@client.command(pass_context=True)
@commands.has_role('Dev/Owner')
async def clear(ctx, number):
    number = int(number)
    realnumber = number
    number = number + 1
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=number):
              messages.append(message)
    embed = discord.Embed(description=f":white_check_mark: | {realnumber} messages were deleted", color=discord.Color.green())
    await channel.delete_messages(messages)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_role('Dev/Owner')
async def clear_chat(ctx):
    embed = discord.Embed(description="**Chat cleaned** :soap:", color=discord.Color.green())
    await ctx.channel.purge(limit=100000)
    await ctx.send(embed=embed)

    
@client.command()
@commands.has_role('User')
#@cooldown(1, 14400, BucketType.user)
async def reset(ctx, string,member: discord.Member = None):
    author = ctx.author.id
    member = ctx.author if not member else member
    try:
        # calculate the amount of time since the last (successful) use of the command
        last_move = datetime.now() - on_cooldown[author]
    except KeyError:
        last_move = None
        on_cooldown[author] = datetime.now()
    if last_move is None or last_move.seconds > move_cooldown:
        r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY'], 'license': f'{string}'})
        if 'true' in r.text:
            embed = discord.Embed(title = 'Hwid Reset', color = discord.Color.green())
            embed.set_author(name=f'{ctx.author.name}', icon_url=f"{member.avatar_url}")
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
async def premium_reset(ctx,member: discord.Member = None, *, string):
    author = ctx.author.id
    member = ctx.author if not member else member
    try:
        # calculate the amount of time since the last (successful) use of the command
        last_move = datetime.now() - on_cooldown[author]
    except KeyError:
        last_move = None
        on_cooldown[author] = datetime.now()
    if last_move is None or last_move.seconds > move_cooldown:
        r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY_PREMIUM'], 'license': f'{string}'})
        if 'true' in r.text:
            embed = discord.Embed(title = 'Premium Hwid Reset', color = discord.Color.green())
            embed.set_author(name=f'{ctx.author.name}', icon_url=f"{member.avatar_url}")
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
async def expiration(ctx, member: discord.Member = None, *, string):
    author = ctx.author.id
    member = ctx.author if not member else member
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
        embed = discord.Embed(title="Expiration Check", color = discord.Color.green())
        embed.set_author(name=f'{ctx.author.name}', icon_url=f"{member.avatar_url}")
        embed.add_field(name = 'Expiration', value = f'{real_expiration}')
        embed.set_footer(text = '60 second cooldown before using this command again')
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=1):
                messages.append(message)
        await channel.delete_messages(messages)
        await channel.send(embed=embed)
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
@commands.has_role('Dev/Owner')
async def warn(ctx, member : discord.Member, *, reason=None):
    author = ctx.author
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
            messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(description=f":white_check_mark: | {member} has been warned for {reason}", color=discord.Color.blue())
    await ctx.send(embed=embed)
    await member.warn(reason=reason)
    embed = discord.Embed(description=f":white_check_mark: | You have been warned for {reason}\n\nPlease try not to do this agian :slight_smile:", color=discord.Color.blue())
    await member.send(embed=embed)


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
@commands.has_role('User')
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
async def embed_in_channel(ctx, channel, *, string):
    channel1 = ctx.message.channel
    channel2 = client.get_channel(f"{channel}")
    messages = []
    async for message in channel1.history(limit=1):
              messages.append(message)
    embed = discord.Embed(description=f"{string}", color=discord.Color.green())
    await channel1.delete_messages(messages)
    await channel2.send(embed=embed)
    
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
@commands.has_role('Dev/Owner')
async def accept_application(ctx, member : discord.Member):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
              messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(description=f"{member} | Application Accepted", color=discord.Color.green())
    await member.send(embed=embed)
    role = discord.utils.get(ctx.guild.roles, name = "Intern") 
    await member.add_roles(role)
    await channel.send(embed=embed)

@client.command()
@commands.has_role('Dev/Owner')
async def decline_application(ctx, member : discord.Member, reason="Denied"):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
              messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(description=f"{member} | Application Denied", color=discord.Color.red())
    channel = client.get_channel(694061907291930664)
    await member.send(embed=embed)
    await channel.send(embed=embed)
    await member.kick(reason=reason)

    
@client.command()
async def application(ctx, member: discord.Member = None):
    application_author = ctx.message.author
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=1):
              messages.append(message)
    await channel.delete_messages(messages) 
    #if not member else member
    member = ctx.author if not member else member
    def checkmsg(m):
        return m.author == member

    def checkreact(reaction, user):
        return user.id == member.id and str(reaction.emoji) in ['✅', '❌']
    try:
        doodoo = discord.Embed(title="Application will start soon...",
                                description="You will be granted or denied access based on your answers", color=discord.Color.gold())
        await member.send(embed=doodoo)
        async with member.typing():
            await asyncio.sleep(5)
        await member.send("What's your Discord Username?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        first = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("Have you use any other scripts previously? If so, describe your experience and name the script.")
        msg = await client.wait_for('message', check=checkmsg, timeout=700.0)
        second = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("Are you decent with computers? (So I won't have to spend hours helping you troubleshoot if you have errors)")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        third = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("Why do you want to join Xeno?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        fourth = msg.content
        async with member.typing():
            await asyncio.sleep(2)
        await member.send("If you do join, do you intend on purchasing the script?")
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
            embed = discord.Embed(description=f"{member} | Thank you for applying! Your application will be reviewed!", color=discord.Color.green())
            await member.send(embed=embed)
            await asyncio.sleep(3)
            poopoo = discord.Embed(
                title='Application Answers', description=f"**1) What\'s your Discord Username?**\n{first}\n**2) Have you used any other scripts previously? If so, describe your experience and name the script.**\n{second}\n**3) Are you decent with computers? (So I won't have to spend hours helping you troubleshoot if you have errors)**\n{third}\n**4)Why do you want to join Xeno?**\n{fourth}\n**5) If you do join, do you intend on purchasing the script?**\n{fifth}\n**6) Anything else you want to say?**\n{sixth}",color=discord.Color.gold())
            poopoo.set_author(
                name=f"Application taken by: {member}", icon_url=f"{member.avatar_url}")
            poopoo.set_footer(text=f"{member}")
            #poopoo.timestamp = datetime.datetime.utcnow()
            await channel.send(embed=poopoo)
        else:
            if str(reaction.emoji) == '❌':
                embed = discord.Embed(description=f"{member} | Your application won't be submitted", color=discord.Color.red())
                await member.send(embed=embed)

client.run(os.environ['DISCORD_TOKEN'])
