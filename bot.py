import requests
import discord
import os
import asyncio
import typing
import time
import array as arr
from datetime import datetime, timedelta    
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandNotFound, CommandOnCooldown)
from discord.utils import get
import mysql.connector


counting = 0
last_user = ''
banned_counters = []
bad_words = ['nigga', 'nigger', 'kys', 'kill your self', 'kill yourself', 'niggas', 'niggers', 'n i g g a', 'n i g g e r s', 'kkk', 'jew']

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
      
@tasks.loop(hours=1)
async def called_once_a_day():
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])

        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT discord, user_id FROM applications")
        config_get = mycursor.fetchall()
        configs = ""
        for row in config_get:
            configs+="|Application Author: "
            configs+=str(row[0])
            configs+=" |"
            configs+=" User ID: "
            configs+=str(row[1])
            configs+=" |\n"
        #print(config_get, end=" ")
        embed = discord.Embed(title="All Applications",description=f"{configs}\n Total Applications: `{mycursor.rowcount}`", color=discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://media.discordapp.net/attachments/695028034704769034/799354209211646002/unknown.jpeg")
        log_channel = client.get_channel(700994155945394246)
        await log_channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()

@called_once_a_day.before_loop
async def before():
    await client.wait_until_ready()
    channel = client.get_channel(700994155945394246)
    embed = discord.Embed(description="**Fetching all applications hourly**", color=discord.Color.green())
    await channel.send(embed=embed)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Xeno on top'))

    
@client.event
async def on_member_join(member):
    guild = client.get_guild(694008360239890492)
    #guild = discord.utils.get(bot.guilds, name=f"{member}")
    if guild.get_member(member.id) is not None:
    #if member.guild.id == 694008360239890492:
        if time.time() - member.created_at.timestamp() < 2592000:
            reason = "Automatic ban by Xeno Bot. Account too young."
            hello = discord.Embed(title='Banned', description='You You have been automatically banned from Xeno because your account was created less than 30 days ago.', color=discord.Color.purple())
            hello.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
            user = client.get_user(member.id)
            await user.send(embed=hello)
            await member.ban(reason=reason)
            logs = client.get_channel(694061907291930664)
            await logs.send(f'{user} automatically banned. New account.')
        else:
            mydb = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            passwd=os.environ['PASSWORD'],
            database=os.environ['DATABASE'])

            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT * FROM blacklist WHERE blacklisted='{member.id}'")
            mycursor.fetchall()

            if mycursor.rowcount > 0:
                reason = "Automatic ban by Xeno Bot. Blacklisted."
                hello = discord.Embed(title='Banned', description='You You have been automatically banned from Xeno because your account was blacklisted by Clarkden.', color=discord.Color.purple())
                hello.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
                user = client.get_user(member.id)
                await user.send(embed=hello)
                await member.ban(reason=reason)
                logs = client.get_channel(694061907291930664)
                await logs.send(f'{user} automatically banned. Blacklisted account.')
            else:
                hello = discord.Embed(title='Welcome', description='Hi! Welcome to Xeno! If you have any questions please feel free to message Clarkden or Riley. Clarkden is the developer and owner and Riley is a Helper/Moderator.', color=discord.Color.purple())
                hello.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
                await user.send(embed=hello)

            mydb.commit()
            mycursor.close()
            mydb.close()
    else:
        pass

@client.command()
async def ghost_ping(ctx, id):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(f'<@{id}>')
    await ctx.channel.purge(limit=1)

@client.command()
@commands.is_owner()
async def test_time(ctx):
    member = ctx.author
    if time.time() - member.created_at.timestamp() < 1619240429:
        await member.send('`You have been automatically banned because your account does not meet then minimum age.`')
    else:
        await member.send('test')

