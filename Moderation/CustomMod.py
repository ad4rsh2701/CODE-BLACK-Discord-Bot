# Python imports
import logging
import json
from os import environ

# Third Party imports
from dotenv import load_dotenv
from interactions.api.events import GuildJoin
from interactions import (
    ActionRow, Button, ButtonStyle, Color, ComponentContext, Embed,
    Extension, InteractionContext, Modal, ParagraphText, StringSelectMenu,
    StringSelectOption, component_callback, listen, slash_command
)

# "stuff I made for the sake of modularity" imports (aka Local imports)
from Resources.CustomEmojis import *


# loading environment variables from .env (refer README.md)
load_dotenv()
PATH = environ.get("MOD_DATABASE_PATH")

# stuff in database file (for my reference)
#   server_id,custom_ban_message_dms,custom_kick_message_dms,custom_timeout_message_dms,custom_soft_ban_message_dms,custom_warn_message_dms


class CustomMod(Extension):
    """Commands: customize kick, customize ban, customize warn, customize timeout\n
    Listeners: on_guild_join\n 
    Handlers: error_handler"""


    def __init__(self, bot):
        self.set_extension_error(self.error_handler)
        
        # Variables
        # These variables are solely present to make building embeds easier
        self.custom_message = ""
        self.dm_user = ""
        self.custom_dm_user = ""

        # Modals
        self.kick_custom_modal = Modal(
            ParagraphText(
                label="Special Words (Do not fill this)",
                custom_id="special_words_text",
                placeholder="1. {server_name}: Server\n2. {user_name}: User\n3. {member_count}: Members\n4. {author_name}: Author",
                required = False
            ),
            ParagraphText(
                label="Example (Do not fill this)",
                custom_id="example_text",
                placeholder="e.g.**{user_name}** has been kicked from {server_name}! That leaves us with {member_count} peeps!",
                required=False
            ),
            ParagraphText(
                label="Your Custom Message (FILL THIS)",
                custom_id="custom_kick_text",
                placeholder="All discord markdowns work!",
                required=True
            ),
            title="Customize Kick!",    
            custom_id="kick_custom_model",
        )
        
        self.ban_custom_modal = Modal(
            ParagraphText(
                label="Special Words (Do not fill this)",
                custom_id="special_words_text",
                placeholder="1. {server_name}: Server\n2. {user_name}: User\n3. {member_count}: Members\n4. {author_name}: Author",
                required = False
            ),
            ParagraphText(
                label="Example (Do not fill this)",
                custom_id="example_text",
                placeholder="e.g.**{user_name}** has been banned from {server_name}! That leaves us with {member_count} peeps!",
                required=False
            ),
            ParagraphText(
                label="Your Custom Message (FILL THIS)",
                custom_id="custom_ban_text",
                placeholder="All discord markdowns work!",
                required=True
            ),
            title="Customize Ban!",    
            custom_id="ban_custom_model", 
        )
        
        self.warn_custom_modal = Modal(
            ParagraphText(
                label="Special Words (Do not fill this)",
                custom_id="special_words_text",
                placeholder="1. {server_name}: Server\n2. {user_name}: User\n3. {author_name}: Author",
                required = False
            ),
            ParagraphText(
                label="Example (Do not fill this)",
                custom_id="example_text",
                placeholder="e.g.**{user_name}** has been warned {server_name}! By the courtasy of {author_name}",
                required=False
            ),
            ParagraphText(
                label="Your Custom Message (FILL THIS)",
                custom_id="custom_ban_text",
                placeholder="All discord markdowns work!",
                required=True
            ),
            title="Customize Ban!",    
            custom_id="ban_custom_model",             
        )


    # For determining switch modes
    # switch and sub_switch here implies check and cross emojis, think of it like an actual switch indicating whether a feature is enabled or not
    def switch_mode(self, custom_message: str, dm_user: str, custom_dm_user: str):
        """Set customization switches based on the values."""

        self.custom_message = "Enable" if custom_message == "None" else "Disable"
        switch = f"{disabled_check}{enabled_cross}" if self.custom_message == "Enable" else f"{enabled_check}{disabled_cross}"

        if dm_user == "False":
            self.dm_user = "Enable"  # letting the user know that they can enable this
            sub_switch = f"{disabled_check}{disabled_cross}"
        else:
            self.dm_user = "Disable" # letting the user know that they can disable this
            sub_switch = f"{disabled_check}{enabled_cross}"
            self.custom_dm_user = "Enable" if custom_dm_user != "None" else "Disable"

        return switch, sub_switch


    # Handy extension level error handler
    async def error_handler(self, error: Exception, ctx: InteractionContext):
        logging.error(f"Error in CustomMod: {error}")
        await ctx.send("An error occurred while processing the command. Please try again.")


    # Everytime the bot starts, it will check the database
    @listen(GuildJoin)
    async def on_guild_join(self, event: GuildJoin) -> None:
        """Listens for servers the bot is active in after it's started."""

        server_id = str(event.guild.id)
        try:
            # Open the database file with both the reading and writing powers
            with open(PATH, 'r+') as file:
                servers = json.load(file)
                
                if server_id not in servers:
                    servers[server_id] = {
                        'custom_ban_message': 'None',
                        'custom_kick_message': 'None',
                        'custom_timeout_message': 'None',
                        'custom_soft_ban_message': 'None',
                        'custom_warn_message': 'None',
                        'custom_ban_message_dms': 'None',
                        "dm_on_ban": "False",
                        'custom_kick_message_dms': 'None',
                        "dm_on_kick": "False",
                        'custom_timeout_message_dms': 'None',
                        'custom_soft_ban_message_dms': 'None',
                        'custom_warn_message_dms': 'None'
                    }

                    # Go back to the beginning of the file before writing
                    file.seek(0)

                    try:
                        json.dump(servers, file, indent=2)
                    except Exception as error:
                        logging.error(f"Error in CustomMod: {error}")
                        await event.bot.send("An error occurred while processing the command. Please try again.")

        except FileNotFoundError:
            logging.error(f"JSON File not found {PATH}")


