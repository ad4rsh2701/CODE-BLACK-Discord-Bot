import os
import json
from dotenv import load_dotenv 
import logging
from interactions import Client, Intents, listen, Activity, ActivityType, Guild
from interactions.api.events import Startup
# Configuring logging cuz why not
logging.basicConfig(level=logging.INFO)


bot = Client(intents=Intents.ALL, send_command_tracebacks=False)


@listen(Startup)
async def on_startup() -> None:
    logging.debug("on_startup function is called. Setting up Ms. Haven's initial state.")

    activity = Activity.create(
        name="Cavetown",
        type=ActivityType.LISTENING
    )
    await bot.change_presence(activity=activity)



load_dotenv()
bot_token = os.environ.get("BOT_TOKEN")
if not bot_token:
    logging.error("Bot token is missing. Please set the BOT_TOKEN environment variable.")
    exit(1)


extensions = [
    "Fun.Confessions",
    "Fun.XPSystem",
    "Moderation.AdvanceMod",
    "Moderation.BasicMod",
    "Moderation.CustomMod",
    "Moderation.ModLog",
    "Utilities.ChannelUtils",
    "Utilities.ServerUtils",
]

for index, extension in enumerate(extensions, start=1): 
    try:
        logging.info(f"Loading extension {index}: {extension}")
        bot.load_extension(extension)
        logging.info(f"Extension {index}: {extension} loaded successfully.\n")

    except Exception as e:
        logging.error(f"Extension {index}: {extension} failed to load. Error: {e}\n")

try:
    logging.debug("Ms. Haven is starting...")
    bot.start(bot_token)
except KeyboardInterrupt:
    bot.close()
    logging.info("Bot terminated by user.")
except Exception as e:
    logging.error(f"An error occurred during bot startup: {e}")
