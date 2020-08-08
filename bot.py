import requests
import discord
import os
import asyncio
import typing
import time
from datetime import datetime, timedelta    
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandNotFound, CommandOnCooldown)
from discord.utils import get
import mysql.connector


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
      
@tasks.loop(minutes=30)
async def called_once_a_day():
    message_channel = client.get_channel(731781244580397066)
    embed = discord.Embed(description="**Chat cleaned** :soap:", color=discord.Color.green())
    await ctx.channel.purge(limit=100000)
    await message_channel.send(embed=embed)

@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    channel = client.get_channel(731781244580397066)
    embed = discord.Embed(description="**Cleaning Chat**", color=discord.Color.green())
    await channel.send

@client.event
async def on_ready():
    channel = client.get_channel(694061907291930664)
    await channel.send('Bot is ready.')
    await client.change_presence(activity=discord.Activity(game=discord.Game(name='Xeno on top')))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel
    if 'license' in message.content.lower():
            hello = discord.Embed(title='License', description='After purchasing your license will be delivered to you by @Clarkden when he is available.\nIf you haven\'t already, redeem your key to the redeem key channel to gain access to the User Discord.', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=hello)
    if message.channel.id == 724550485742452820 or message.channel.id  == 731781244580397066 or message.channel.id == 717535356903227413:
        if 'auth failed' in message.content.lower():
            auth_failed = discord.Embed(title='Auth Failed', description='**Some causes of auth failed:**\n1. Entering wrong key or opening premium instead of regular.\n2. Not running as administrator.\n3. Computer or Internet is blocking the connection. Try opening script with vpn.\n4. Hwid needs to be reset. Depending on your subcription use the command $reset or $premium_reset in #hwid_reset\nWhen running the script if it says auth failed with no return message it is most likely error 3', color=discord.Color.purple())
            auth_failed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=auth_failed)
        if 'good settings' in message.content.lower() or 'what settings' in message.content.lower() or 'what is timing' in message.content.lower() or 'what is gun timing' in message.content.lower() or 'how to use' in message.content.lower():
            good_settings = discord.Embed(title='Needed Game Settings', description='1. 85 field fo view\n2. Bordlerless Windowed (Otherwise script will freeze)\n3. If you\'re using auto detect User Interface Scale = 1\n\n To find good settings use the commands\n$show_all_configs | $show_config (config name) | $new_config', color=discord.Color.purple())
            good_settings.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=good_settings)
    if message.channel.id  == 694008360239890495:
        if 'how do i buy' in message.content.lower() or 'how do i purchase' in message.content.lower() or 'what is the price' in message.content.lower() or 'is this free' in message.content.lower() or 'is this undetected' in message.content.lower()  or 'help' in message.content.lower() or 'i want to buy' in message.content.lower() or 'how much' in message.content.lower() or 'are there any slots' in message.content.lower() or 'how many slots' in message.content.lower() or 'how much does this cost' in message.content.lower():
                information_embed = discord.Embed(title='Information', description='**Xeno Information:**\n1. You can purchase on my website: https://xenoservices.xyz.\n2. Slots are limited and are not filled often and maybe not be filled again depending on the user base.\n3. Delivery is instant when purchasing on the website.\n4. This software has never been detected.\n5. For any extra need information please message the owner or moderator.', color=discord.Color.purple())
                information_embed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
                await channel.send(embed=information_embed)
        if 'hello' in message.content.lower() or 'hi' in message.content.lower():
            async with channel.typing():
                await asyncio.sleep(3)
            hello = discord.Embed(title='Hello', description='What can I help you with today?', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=hello)
        if 'kys' in message.content.lower() or 'fuck you' in message.content.lower():
            async with channel.typing():
                await asyncio.sleep(3)
            hello = discord.Embed(title='Hello', description='Hey don\'t say that :)', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=hello)
        if 'bye' in message.content.lower() or 'cya' in message.content.lower():
            async with channel.typing():
                await asyncio.sleep(4)
            hello = discord.Embed(title='Bye', description='Have a good day', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=hello)
            await asyncio.sleep(5)
            await message.channel.purge(limit=4)

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
    await ctx.channel.purge(limit=number)
    embed = discord.Embed(description=f":soap: | {realnumber} messages were deleted", color=discord.Color.green())
    await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_role('Dev/Owner')
