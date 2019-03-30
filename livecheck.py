import discord
import random, cfg, twitch_stuff
import asyncio, logging, datetime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler('discordbot.log', mode='w')
formatter = logging.Formatter('''%(asctime)s -
                              %(name)s - %(levelname)s - %(message)s''')
handler.setFormatter(formatter)
logger.addHandler(handler)


TOKEN = cfg.D_TOKEN


twitchid = twitch_stuff.get_user_id('emongg')
print(twitchid)
if twitchid==False:
    print('no id')
    have_id = False
else:
    have_id = True

if have_id:
    live_check = twitch_stuff.get_status(twitchid)


client = discord.Client()


async def check_live():
    global live_check
    while True:
        currentDT = str(datetime.datetime.now())
        try:
            new_check = twitch_stuff.get_status(twitchid)
        except:
            continue
        if new_check == True:
            if live_check == False:
                try:
                    logger.info('posting message at ' + currentDT)
                    message = "@everyone emongg is live https://twitch.tv/emongg"
                    await client.send_message(discord.Object(id='422170422516121612'), message)
                except:
                    logger.exception('error posting message: ')
            elif live_check == True:
                logger.info('still live as of ' + currentDT)
                pass
            else:
                print('something broke. live_check = ', live_check)
            live_check = new_check
        elif new_check == False:
            logger.info('not live as of ' + currentDT)
            live_check = new_check
            pass
        else:
            print('something broke. new_check = ', new_check)
        await asyncio.sleep(60)


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="\"Life? Don't talk to me about life.\""))
    print("Logged in as " + client.user.name)


try:
    if have_id:
        print('creating loop')
        client.loop.create_task(check_live())
    client.run(TOKEN)
except:
    logger.exception("message:")