@client.event
async def on_message(message):
    global counting
    global last_user
    if message.author == client.user:
        return
    channel = message.channel
    if message.channel.id == 724550485742452820 or message.channel.id == 750447222360899685 or message.channel.id == 694008360239890495 or message.channel.id  == 731781244580397066 or message.channel.id == 717535356903227413 or message.channel.id == 717535357540892675:
        if 'auth failed' in message.content.lower():
            auth_failed = discord.Embed(title='Auth Failed', description='**Some causes of auth failed:**\n1. Entering wrong key or opening premium instead of regular.\n2. Not running as administrator.\n3. Computer or Internet is blocking the connection. Try opening script with vpn.\n4. Hwid needs to be reset. Depending on your subcription use the command .reset or .premium_reset in #hwid_reset\nWhen running the script if it says auth failed with no return message it is most likely error 3', color=discord.Color.purple())
            auth_failed.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
            await channel.send(embed=auth_failed)
        if 'good settings' in message.content.lower() or 'what settings' in message.content.lower() or 'what is timing' in message.content.lower() or 'what is gun timing' in message.content.lower() or 'how to use' in message.content.lower():
            good_settings = discord.Embed(title='Needed Game Settings', description='1. 85 field fo view\n2. Bordlerless Windowed (Otherwise script will freeze)\n3. If you\'re using auto detect User Interface Scale = 1\n\n To find good settings use the commands\n.show_all_configs | .show_config (config name) | .new_config', color=discord.Color.purple())
            good_settings.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
            await channel.send(embed=good_settings)

        if 'https://' in message.content.lower() or 'http://' in message.content.lower():
            if message.author.id == 208036172247728128 or message.author.id == 731231437478690856:
                pass
            else:
                await channel.purge(limit=1)
                mydb = mysql.connector.connect(
                    host=os.environ['HOST'],
                    user=os.environ['USER'],
                    passwd=os.environ['PASSWORD'],
                    database=os.environ['DATABASE'],
                )
                mycursor = mydb.cursor()
                mycursor.execute(f"INSERT INTO Warns VALUES ('NULL', '{message.author}', 'Sending links in a prohibited channel', 'Xeno Bot', '{message.author.id}')")
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
                mycursor.execute(f"SELECT * FROM Warns WHERE discord='{message.author}'")
                mycursor.fetchall()
                #member = client.get_user(author)

                embed = discord.Embed(title="Warning",description=f"\nName: <@{message.author.id}>\nReason: `Sending links in a prohibited channel`\nWarns: `{mycursor.rowcount}`\nWarner: <@731231437478690856>", color=discord.Color.purple())
                embed.set_author(name="Xeno", icon_url="https://cdn.discordapp.com/attachments/700994155945394246/742867155451772938/Xeno2-nobackground.gif")
                await message.author.send(embed=embed)
                embeded = await message.channel.send(embed=embed)
                await embeded.add_reaction(":nicecheckmark:742861250341502997")

                if mycursor.rowcount == 3:
                    embed = discord.Embed(title="Ban",description=f"\nName: <@{message.author.id}>\nReason: `Sending links in a prohibited channel`\nReason for ban: `Warned 3 times` ", color=discord.Color.purple())
                    embed.set_author(name="Xeno", icon_url="https://cdn.discordapp.com/attachments/700994155945394246/742867155451772938/Xeno2-nobackground.gif")
                    embeded = await message.channel.send(embed=embed)
                    await embeded.add_reaction(":nicecheckmark:742861250341502997")
                    await message.author.send(embed=embed)
                    await message.author.ban(reason='Sending links in a prohibited channel')
                
                mydb.commit()
                mycursor.close()
                mydb.close()
    if 'hey don\'t say that' in message.content.lower() or 'be nice' in message.content.lower() or 'clarkden is daddy' in message.content.lower():
        await message.add_reaction(":nicecheckmark:742861250341502997")

    if any(word in message.content.lower() for word in bad_words):
    #if  message.content.lower() in bad_words:
        await channel.purge(limit=1)
        #async with channel.typing():
            #await asyncio.sleep(3)
        #color = 0xeb4034
        hello = discord.Embed(description='Hey don\'t say that :)', color=0xeb4034)
        #hello.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
        await(await channel.send(embed=hello)).delete(delay=3)
        time.sleep(3)
        #await channel.purge(limit=1)
    #if 'license' in message.content.lower():
           # hello = discord.Embed(title='License', description='After purchasing your license will be delivered to you by @Clarkden when he is available.\nIf you haven\'t already, redeem your key to the redeem key channel to gain access to the User Discord.', color=discord.Color.purple())
            #hello.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
           # await channel.send(embed=hello)
    if message.channel.id == 724550485742452820 or message.channel.id  == 731781244580397066 or message.channel.id == 717535356903227413:
        if 'auth failed' in message.content.lower():
            auth_failed = discord.Embed(title='Auth Failed', description='**Some causes of auth failed:**\n1. Entering wrong key or opening premium instead of regular.\n2. Not running as administrator.\n3. Computer or Internet is blocking the connection. Try opening script with vpn.\n4. Hwid needs to be reset. Depending on your subcription use the command .reset or .premium_reset in #hwid_reset\nWhen running the script if it says auth failed with no return message it is most likely error 3', color=discord.Color.purple())
            auth_failed.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
            await channel.send(embed=auth_failed)
        if 'good settings' in message.content.lower() or 'what settings' in message.content.lower() or 'what is timing' in message.content.lower() or 'what is gun timing' in message.content.lower() or 'how to use' in message.content.lower():
            good_settings = discord.Embed(title='Needed Game Settings', description='1. 85 field fo view\n2. Bordlerless Windowed (Otherwise script will freeze)\n3. If you\'re using auto detect User Interface Scale = 1\n\n To find good settings use the commands\n.show_all_configs | .show_config (config name) | .new_config', color=discord.Color.purple())
            good_settings.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
            await channel.send(embed=good_settings)
    if message.channel.id  == 694008360239890495:
        if 'how do i buy' in message.content.lower() or 'how do i purchase' in message.content.lower() or 'what is the price' in message.content.lower() or 'is this free' in message.content.lower() or 'is this undetected' in message.content.lower()  or 'help' in message.content.lower() or 'i want to buy' in message.content.lower() or 'how much' in message.content.lower() or 'are there any slots' in message.content.lower() or 'how many slots' in message.content.lower() or 'how much does this cost' in message.content.lower():
                information_embed = discord.Embed(title='Information', description='**Xeno Information:**\n1. You can purchase on my website: https://xenoservices.xyz.\n2. Slots are limited and are not filled often and maybe not be filled again depending on the user base.\n3. Delivery is instant when purchasing on the website.\n4. This software has never been detected.\n5. For any extra need information please message the owner or moderator.', color=discord.Color.purple())
                information_embed.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
                await channel.send(embed=information_embed)
    if message.channel.id == 748596711747879062 or message.channel.id == 717535356903227413:
        if message.content.startswith('1') or message.content.startswith('2') or message.content.startswith('3') or message.content.startswith('4') or message.content.startswith('5') or message.content.startswith('6') or message.content.startswith('7') or message.content.startswith('8') or message.content.startswith('9'):
            user = message.author
            '''if user == last_user:
                banned_counters.append(user)
                last_user = ''
                counting = 0
                await message.add_reaction(":nologo:742796559896412161")
                await message.channel.send(f"`{message.author} messed up the count! You cannot say more than 1 number in a row!`")
                await message.channel.send("`Start at 1!`")
                if banned_counters.count(user) > 2:
                        await message.channel.send(f"`{user} has lost the ability to count!`")
                        role = discord.utils.get(message.channel.guild.roles, name = f"Counter")
                        await user.remove_roles(role)
            else:
                last_user = user'''
            try:
                currentCount = int(message.content)
                newcount = counting + 1
                if  currentCount == newcount:
                    counting += 1
                    await message.add_reaction(":nicecheckmark:742861250341502997")
                    if counting % 20 == 0:
                        if counting == 100:
                            pass
                        elif counting == 500:
                            pass
                        else:
                            await message.channel.send("`REMINDER! Whoever is the person to say 250 by counting from 1 wins a premium key.`")

                    if counting == 100:
                        await message.channel.send("`YAY 100`")
                    if counting == 250:
                        await message.channel.send(f"`YAY 250 {message.author} wins`")
                        channel = client.get_channel(694061907291930664)
                        await channel.send(f"`YAY 250 {message.author} wins`")
                        mydb = mysql.connector.connect(
    host=os.environ['HOST'],
    user=os.environ['USER'],
    passwd=os.environ['PASSWORD'],
    database=os.environ['DATABASE'],
)
                        #key = str(key)
                        mycursor = mydb.cursor()
                        mycursor.execute(f"SELECT * from license_giveaway where ID='1'")
                        redeemed = mycursor.fetchall()
                        if (redeemed):#[0]: #== 1:
                            for row in redeemed:
                                giveaway_license = row[1]
                            channel = client.get_channel(694061907291930664)
                            if str(giveaway_license) == '1':
                                mycursor.execute(f"DELETE from license_giveaway where ID='1'")
                                r = requests.post('https://api.c0gnito.cc/generate-keys', data={'privateKey':os.environ['PRIVATE_KEY_PREMIUM'], 'numberOfLicenses': '1', 'expiryTime':'0'})
                                before_keyword, keyword, after_keyword = r.text.partition('{\"success\":true,\"message\":\"Generated licenses.\",\"licenses\":[\"')
                                key = r.text.replace('{\"success\":true,\"message\":\"Generated licenses.\",\"licenses\":[\"', '')
                                key2 = key.split('\"]', 1)[0]

                                embed = discord.Embed(title="License",description=f"<@{message.author.id}>You have won the counting challenge.\n`{key2}`\nYou have been given a premium subscription. You can access the download to the script in the user discord. If you have any issues contact Clarkden.", color=discord.Color.red())
                                embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")

                                await message.author.send(embed=embed)
                                await channel.send(embed=embed)
                            else:
                                await message.channel.send("`There is no premium license to giveaway`")
                        else:
                            await message.channel.send("`There is no premium license to giveaway`")
                        mydb.commit()
                        mycursor.close()
                        mydb.close()
                        
                else:
                    purposely_messed_up = currentCount- newcount
                    if purposely_messed_up > 2:
                        await message.add_reaction(":nologo:742796559896412161")
                        await message.channel.send(f"`{message.author} messed up the count on purpose and has lost the ability to count!`")
                        await message.channel.send(f"`The count has been set back to the previous number! Next number is {newcount}`")      
                        role = discord.utils.get(message.channel.guild.roles, name = f"Counter")
                        await user.remove_roles(role)
                    else:
                        banned_counters.append(user)
                        last_user = ''
                        counting = 0
                        await message.add_reaction(":nologo:742796559896412161")
                        await message.channel.send(f"`{message.author} messed up the count!`")
                        await message.channel.send("`The next number is 1!`")
                        if banned_counters.count(user) > 1:
                            await message.channel.send(f"`{user} has lost the ability to count!`")
                            role = discord.utils.get(message.channel.guild.roles, name = f"Counter")
                            await user.remove_roles(role)

            except ValueError:
                await message.channel.purge(limit=1)
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
    embed.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")  
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