# customise kick
    @slash_command(name = "customize",
                   description = "Customize various responses!",
                   sub_cmd_name = "kick",
                   sub_cmd_description = "Customize Kick Command!"
                   )
    async def customize_kick(self, ctx: ComponentContext) -> None:
        try:

            with open(PATH, 'r') as file:
                servers = json.load(file)

            server_id = str(ctx.guild_id)

            custom_kick_message = servers[server_id]["custom_kick_message"]
            dm_on_kick = servers[server_id]["dm_on_kick"]
            custom_kick_message_dms = servers[server_id]["custom_kick_message_dms"]
            
            # Getting switch and sub_switch values
            switch, sub_switch = self.switch_mode(custom_kick_message, dm_on_kick, custom_kick_message_dms)

            # Building embed
            customize_kick_command_embed = Embed(
                title = "Customize the Kick Command!",
                description = f"Here are the current configurations for the \n`Kick Command` in **{ctx.guild.name}**\n\u200b",
                color = Color.from_hex("#000000")
            )
            customize_kick_command_embed.add_field(
                name = f"> Custom Kick Message           {switch}",
                value= "Have me send a message of your choice \nwhen a user is kicked!\n\u200b"
            )
            customize_kick_command_embed.add_field(
                name = f"> DM User on Kick                     {switch}",
                value= "Have me send some Direct Message(DM)\nto a user when they are kicked!\n\u200b"
            )
            customize_kick_command_embed.add_field(
                name = f"> Custom DM Kick Message   {sub_switch}",
                value= "Have me send Direct Message(DM) of your choice\nto a user when they are kicked!"
            )
            customize_kick_command_embed.add_field(
                name = "\u200b",
                value ="Select the modifications you want to apply\nusing the drop down below."
            )

            # building select menu options
            common_options = [
                StringSelectOption(label=f"{self.custom_message} Custom Kick Message", value="1"),
                StringSelectOption(label=f"{self.dm_user} DM User on Kick", value="4")
            ]

            if dm_on_kick != "False":
                common_options.append(
                    StringSelectOption(label=f"{self.custom_dm_user} Custom DM Kick Message", value="3")
                )
            options = common_options
            
            # Building the select menu
            kick_customs_menu = StringSelectMenu(
                *options,          
                custom_id= 'kick_custom_list',
                placeholder= 'Select a modification!',
                max_values=1, min_values=1)

            # Sending the embed with the dynamic select menu
            await ctx.send(embeds=customize_kick_command_embed, components=kick_customs_menu, ephemeral= True)
        
        except Exception as e:
            await self.error_handler(e, ctx)

    @component_callback("kick_custom_list")
    async def kick_custom_list(self, ctx: ComponentContext):
        selected_option = ctx.values[0]
        if selected_option == "1" and self.custom_message == "Enable":
            await ctx.send_modal(modal = self.kick_custom_modal)