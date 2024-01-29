import logging
import json
from interactions import Extension, Modal, ShortText, slash_command, InteractionContext, subcommand, ParagraphText, StringSelectMenu, StringSelectOption, ActionRow, Button, ButtonStyle, Embed, Color, component_callback, ComponentContext

# server_id,custom_ban_message_dms,custom_kick_message_dms,custom_timeout_message_dms,custom_soft_ban_message_dms,custom_warn_message_dms

# server_id,custom_ban_message_dms,custom_kick_message_dms,custom_timeout_message_dms,custom_soft_ban_message_dms,custom_warn_message_dms


class BasicMod(Extension):
    def __init__(self, bot):
        self.set_extension_error(self.error_handler)

    async def error_handler(self, error: Exception, ctx: InteractionContext):
        logging.error(f"Error in BasicMod: {error}")
        await ctx.send("An error occurred while processing the command. Please try again.")

    
    @slash_command(name = "Customize",
                   description = "Customize various responses!",
                   sub_cmd_name = "Kick",
                   sub_cmd_description = "Customize Kick Command!"
                   )
    
    async def customize_kick(ctx: InteractionContext):
        
        json_file = 'Database/server_mod_customs.json'

        with open(json_file, 'r') as file:
            server = json.load(file)

        server_id = ctx.guild_id
        
        custom_kick_message = server[server_id]["custom_kick_message"]
        custom_kick_message_dms = [server_id]["custom_kick_message_dms"]
        