@client.command()
async def bot_commands(ctx):
    if ctx.channel.id == 694008360239890495:
        embed = discord.Embed(name="Error",description="This channel does not have access", color=discord.Color.red())
        await ctx.send(embed=embed)  
    else:
        embed = discord.Embed(title = 'Commands', description="1. Reset Hwid for Normal Key | .reset\n2. Reset Hwid for Premium Key | .premium_reset\n3. Get Download for script | .download\n4. Embed a message | .embed\n5. Suggest a feature or fix bug | .suggest\n6. Check Expiration on key | .expiration", color = discord.Color.green())
        embed.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
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
async def view(ctx, member: discord.Member = None):
    await ctx.channel.purge(limit=1)
    if ctx.channel.id == 740481635614720122:
        member = ctx.author if not member else member
        role = discord.utils.get(ctx.guild.roles, name = "Waiting For Role")
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
                    await member.send("https://mega.nz/file/bAtyXQyQ#EQuU1xxHDJdagiAAAoEkpUv6te3kt99UJOCYj4nDQEw")
                    channel = client.get_channel(694061907291930664)
                    await channel.send(f'`{member} downloaded Xeno v2.8`')
            else:   
                await member.send("Key not active or is expired")
                channel = client.get_channel(694061907291930664)
                await channel.send(f'`{member} tried to download Xeno but their key is not active or expired`')
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
async def poll(ctx, *, message):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(title='Poll', description=f'{message}\n\n-{ctx.author.mention}',  color=discord.Color.green())
    embed.set_author(name='Xeno', icon_url="https://media.discordapp.net/attachments/694061907291930664/748968125424205955/Xeno-discord-pfp.png?width=279&height=279")
    embeded = await ctx.channel.send(embed=embed)
    await embeded.add_reaction(":online:742849952568442960")
    await embeded.add_reaction(":offline:742850032688037973")


