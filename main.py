import os
import json
from dotenv import load_dotenv 
import logging
from interactions import Client, Intents, listen, Activity, ActivityType, Guild
from interactions.api.events import GuildJoin, Startup
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


@listen(GuildJoin)
async def on_guild_join(event: GuildJoin) -> None:
    # Total Guilds Joined
    num_guilds = len(bot.guilds)
    print("")
    logging.info(f"Servers Joined! Now in {num_guilds} server(s).\n")

    server_id = str(event.guild.id)
    json_file = 'Database/server_mod_customs.json'

    try:
        with open(json_file, 'r') as file:
            servers = json.load(file)
    except FileNotFoundError:
        logging.error("JSON File not found")

    if server_id not in servers:
        servers[server_id] = {
            'custom_ban_message': 'None',
            'custom_kick_message': 'None',
            'custom_timeout_message': 'None',
            'custom_soft_ban_message': 'None',
            'custom_warn_message': 'None',
            'custom_ban_message_dms': 'None',
            'custom_kick_message_dms': 'None',
            'custom_timeout_message_dms': 'None',
            'custom_soft_ban_message_dms': 'None',
            'custom_warn_message_dms': 'None',
        }
        with open(json_file, 'w') as file:
            json.dump(servers, file, indent=2)


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