async def clear_chat(ctx):
    embed = discord.Embed(description="**Chat cleaned** :soap:", color=discord.Color.green())
    await ctx.channel.purge(limit=100000)
    await ctx.send(embed=embed)

@client.command()
async def bot_commands(ctx):
    if ctx.channel.id == 694008360239890495:
        embed = discord.Embed(name="Error",description="This channel does not have access", color=discord.Color.red())
        await ctx.send(embed=embed)  
    else:
        embed = discord.Embed(title = 'Commands', description="1. Reset Hwid for Normal Key | $reset\n2. Reset Hwid for Premium Key | $premium_reset\n3. Get Download for script | $download\n4. Embed a message | $embed\n5. Suggest a feature or fix bug | $suggest\n6. Check Expiration on key | $expiration", color = discord.Color.green())
        embed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
        embed.set_footer(text = '$bot_commands')
        await ctx.send(embed=embed)

@client.command()
async def join(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if ctx.channel.id == 694013033521086554:
        member = ctx.author if not member else member
        role = discord.utils.get(ctx.guild.roles, name = "Intern")
        await member.add_roles(role)

@client.command()
@commands.has_role('Intern')
async def redeem_key(ctx, key, member: discord.Member = None):
    
    if ctx.channel.id == 740405740950519839 or ctx.channel.id == 717535356903227413:
        mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'],
)
        await ctx.channel.purge(limit=1)
        author = ctx.author.id
        member = ctx.author if not member else member
        #key = str(key)
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * from access_keys where access='{key}'")
        redeemed = mycursor.fetchone()
        if redeemed:#[0]: #== 1:
            mycursor.execute(f"DELETE from access_keys where access='{key}'")
            channel = client.get_channel(724550485742452820)
            invitelink = await channel.create_invite(max_uses=1,unique=True)
            role = discord.utils.get(ctx.guild.roles, name = "New User")
            await member.send(invitelink) 
            await member.add_roles(role)
            await member.send("Please wait for Clarkden to get online to receive your key for the script. Nobody else can give you the key and download.")
        else:
            await member.send("There was an issue validating your key. Please message Clarkden.")
    else:
        await ctx.channel.purge(limit=1)
    #time.sleep(10)
    mydb.commit()
    mycursor.close()
    mydb.close()

@client.command()
@commands.has_role('User')
#@cooldown(1, 14400, BucketType.user)
async def reset(ctx, member: discord.Member = None):
    if ctx.channel.id == 731781244580397066:
        def checkmsg(m):
            return m.author == member
        author = ctx.author.id
        member = ctx.author if not member else member
        await member.send("What is your key?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        string = msg.content
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
                embed.set_footer(text = '$reset')
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
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

@client.command()
@commands.has_role('User')
@cooldown(1, 14400, BucketType.user)
async def download(ctx, member: discord.Member = None):
    if ctx.channel.id == 740419650612887643:
        def checkmsg(m):
            return m.author == member
        author = ctx.author.id
        member = ctx.author if not member else member
        await member.send("What is your key?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        string = msg.content
        try:
            # calculate the amount of time since the last (successful) use of the command
            last_move = datetime.now() - on_cooldown2[author]
        except KeyError:
            last_move = None
            on_cooldown[author] = datetime.now()
        if last_move is None or last_move.seconds > move_cooldown:
            r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY'], 'license': f'{string}'})
            p = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY_PREMIUM'], 'license': f'{string}'})
            if 'true' in r.text or 'true' in p.text:
                await member.send("https://mega.nz/file/3M03DBAB#MB9P7viKu5UEd0kje7zcPx5GRgHNAmy-SxAqAp-QsaI")
                await ctx.channel.purge(limit=1)
            else:   
                await member.send("Key not active or is expired")
                await ctx.channel.purge(limit=1)
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
    else:
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)
 
 
@client.command()
@commands.has_role('Premium')
#@cooldown(1, 14400, BucketType.user)
async def premium_reset(ctx,member: discord.Member = None):

    if ctx.channel.id == 731781244580397066:
        def checkmsg(m):
            return m.author == member

        author = ctx.author.id
        member = ctx.author if not member else member
        await member.send("What is your key?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        string = msg.content
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
                embed.set_footer(text = '$premium_reset')
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
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

@client.command()
@commands.has_role('User')
async def expiration(ctx, member: discord.Member = None):
    if ctx.channel.id == 731781244580397066:
        def checkmsg(m):
            return m.author == member
        author = ctx.author.id
        member = ctx.author if not member else member
        await member.send("What is your key?")
        msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
        string = msg.content
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
            embed.set_footer(text = '$expiration')
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=1):
                    messages.append(message)
            await channel.delete_messages(messages)
            await ctx.channel.send(embed=embed)
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
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
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
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(description=f"{string}", color=discord.Color.green())
    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_role('Dev/Owner')
async def announcement(ctx, *, string):
    channel = ctx.message.channel
    embed = discord.Embed(title="Announcement",description=f"\n{string}\n\n-{ctx.author.mention}", color=discord.Color.red())
    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    await channel.purge(limit=1)
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
@commands.has_role('User')
async def show_config(ctx, *, name):
    mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'],
)
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM Configs WHERE Name='{name}'")
    config_get = mycursor.fetchall()
    if(config_get):
        for row in config_get:
            name = row[0]
            timing = row[2]
            guntiming = row[3]
            controlpercent = row[4]
            humanization = row[5]
            author = row[6]
        embed = discord.Embed(title=f"Config: {name} by {author}",description=f"Timing: {timing}\nGun Timing: {guntiming}\nControl Percent: {controlpercent}\nHumanization: {humanization}", color=discord.Color.green())
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title="Config Error",description=f"The config named {name} could not be found", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
    #time.sleep(5)
    mydb.commit()
    mycursor.close()
    mydb.close()