@client.command()
@commands.is_owner()
async def blacklist(ctx, idd):
    if idd == 208036172247728128:
            await ctx.channel.send("`You cannot warn Clarkden`")
    else:
        mydb = mysql.connector.connect(
            host=os.environ['HOST'],
            user=os.environ['USER'],
            passwd=os.environ['PASSWORD'],
            database=os.environ['DATABASE'])

        mycursor = mydb.cursor()
        mycursor.execute(f"INSERT INTO blacklist VALUES ('NULL', '{idd}')")
        mydb.commit()
        mycursor.close()
        mydb.close()

        embed = discord.Embed(description=f'<@{idd}> has been added to the blacklist',  color=discord.Color.purple())
        await ctx.channel.send(embed=embed)

    


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
@commands.has_role('team')
async def bot_embed(ctx, *, string):
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(description=f"{string}", color=discord.Color.red())
    embed.set_author(name=f"Xeno", icon_url=f"https://media.discordapp.net/attachments/695028034704769034/799354209211646002/unknown.jpeg")
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_role('Admin')
async def announcement(ctx, *, string):
    channel = ctx.message.channel
    embed = discord.Embed(title="Announcement",description=f"\n{string}\n\n-{ctx.author.mention}", color=discord.Color.red())
    embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    await channel.purge(limit=1)
    await ctx.send('||@everyone||')
    await ctx.send(embed=embed)

