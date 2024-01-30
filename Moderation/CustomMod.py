import logging
import traceback
import json
from interactions import Extension, Modal, ShortText, slash_command, InteractionContext, subcommand, ParagraphText, StringSelectMenu, StringSelectOption, ActionRow, Button, ButtonStyle, Embed, Color, component_callback, ComponentContext, listen
from Resources.CustomEmojis import *
from interactions.api.events import GuildJoin
# server_id,custom_ban_message_dms,custom_kick_message_dms,custom_timeout_message_dms,custom_soft_ban_message_dms,custom_warn_message_dms

# server_id,custom_ban_message_dms,custom_kick_message_dms,custom_timeout_message_dms,custom_soft_ban_message_dms,custom_warn_message_dms


class CustomMod(Extension):
    def __init__(self, bot):
        self.set_extension_error(self.error_handler)

    async def error_handler(self, error: Exception, ctx: InteractionContext):
        logging.error(f"Error in CustomMod: {error}")
        traceback.print_exc()
        await ctx.send("An error occurred while processing the command. Please try again.")


    @listen(GuildJoin)
    async def on_guild_join(self, event: GuildJoin) -> None:

        server_id = str(event.guild.id)
        json_file = 'CODE-BLACK-Discord-Bot/Database/server_mod_customs.json'

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
                "dm_on_ban": "False",
                'custom_kick_message_dms': 'None',
                "dm_on_kick": "False",
                'custom_timeout_message_dms': 'None',
                'custom_soft_ban_message_dms': 'None',
                'custom_warn_message_dms': 'None',
            }
            with open(json_file, 'w') as file:
                json.dump(servers, file, indent=2)




# customise kick    
    @slash_command(name = "customize",
                   description = "Customize various responses!",
                   sub_cmd_name = "kick",
                   sub_cmd_description = "Customize Kick Command!"
                   )
    async def customize_kick(self, ctx: ComponentContext):
        try:    
            json_file = 'CODE-BLACK-Discord-Bot/Database/server_mod_customs.json'

            with open(json_file, 'r') as file:
                servers = json.load(file)

            server_id = str(ctx.guild_id)

            custom_kick_message = servers[server_id]["custom_kick_message"]
            dm_on_kick = servers[server_id]["dm_on_kick"]
            custom_kick_message_dms = servers[server_id]["custom_kick_message_dms"]

            print(f"server_id: {server_id}")
            print(f"custom_kick_message: {custom_kick_message}")
            print(f"dm_on_kick: {dm_on_kick}")
            print(f"custom_kick_message_dms: {custom_kick_message_dms}")


            if custom_kick_message == "None":
                option_type = f"{disabled_check}{enabled_cross}"
            else:
                option_type = f"{enabled_check}{disabled_cross}"
            if dm_on_kick == "False":
                option_type = f"{disabled_check}{enabled_cross}"
                sub_option_type = f"{disabled_check}{disabled_cross}"
            else:
                option_type = f"{enabled_check}{disabled_cross}"
                sub_option_type = f"{disabled_check}{enabled_cross}"
                if custom_kick_message_dms != "None":
                    sub_option_type = f"{enabled_check}{disabled_cross}"
        
            customize_kick_command_embed = Embed(
                title = "Customize the Kick Command!",
                description = f"Here are the current configurations for the \n`Kick Command` in **{ctx.guild.name}**\n\u200b",
                color = Color.from_hex("#000000")
            )
            customize_kick_command_embed.add_field(
                name = f"> Custom Kick Message          {option_type}",
                value= "Have me send a message of your choice \nwhen a user is kicked!\n\u200b"
            )
            customize_kick_command_embed.add_field(
                name = f"> DM User on Kick                     {option_type}",
                value= "Have me send some Direct Message(DM)\nto a user when they are kicked!\n\u200b"
            )
            customize_kick_command_embed.add_field(
                name = f"> Custom DM Kick Message   {sub_option_type}",
                value= "Have me send Direct Message(DM) of your choice\nto a user when they are kicked!"
            )
            customize_kick_command_embed.add_field(
                name = "\u200b",
                value ="Select the modifications you want to apply\nusing the drop down below."
            )
            # TODO: Make the drop down dynamic
            options = [
                StringSelectOption(label="option 1", value="1"),
                StringSelectOption(label="option 2", value="2"),
                StringSelectOption(label="option 3", value="3")
            ]
            kick_customs_menu = StringSelectMenu(
                *options,          
                custom_id= 'kick_custom_list',
                placeholder= 'Select a modification!',
                max_values=1, min_values=1)
            
            await ctx.send(embeds=customize_kick_command_embed, components=kick_customs_menu)

        except Exception as e:
            await self.error_handler(e, ctx)