@client.command()
@commands.is_owner()
async def delete_config(ctx, *, name):
    mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'],
)
    mycursor = mydb.cursor()
    mycursor.execute(f"DELETE FROM Configs WHERE Name='{name}'")
    embed = discord.Embed(title="Config Deleted",description=f"The config named {name} was deleted", color=discord.Color.red())
    await ctx.channel.send(embed=embed)
    #time.sleep(5)
    mydb.commit()
    mycursor.close()
    mydb.close()

@client.command()
@commands.has_role('User')
async def show_all_configs(ctx):
    mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'],
)
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT Name, Author FROM Configs")
    config_get = mycursor.fetchall()
    configs = ""
    for row in config_get:
        configs+="**"
        configs+=str(row[0])
        configs+="**"
        configs+=" by "
        configs+=str(row[1])
        configs+="\n"
    #print(config_get, end=" ")
    embed = discord.Embed(title="All Configs",description=f"{configs}", color=discord.Color.purple())
    await ctx.channel.send(embed=embed)
    #time.sleep(5)
    mydb.commit()
    mycursor.close()
    mydb.close()

@client.command()
@commands.has_role('User')
async def new_config(ctx,member: discord.Member = None):
    mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'],
)
    member = ctx.author if not member else member
    def checkmsg(m):
        return m.author == member
    await ctx.channel.send("Enter config name:")
    name = await client.wait_for('message', check=checkmsg)
    name = name.content
    await ctx.channel.send("Enter timing value:")
    Timing = await client.wait_for('message', check=checkmsg)
    Timing = Timing.content
    await ctx.channel.send("Enter gun timing value:")
    GunTiming = await client.wait_for('message', check=checkmsg)
    GunTiming = GunTiming.content
    await ctx.channel.send("Enter your control percent value or if you don't use it enter No:")
    ControlPercent = await client.wait_for('message', check=checkmsg)
    ControlPercent = ControlPercent.content
    await ctx.channel.send("Enter your humanization value or if you don't use it enter No:")
    Humanization = await client.wait_for('message', check=checkmsg)
    Humanization = Humanization.content
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM Configs WHERE Name='{name}'")
    name_check = mycursor.fetchone()
    await ctx.channel.purge(limit=10)
    if name_check:#[0]: #== 1:
        embed = discord.Embed(title="Config Error",description=f"The name {name} has been used already", color=discord.Color.red())
        await ctx.channel.send(embed=embed)
    else:
        mycursor.execute(f"INSERT INTO Configs VALUES ('{name}','NULL','{Timing}','{GunTiming}','{ControlPercent}', '{Humanization}', '{ctx.author}')")
        embed = discord.Embed(title="Config Added",description=f"Config named {name} has been added Successfully ", color=discord.Color.green())
        await ctx.channel.send(embed=embed)
    #time.sleep(5)
    mydb.commit()
    mycursor.close()
    mydb.close()

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

called_once_a_day.start()
client.run(os.environ['DISCORD_TOKEN'])