@client.command()
@commands.has_role('Admin')
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
            embed = discord.Embed(title="Config Error",description=f"The config named `{name}` could not be found", color=discord.Color.red())
            embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
            await ctx.channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel. Use <#731781244580397066> instead.", color = discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/703355033374162944/742836954248249445/5765_Offline.png")
        await ctx.send(embed=embed)


@client.command()
async def application_show(ctx, *, user_id):
    if ctx.author.id == 208036172247728128 or ctx.author.id == 519167807108415499:
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])

        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * from applications where user_id = '{user_id}'")
        config_get = mycursor.fetchall()
        configs = ""
        for row in config_get:
            configs+="| **Application Author: **"
            configs+=str(row[2])
            configs+=" |\n"
            configs+=" | **User ID: **"
            configs+=str(row[1])
            configs+=" |\n"
            configs+=" | **First name: **"
            configs+=str(row[3])
            configs+=" |\n"
            configs+=" | **Country: **"
            configs+=str(row[5])
            configs+=" |\n"
            configs+=" | **Occupation: **"
            configs+=str(row[7])
            configs+=" |\n"
            configs+=" | **Applying for: **"
            configs+=str(row[6])
            configs+=" |\n"
            configs+=" | **Extra Info: **"
            configs+=str(row[8])
            configs+=" |\n"
            configs+=" | **Cheats used: **"
            configs+=str(row[9])
            configs+=" |"
        #print(config_get, end=" ")
        embed = discord.Embed(title="Application",description=f"{configs}\n Applications User ID: `{row[1]}`", color=discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://media.discordapp.net/attachments/695028034704769034/799354209211646002/unknown.jpeg")
        log_channel = client.get_channel(700994155945394246)
        await log_channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()
    else:
        await ctx.channel.send("No perms")


@client.command()
async def website_users(ctx):
    if ctx.author.id == 208036172247728128 or ctx.author.id == 519167807108415499:
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])

        users = []

        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT username, status, script_sub, cheat_sub, spoofer_sub FROM users")
        #config_get = mycursor.fetchall()
        for row in config_get:
            configs = ""
            configs+="| **Username: **"
            configs+=str(row[0])
            configs+=" |"
            configs+="  **Status: **"
            configs+=str(row[1])
            configs+=" |"
            configs+="  **Script Subscription: **"
            configs+=str(row[2])
            configs+=" |"
            configs+="  **Cheat Subscription: **"
            configs+=str(row[3])
            configs+=" |"
            configs+="  **Spoofer Subscription: **"
            configs+=str(row[4])
            configs+=" |\n"
            #users.append[configs]
            embed = discord.Embed(description=f"{configs}", color=discord.Color.red())
        #embed.set_author(name=f'Xeno', icon_url=f"https://media.discordapp.net/attachments/695028034704769034/799354209211646002/unknown.jpeg")
            log_channel = client.get_channel(700994155945394246)
            await log_channel.send(embed=embed)
        #print(config_get, end=" ")
       # embed = discord.Embed(description=f"{configs}", color=discord.Color.red())
        #embed.set_author(name=f'Xeno', icon_url=f"https://media.discordapp.net/attachments/695028034704769034/799354209211646002/unknown.jpeg")
        #log_channel = client.get_channel(700994155945394246)
        #await log_channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()
    else:
        await ctx.channel.send("No perms")


