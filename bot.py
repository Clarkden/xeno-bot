import requests
import discord
import os
from datetime import datetime, timedelta    
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandNotFound, CommandOnCooldown)


on_cooldown = {}
on_cooldown2 = {}
move_cooldown = 14400
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

@client.command(pass_context=True)
@commands.has_role('Dev/Owner')
async def clear(ctx, number):
    number = int(number)
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=number):
              messages.append(message)

    await channel.delete_messages(messages)
    await ctx.send('Messages deleted.')

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
        embed = discord.Embed(description = 'HWID RESET', color = discord.Color.blue())
        embed.set_author(name=f'{ctx.author.name}')
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
    if last_move is None or last_move.seconds > move_cooldown:
        r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY'], 'license': f'{string}'})   
        keyword = '\"expiresIn\":\"'
        before_keyword, keyword, after_keyword = r.text.partition(keyword)
        expiration = after_keyword.replace('\"', '')
        real_expiration = expiration.replace('}', '')
        embed = discord.Embed(description = 'EXPIRATION DATE CHECK', color = discord.Color.green())
        embed.set_author(name=f'{ctx.author.name}')
        embed.add_field(name = 'Expiration Date', value = f'{real_expiration}')
        embed.set_footer(text = '4 hour cool down before using this command again')
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
        cooldown_count = move_cooldown - last_move.seconds
        real_coold_count = convert(cooldown_count)
        embed.set_footer(text = f'You are still on cooldown for {real_coold_count}')
        await ctx.send(embed=embed)

client.run(os.environ['DISCORD_TOKEN'])
