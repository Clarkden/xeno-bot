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


counting = 0
last_user = ''
banned_counters = []

on_cooldown = {}
on_cooldown2 = {}
move_cooldown = 14400
move_cooldown2 = 60
client = commands.Bot(command_prefix = '.')
client.remove_command('help')
#hi
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d hours %02d minutes %02d seconds" % (hour, minutes, seconds) 
      
@tasks.loop(hours=24)
async def called_once_a_day():
    message_channel = client.get_channel(731781244580397066)
    embed = discord.Embed(description="**Chat cleaned** :soap:", color=discord.Color.green())
    await message_channel.purge(limit=100000)
    await message_channel.send(embed=embed)

@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    channel = client.get_channel(731781244580397066)
    embed = discord.Embed(description="**Cleaning Chat**", color=discord.Color.green())
    await channel.send(embed=embed)

@client.event
async def on_ready():
    channel = client.get_channel(694061907291930664)
    await channel.send('Bot is ready.')
    await client.change_presence(activity=discord.Activity(game=discord.Game(name='Xeno on top')))
    
@client.event
async def on_message(message):
    global counting
    global last_user
    if message.author == client.user:
        return
    channel = message.channel
    if 'hey don\'t say that' in message.content.lower() or 'be nice' in message.content.lower() or 'clarkden is daddy' in message.content.lower():
        await message.add_reaction(":nicecheckmark:742861250341502997")

    if 'kys' in message.content.lower() or 'fuck you' in message.content.lower() or 'kill yourself' in message.content.lower():
        await channel.purge(limit=1)
        #async with channel.typing():
            #await asyncio.sleep(3)
        #color = 0xeb4034
        hello = discord.Embed(description='Hey don\'t say that :)', color=0xeb4034)
        #hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
        await channel.send(embed=hello)
        time.sleep(3)
        await channel.purge(limit=1)
    if 'license' in message.content.lower():
            hello = discord.Embed(title='License', description='After purchasing your license will be delivered to you by @Clarkden when he is available.\nIf you haven\'t already, redeem your key to the redeem key channel to gain access to the User Discord.', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=hello)
    if message.channel.id == 724550485742452820 or message.channel.id  == 731781244580397066 or message.channel.id == 717535356903227413:
        if 'auth failed' in message.content.lower():
            auth_failed = discord.Embed(title='Auth Failed', description='**Some causes of auth failed:**\n1. Entering wrong key or opening premium instead of regular.\n2. Not running as administrator.\n3. Computer or Internet is blocking the connection. Try opening script with vpn.\n4. Hwid needs to be reset. Depending on your subcription use the command .reset or .premium_reset in #hwid_reset\nWhen running the script if it says auth failed with no return message it is most likely error 3', color=discord.Color.purple())
            auth_failed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=auth_failed)
        if 'good settings' in message.content.lower() or 'what settings' in message.content.lower() or 'what is timing' in message.content.lower() or 'what is gun timing' in message.content.lower() or 'how to use' in message.content.lower():
            good_settings = discord.Embed(title='Needed Game Settings', description='1. 85 field fo view\n2. Bordlerless Windowed (Otherwise script will freeze)\n3. If you\'re using auto detect User Interface Scale = 1\n\n To find good settings use the commands\n.show_all_configs | .show_config (config name) | .new_config', color=discord.Color.purple())
            good_settings.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=good_settings)
    if message.channel.id  == 694008360239890495:
        if 'how do i buy' in message.content.lower() or 'how do i purchase' in message.content.lower() or 'what is the price' in message.content.lower() or 'is this free' in message.content.lower() or 'is this undetected' in message.content.lower()  or 'help' in message.content.lower() or 'i want to buy' in message.content.lower() or 'how much' in message.content.lower() or 'are there any slots' in message.content.lower() or 'how many slots' in message.content.lower() or 'how much does this cost' in message.content.lower():
                information_embed = discord.Embed(title='Information', description='**Xeno Information:**\n1. You can purchase on my website: https://xenoservices.xyz.\n2. Slots are limited and are not filled often and maybe not be filled again depending on the user base.\n3. Delivery is instant when purchasing on the website.\n4. This software has never been detected.\n5. For any extra need information please message the owner or moderator.', color=discord.Color.purple())
                information_embed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
                await channel.send(embed=information_embed)
        if 'hello' in message.content.lower.startswith() or 'hi' in message.content.lower.startswith():
            async with channel.typing():
                await asyncio.sleep(3)
            hello = discord.Embed(title='Hello', description='What can I help you with today?', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=hello)
        if 'bye' in message.content.lower.startswith() or 'cya' in message.content.lower.startswith():
            async with channel.typing():
                await asyncio.sleep(4)
            hello = discord.Embed(title='Bye', description='Have a good day', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
            await channel.send(embed=hello)
            await asyncio.sleep(5)
            await message.channel.purge(limit=4)
    if message.channel.id == 748596711747879062:
        if message.content.startswith('1') or message.content.startswith('2') or message.content.startswith('3') or message.content.startswith('4') or message.content.startswith('5') or message.content.startswith('6') or message.content.startswith('7') or message.content.startswith('8') or message.content.startswith('9'):
            user = message.author
            if user == last_user:
                banned_counters.append(user)
                last_user = ''
                counting = 0
                await message.add_reaction(":nologo:742796559896412161")
                await message.channel.send(f"`{message.author} messed up the count! You cannot say more than 1 number in a row!`")
                await message.channel.send("`Start at 1!`")
                if banned_counters.count(user) == 4:
                        await message.channel.send(f"`{user} has lost the ability to count!`")
                        role = discord.utils.get(message.channel.roles, name = f"Counter")
                        await user.remove_roles(role)
            else:
                last_user = user
                try:
                    currentCount = int(message.content)
                    newcount = counting + 1
                    if  currentCount == newcount:
                        counting += 1
                        await message.add_reaction(":nicecheckmark:742861250341502997")
                        if counting == 100:
                            await message.channel.send("`YAY 100`")
                        if counting == 500:
                            await message.channel.send(f"`YAY 500 {message.author} wins`")
                            channel = client.get_channel(694061907291930664)
                            await channel.send(f"`YAY 500 {message.author} wins`")
                            await message.author.send("`Your premium license: GQKHX-F939-K1MDN`")
                    else:
                        banned_counters.append(user)
                        last_user = ''
                        counting = 0
                        await message.add_reaction(":nologo:742796559896412161")
                        await message.channel.send(f"`{message.author} messed up the count!`")
                        await message.channel.send("`Start at 1!`")
                        if banned_counters.count(user) == 4:
                            await message.channel.send(f"`{user} has lost the ability to count!`")
                            role = discord.utils.get(message.channel.roles, name = f"Counter")
                            await user.remove_roles(role)
                    
                except:
                    pass

    await client.process_commands(message)

@client.command()
@commands.is_owner()
async def setcount(ctx, count):
    global counting
    counting = int(count)
    await ctx.channel.send(f'`Count set at {count}`')

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

@client.command()
async def help(ctx):
    embed = discord.Embed(title="All Commands", description="**.download** (Download Xeno)\n**.embed** (Embed a message)\n**.expiration** (Check the expiration of your key)\n**.redeem_key** (Redeem a key from the shoppy to access the user discord)\n**.reset** (Reset your hwid)\n**.new_config** (creates a config that can be uploaded to a database)\n**.show_all_configs** (Shows all configs in the database)\n**.show_config** (Show a specific config)\n**.suggest** (Suggest a feature or bug fix)\n", color=discord.Color.purple())
    embed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")  
    await ctx.send(embed=embed)


@client.command(pass_context=True)
@commands.has_role('Dev/Owner')
async def clear(ctx, number):
    number = int(number)
    realnumber = number
    number = number + 1
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
        embed = discord.Embed(title = 'Commands', description="1. Reset Hwid for Normal Key | .reset\n2. Reset Hwid for Premium Key | .premium_reset\n3. Get Download for script | .download\n4. Embed a message | .embed\n5. Suggest a feature or fix bug | .suggest\n6. Check Expiration on key | .expiration", color = discord.Color.green())
        embed.set_author(name='Xeno', icon_url="https://cdn.discordapp.com/attachments/717535356903227416/739658839678517278/Xeno2.jpg")
        embed.set_footer(text = '.bot_commands')
        await ctx.send(embed=embed)

@client.command()
async def join(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if ctx.channel.id == 694013033521086554:
        member = ctx.author if not member else member
        role = discord.utils.get(ctx.guild.roles, name = "Intern")
        await member.add_roles(role)

@client.command()
@commands.is_owner()
async def create_key(ctx, key):
    mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'],)
    await ctx.channel.purge(limit=1)
    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO access_keys VALUES ('NULL', '{key}')")
    await ctx.channel.send(f'`Created key: {key}`')
    mydb.commit()
    mycursor.close()
    mydb.close()


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
            role2 = discord.utils.get(ctx.guild.roles, name = "Intern")
            await member.send(invitelink) 
            await member.add_roles(role)
            await member.remove_roles(role2)
            await member.send("`Please wait for Clarkden to get online to receive your key for the script. Nobody else can give you the key and download.`")
        else:
            await member.send("`There was an issue validating your key. Please message Clarkden.`")
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

    embed = discord.Embed(title = 'Error', description = "Command is not active", color = discord.Color.red())
    embed.set_author(name=f'{ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
    await ctx.send(embed=embed)

    '''
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
                #embed = discord.Embed(title = 'Hwid Reset', color = discord.Color.green())
                embed = discord.Embed(description=f'<@{author}>',color = discord.Color.green())
                embed.set_author(name=f'Hwid Reset Succeeded', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742831007178162238/6951_Online.png")
                #embed.add_field(name = 'Reset', value = 'Success')
                #embed.set_footer(text = f'<@{author}>')
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
                embed = discord.Embed(description=f'<@{author}>',color = discord.Color.red())
                embed.set_author(name=f'Hwid Reset Failed', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
                #embed = discord.Embed(description = 'Error', color = discord.Color.red())
                #embed.set_author(name=f'{ctx.author.name}')
                #embed.set_footer(text = 'Key does not exist or is expired')
                await ctx.send(embed=embed)
        else:
            channel = ctx.message.channel
            messages = []
            async for message in channel.history(limit=1):
                    messages.append(message)
            await channel.delete_messages(messages)
            cooldown_count = move_cooldown - last_move.seconds
            real_coold_count = convert(cooldown_count)

            embed = discord.Embed(description=f'<@{author}> you are still on cooldown for {real_coold_count}',color = discord.Color.red())
            embed.set_author(name=f'Hwid Reset Failed', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'{ctx.author.name}', icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)
        '''

@client.command()
@commands.has_role('User')
async def download(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if ctx.channel.id == 740419650612887643 or ctx.channel.id==717535356903227418:
        def checkmsg(m):
            return m.author == member
        author = ctx.author.id
        member = ctx.author if not member else member
        try:
            # calculate the amount of time since the last (successful) use of the command
            last_move = datetime.now() - on_cooldown2[author]
        except KeyError:
            last_move = None
            on_cooldown2[author] = datetime.now()
        if last_move is None or last_move.seconds > move_cooldown2:
            await member.send("What is your key?")
            msg = await client.wait_for('message', check=checkmsg, timeout=250.0)
            string = msg.content
            r = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY'], 'license': f'{string}'})
            p = requests.post('https://api.c0gnito.cc/simple-authenticate', data={'publicKey':os.environ['PUBLIC_KEY_PREMIUM'], 'license': f'{string}'})
            if 'true' in r.text or 'true' in p.text:
                await member.send("Type `1` for `Xeno 2.7.5` or `2` for `Xeno 2.7.5.5 (beta update)` or `3` for `Xeno 2.7.5.5 (fixed auto-detect)`")
                msg2 = await client.wait_for('message', check=checkmsg, timeout=250.0)
                string2 = msg2.content
                if '1' in string2:
                    await member.send("https://mega.nz/file/zENlXCxL#Ek7ifZvE-eLG7b6-UCNhLFA9W7xus46ZURFEgfxY4SI")
                    channel = client.get_channel(694061907291930664)
                    await channel.send(f'`{member} downloaded the Xeno v2.7.5`')
                elif '2' in string2:
                    await member.send("https://mega.nz/file/accl1QpS#yFAq2kmTF6yi7lqqPw45gX3qESpG8tkbZDdW8ICaj3Q")
                    channel = client.get_channel(694061907291930664)
                    await channel.send(f'`{member} downloaded the test update`')
                elif '3' in string2:
                    await member.send("https://mega.nz/file/mJthVQwA#KPxdDotNtYH3TMCgyadfXVmE6ABrChRMn3es44gzeRE")
                    channel = client.get_channel(694061907291930664)
                    await channel.send(f'`{member} downloaded the test update with fixed auto detect`')
                else:
                    await member.send("Invalid Option")
            else:   
                await member.send("Key not active or is expired")
        else:
            cooldown_count = move_cooldown2 - last_move.seconds
            real_coold_count = convert(cooldown_count)
            embed = discord.Embed(title="Error", description = f'<@{member.id}> you are still on cooldown for {real_coold_count}', color = discord.Color.red())
            embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
            await member.send(embed=embed)
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
        await ctx.send(embed=embed)
 
 
@client.command()
@commands.has_role('Premium')
#@cooldown(1, 14400, BucketType.user)
async def premium_reset(ctx,member: discord.Member = None):
    await ctx.channel.purge(limit=1)
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
                embed = discord.Embed(description=f'<@{author}>',color = discord.Color.green())
                embed.set_author(name=f'Premium Hwid Reset Success', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742831007178162238/6951_Online.png")
                await ctx.channel.send(embed=embed)
                requests.post('https://api.c0gnito.cc/reset-hwid', data={'privateKey':os.environ['PRIVATE_KEY_PREMIUM'], 'license': f'{string}'})
            else:   
                embed = discord.Embed(description=f'<@{author}>',color = discord.Color.red())
                embed.set_author(name=f'Hwid Reset Failed', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
                await ctx.send(embed=embed)
        else:
            cooldown_count = move_cooldown - last_move.seconds
            real_coold_count = convert(cooldown_count)
            embed = discord.Embed(description=f'<@{author}> you are still on cooldown for {real_coold_count}',color = discord.Color.red())
            embed.set_author(name=f'Hwid Reset Failed', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
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
            embed.set_footer(text = '.expiration')
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
    author = member.id
    await ctx.channel.purge(limit=0)
    embed = discord.Embed(title="Kick",description=f"\nName: <@{author}>\nReason: `{reason}` ", color=discord.Color.purple())
    #embed = discord.Embed(description=f"<:nicecheckmark:742861250341502997> | <@{author}> has been kicked for {reason}", color=discord.Color.blue())
    embeded = await ctx.send(embed=embed)
    await embeded.add_reaction(":nicecheckmark:742861250341502997")
    await member.send(embed=embed)
    await member.kick(reason=reason)

@client.command()
@commands.has_role('Dev/Owner')
async def ban(ctx, member : discord.Member, *, reason=None):
    author = member.id
    await ctx.channel.purge(limit=0)
    embed = discord.Embed(title="Ban",description=f"\nName: <@{author}>\nReason: `{reason}` ", color=discord.Color.purple())
    #embed = discord.Embed(description=f"<:nicecheckmark:742861250341502997> | <@{author}> has been banned for {reason}", color=discord.Color.blue())
    embeded = await ctx.send(embed=embed)
    await embeded.add_reaction(":nicecheckmark:742861250341502997")
    await member.send(embed=embed)
    await member.ban(reason=reason)

@client.command()
async def all_warns(ctx):
    mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'])

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT Discord, Reason, Warner FROM Warns")
    config_get = mycursor.fetchall()
    configs = ""
    for row in config_get:
        configs+="Discord: "
        configs+="`"
        configs+=str(row[0])
        configs+="`"
        configs+=" Reason: "
        configs+="`"
        configs+=str(row[1])
        configs+="`"
        configs+=" Warner: "
        configs+="`"
        configs+=str(row[2])
        configs+="`"
        configs+="\n"
    #print(config_get, end=" ")
    embed = discord.Embed(title="All Warns",description=f"{configs}\n **Total Warns: {mycursor.rowcount}**", color=discord.Color.purple())
    embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
    await ctx.channel.send(embed=embed)
    #time.sleep(5)
    mydb.commit()
    mycursor.close()
    mydb.close()




@client.command()
async def remove_warn(ctx, member : discord.Member, *, reason=None):
    if ctx.author.id == 208036172247728128 or ctx.author.id == 519167807108415499:
        await ctx.channel.purge(limit=1)
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'],
        )
        mycursor = mydb.cursor()
        mycursor.execute(f"DELETE FROM Warns WHERE Discord='{member}' AND Reason='{reason}'")
        mydb.commit()
        mycursor.close()
        mydb.close()
        time.sleep(5)

        embed = discord.Embed(title="Warning Removed",description=f"\n`Warning removed by:`<@{ctx.author.id}>\n`Recepient of original warning:`<@{member.id}> \n`Warning reason: {reason}`", color=discord.Color.purple())
        embed.set_author(name="Xeno", icon_url="https://cdn.discordapp.com/attachments/700994155945394246/742867155451772938/Xeno2-nobackground.gif")
        await ctx.channel.send(embed=embed)
        await member.send(embed=embed)

    else:
        ctx.channel.send("You lack the perms to use this command")
    


@client.command()
#@commands.is_owner()
async def warn(ctx, member : discord.Member, *, reason=None):
    author = member.id
    warner = ctx.author
    await ctx.channel.purge(limit=1)
    #if ctx.author.id == 208036172247728128 or ctx.author.id == 519167807108415499:
    if ctx.author.id == 208036172247728128:
        if author == 208036172247728128:
            await ctx.channel.send("`You cannot warn Clarkden`")
        else:
            mydb = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            passwd=os.environ['PASSWORD'],
            database=os.environ['DATABASE'],
        )
            mycursor = mydb.cursor()
            mycursor.execute(f"INSERT INTO Warns VALUES ('NULL', '{member}', '{reason}', '{warner}', '{author}')")
            mydb.commit()
            mycursor.close()
            mydb.close()

            time.sleep(5)
            mydb = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            passwd=os.environ['PASSWORD'],
            database=os.environ['DATABASE'],
        )
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT * FROM Warns WHERE discord='{member}'")
            mycursor.fetchall()
            #member = client.get_user(author)

            embed = discord.Embed(title="Warning",description=f"\nName: <@{author}>\nReason:`{reason}`\nWarns: `{mycursor.rowcount}`\nWarner: <@{warner.id}>", color=discord.Color.purple())
            embed.set_author(name="Xeno", icon_url="https://cdn.discordapp.com/attachments/700994155945394246/742867155451772938/Xeno2-nobackground.gif")
            await member.send(embed=embed)
            embeded = await ctx.send(embed=embed)
            await embeded.add_reaction(":nicecheckmark:742861250341502997")

            if mycursor.rowcount == 3:
                embed = discord.Embed(title="Ban",description=f"\nName: <@{author}>\nReason: `{reason}`\nReason for ban: `Warned 3 times` ", color=discord.Color.purple())
                embed.set_author(name="Xeno", icon_url="https://cdn.discordapp.com/attachments/700994155945394246/742867155451772938/Xeno2-nobackground.gif")
                embeded = await ctx.send(embed=embed)
                await embeded.add_reaction(":nicecheckmark:742861250341502997")
                await member.send(embed=embed)
                await member.ban(reason=reason)
            
            mydb.commit()
            mycursor.close()
            mydb.close()
    else:
        ctx.channel.send("`You lack the perms to use this command`")



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
    await poo.add_reaction(":online:742849952568442960")
    await poo.add_reaction(":offline:742850032688037973")
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
async def info(ctx, wanted_channel, *, string):
    #channel = ctx.message.channel
    wanted_channel = int(wanted_channel)
    channel = client.get_channel(wanted_channel)
    embed = discord.Embed(description=f"{string}", color=discord.Color.green())
    #embed = discord.Embed('''title="Information",'''description=f"\n{string}\n\n-Xeno Bot", color=discord.Color.purple())
    embed = discord.Embed(description=f"\n{string}\n\n-Xeno Bot", color=discord.Color.purple())
    embed.set_author(name=f"Xeno Information", icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742823638897655829/3224_info.png")
    await ctx.channel.purge(limit=1)
    #await channel.send('||@here||')
    await channel.send("||@here||", embed=embed)

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
    if ctx.channel.id == 731781244580397066:
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])

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
                adjustment = row[6]
                author = row[7]
            embed = discord.Embed(title=f"Config: {name} by {author}",description=f"Timing: {timing}\nGun Timing: {guntiming}\nControl Percent: {controlpercent}\nHumanization: {humanization}\nAdjustment: {adjustment}", color=discord.Color.green())
            embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Config Error",description=f"The config named {name} could not be found", color=discord.Color.red())
            embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
            await ctx.channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
        await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def delete_config(ctx, *, name):
    mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'])

    mycursor = mydb.cursor()
    mycursor.execute(f"DELETE FROM Configs WHERE Name='{name}'")
    embed = discord.Embed(title="Config Deleted",description=f"The config named {name} was deleted", color=discord.Color.red())
    embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
    await ctx.channel.send(embed=embed)
    #time.sleep(5)
    mydb.commit()
    mycursor.close()
    mydb.close()

@client.command()
@commands.has_role('User')
async def show_all_configs(ctx):
    if ctx.channel.id == 731781244580397066:
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])

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
        embed = discord.Embed(title="All Configs",description=f"{configs}\n **Total Configs: {mycursor.rowcount}**", color=discord.Color.purple())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await ctx.channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
        await ctx.send(embed=embed)

@client.command()
@commands.has_role('User')
async def new_config(ctx,member: discord.Member = None):
    if ctx.channel.id == 731781244580397066:
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])
        
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
        await ctx.channel.send("Enter your Adjustment value and your sensitivity(the effect of adjustment varies per sensitivity):")
        Adjustment = await client.wait_for('message', check=checkmsg)
        Adjustment = Adjustment.content
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM Configs WHERE Name='{name}'")
        name_check = mycursor.fetchone()
        await ctx.channel.purge(limit=12)
        if name_check:#[0]: #== 1:
            embed = discord.Embed(title="Config Error",description=f"The name {name} has been used already", color=discord.Color.red())
            embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
            await ctx.channel.send(embed=embed)
        else:
            mycursor.execute(f"INSERT INTO Configs VALUES ('{name}','NULL','{Timing}','{GunTiming}','{ControlPercent}', '{Humanization}','{Adjustment}', '{ctx.author}')")
            embed = discord.Embed(title="Config Added",description=f"Config named `{name}` has been added Successfully ", color=discord.Color.green())
            embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
            await ctx.channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel", color = discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
        await ctx.send(embed=embed)

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

@client.command()
@commands.is_owner()
async def message_all(ctx, channelid, role: discord.Role):
    channelid = int(channelid)
    channel = client.get_channel(channelid)
    await ctx.channel.purge(limit=1)
    for member in channel.guild.members:
        if role in member.roles:
            try:
                embed = discord.Embed(title='Xeno Rust Script',description=f"Hi {member}, administration has noticed that you haven't purchased. Xeno is premium rust software and will provide a great experience for anyone using it. If you are interested, message Clarkden for more information. Feel free to check out our latest showcase as well: https://youtu.be/5Tjtqs7dXes", color=discord.Color.purple())
                await member.send(embed=embed)    
            except:
                pass            

@client.command()
@commands.is_owner()
async def give_all_role(ctx, channelid, role: discord.Role):
    channelid = int(channelid)
    channel = client.get_channel(channelid)
    await ctx.channel.purge(limit=1)
    role2 = discord.utils.get(ctx.guild.roles, name = f"{role}")
    for member in channel.guild.members:
        try:
            await member.add_roles(role2)
            #await member.send(embed=embed)    
        except:
            pass            


#called_once_a_day.start()
client.run(os.environ['DISCORD_TOKEN'])