@client.command()
async def application_accept(ctx, *, user_id):
    if ctx.author.id == 208036172247728128:
        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])

        mycursor = mydb.cursor()
        mycursor.execute(f"update users set status = '2' where user_id = '{user_id}'")
        config_get = mycursor.fetchall()
        #print(config_get, end=" ")
        embed = discord.Embed(title="Application Accepted",description=f"Applications User ID: `{user_id}`", color=discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://media.discordapp.net/attachments/695028034704769034/799354209211646002/unknown.jpeg")
        log_channel = client.get_channel(700994155945394246)
        await log_channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()


        mydb = mysql.connector.connect(
        host=os.environ['HOST'],
        user=os.environ['USER'],
        passwd=os.environ['PASSWORD'],
        database=os.environ['DATABASE'])

        mycursor = mydb.cursor()
        mycursor.execute(f"delete from applications where user_id = {user_id}'")
        mydb.commit()
        mycursor.close()
        mydb.close()
   


    else:
        await ctx.channel.send("No perms")


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
    embed = discord.Embed(title="Config Deleted",description=f"The config named `{name}` was deleted", color=discord.Color.red())
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
        embed = discord.Embed(title="All Configs",description=f"{configs}\n Total Configs: `{mycursor.rowcount}`", color=discord.Color.purple())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await ctx.channel.send(embed=embed)
        #time.sleep(5)
        mydb.commit()
        mycursor.close()
        mydb.close()
    else:
        embed = discord.Embed(title = 'Error', description = "Wrong Channel. Use <#731781244580397066> instead.", color = discord.Color.red())
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
            embed = discord.Embed(title="Config Error",description=f"The name `{name}` has been used already", color=discord.Color.red())
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
        embed = discord.Embed(title = 'Error', description = "Wrong Channel. Use <#731781244580397066> instead.", color = discord.Color.red())
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
@commands.has_role('Waiting For Role')
async def request_key(ctx, member: discord.Member = None):
    def checkmsg(m):
        return m.author == member

    def checkreact(reaction, user):
        return user.id == member.id and str(reaction.emoji) in ['✅', '❌']


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


@client.command()
@commands.is_owner()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name = "Intern")
    await member.remove_roles(role)

    role2 = discord.utils.get(ctx.guild.roles, name = "Muted")
    await member.add_roles(role2)

    embed = discord.Embed(description=f"<@{member.id}> `has been muted`")
    await ctx.channel.send(embed=embed)

@client.command()
@commands.is_owner()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name = "User")
    await member.add_roles(role)
    embed = discord.Embed(description=f"<@{member.id}> `has been unmuted`")
    await ctx.channel.send(embed=embed)

@client.command()
@commands.is_owner()
async def give_sub(ctx, length, member: discord.Member):
    print('1')
    await ctx.channel.purge(limit=1)
    length = str(length)
    sub_length = ''
    if 'week' in length:
        sub_length = '168'
    if 'month' in length:
        sub_length = '768'
    if 'lifetime' in length:
        sub_length = '0'

    if 'week' in length or 'month' in length or 'lifetime' in length:
        r = requests.post('https://api.c0gnito.cc/generate-keys', data={'privateKey':os.environ['PRIVATE_KEY'], 'numberOfLicenses': '1', 'expiryTime':f'{sub_length}'})
    else: 
        r = requests.post('https://api.c0gnito.cc/generate-keys', data={'privateKey':os.environ['PRIVATE_KEY_PREMIUM'], 'numberOfLicenses': '1', 'expiryTime':'0'})
    before_keyword, keyword, after_keyword = r.text.partition('{\"success\":true,\"message\":\"Generated licenses.\",\"licenses\":[\"')
    key = r.text.replace('{\"success\":true,\"message\":\"Generated licenses.\",\"licenses\":[\"', '')
    key2 = key.split('\"]', 1)[0]

    logs = client.get_channel(694061907291930664)

    if length == 'week':
        embed = discord.Embed(title="License",description=f"Your license has been generated by Clarkden.\n`{key2}`\nYou have been given a 1 week subscription. You can access the download to the script in the user discord. If you have any issues contact Clarkden.", color=discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await member.send(embed=embed)
        role = discord.utils.get(ctx.guild.roles, name = "Weekly User")
        role2 = discord.utils.get(ctx.guild.roles, name = "User")
        role3 = discord.utils.get(ctx.guild.roles, name = "Counter")
        role4 = discord.utils.get(ctx.guild.roles, name = "Waiting For Role")
        await member.remove_roles(role4)
        await member.add_roles(role, role2, role3)

        embed2 = discord.Embed(title="License",description=f"A license has been generated.\n`{key2}`\n{member.mention} has been given a 1 week subscription.", color=discord.Color.red())
        embed2.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await logs.send(embed=embed2)

    if length == 'month':
        embed = discord.Embed(title="License",description=f"Your license has been generated by Clarkden.\n`{key2}`\nYou have been given a 1 month subscription. You can access the download to the script in the user discord. If you have any issues contact Clarkden.", color=discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await member.send(embed=embed)
        role = discord.utils.get(ctx.guild.roles, name = "Monthly User")
        role2 = discord.utils.get(ctx.guild.roles, name = "User")
        role3 = discord.utils.get(ctx.guild.roles, name = "Counter")
        role4 = discord.utils.get(ctx.guild.roles, name = "Waiting For Role")
        await member.remove_roles(role4)
        await member.add_roles(role, role2, role3)

        embed2 = discord.Embed(title="License",description=f"A license has been generated.\n`{key2}`\n{member.mention} has been given a 1 month subscription.", color=discord.Color.red())
        embed2.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await logs.send(embed=embed2)

    if length == 'lifetime':
        embed = discord.Embed(title="License",description=f"Your license has been generated by Clarkden.\n`{key2}`\nYou have been given a lifetime subscription. You can access the download to the script in the user discord. If you have any issues contact Clarkden.", color=discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await member.send(embed=embed)
        role = discord.utils.get(ctx.guild.roles, name = "Lifetime User")
        role2 = discord.utils.get(ctx.guild.roles, name = "User")
        role3 = discord.utils.get(ctx.guild.roles, name = "Counter")
        role4 = discord.utils.get(ctx.guild.roles, name = "Waiting For Role")
        await member.remove_roles(role4)
        await member.add_roles(role, role2, role3)

        embed2 = discord.Embed(title="License",description=f"A license has been generated.\n`{key2}`\n{member.mention} has been given a lifetime subscription.", color=discord.Color.red())
        embed2.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await logs.send(embed=embed2)

    if length == 'premium':
        embed = discord.Embed(title="License",description=f"Your license has been generated by Clarkden.\n`{key2}`\nYou have been given a premium subscription. You can access the download to the script in the user discord. If you have any issues contact Clarkden.", color=discord.Color.red())
        embed.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await member.send(embed=embed)
        role = discord.utils.get(ctx.guild.roles, name = "Lifetime User")
        role2 = discord.utils.get(ctx.guild.roles, name = "User")
        role3 = discord.utils.get(ctx.guild.roles, name = "Counter")
        role4 = discord.utils.get(ctx.guild.roles, name = "Waiting For Role")
        role5 = discord.utils.get(ctx.guild.roles, name = "Premium")
        await member.remove_roles(role4)
        await member.add_roles(role, role2, role3, role5)

        embed2 = discord.Embed(title="License",description=f"A license has been generated.\n`{key2}`\n{member.mention} has been given a premium subscription.", color=discord.Color.red())
        embed2.set_author(name=f'Xeno', icon_url=f"https://cdn.discordapp.com/attachments/717535356903227416/742981932031148052/Xeno2-nobackground.gif")
        await logs.send(embed=embed2)
      

called_once_a_day.start()
client.run(os.environ['DISCORD_TOKEN'])
