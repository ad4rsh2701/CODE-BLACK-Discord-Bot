import logging
import traceback
import json
from interactions import Extension, component_callback, Modal, ShortText, slash_command, InteractionContext, subcommand, ParagraphText, StringSelectMenu, StringSelectOption, ActionRow, Button, ButtonStyle, Embed, Color, component_callback, ComponentContext, listen
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

            global kick_list_value
            global dm_kick_list_value
            global dm_kick_custom_list_value
            
            if custom_kick_message == "None":
                option_type = f"{disabled_check}{enabled_cross}"
                kick_list_value = "Enable"
                
            else:
                option_type = f"{enabled_check}{disabled_cross}"
                kick_list_value = "Disable"
            if dm_on_kick == "False":
                option_type = f"{disabled_check}{enabled_cross}"
                sub_option_type = f"{disabled_check}{disabled_cross}"   
                dm_kick_list_value = "Enable"
            
            else:
                option_type = f"{enabled_check}{disabled_cross}"
                sub_option_type = f"{disabled_check}{enabled_cross}"
                dm_kick_list_value = "Disable"
                dm_kick_custom_list_value = "Enable"
                
                if custom_kick_message_dms != "None":
                    sub_option_type = f"{enabled_check}{disabled_cross}"
                    dm_kick_custom_list_value = "Disable"
        
            customize_kick_command_embed = Embed(
                title = "Customize the Kick Command!",
                description = f"Here are the current configurations for the \n`Kick Command` in **{ctx.guild.name}**\n\u200b",
                color = Color.from_hex("#000000")
            )
            customize_kick_command_embed.add_field(
                name = f"> Custom Kick Message           {option_type}",
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
            if dm_on_kick == "False":
                options = [
                    StringSelectOption(label=f"{kick_list_value} Custom Kick Message", value= "1"),
                    StringSelectOption(label=f"{dm_kick_list_value} DM User on Kick", value= 4)
                ]
            else:
                options = [
                    StringSelectOption(label=f"{kick_list_value} Custom Kick Message", value= 1),
                    StringSelectOption(label=f"{dm_kick_list_value} DM User on Kick", value= 2),
                    StringSelectOption(label=f"{dm_kick_custom_list_value} Custom DM Kick Message", value= 3)
                ]
            
            kick_customs_menu = StringSelectMenu(
                *options,          
                custom_id= 'kick_custom_list',
                placeholder= 'Select a modification!',
                max_values=1, min_values=1)
            
            global kick_custom_modal
            kick_custom_modal = Modal(
                ParagraphText(
                    label="Enter your kick message!",
                    custom_id="text_kick_custom",
                    value = "Code words:\n1. {server_name} : Name of the server\n"\
                        "2. {user_name} : Name of user\n"\
                        "3. {member_count} : Number of Server Members\n"\
                        "4. {author_name} : Name of the user who used the command\n"\
                            "All markdowns available in discord work.\n\n"\
                                "Example Text: Aaaand Yeetus Burgertus people! **{user_name}** has been kicked from {server_name}! That leaves us with {member_count} peeps!",),
                title="Customize Kick!",    
                custom_id="kick_custom_model",
            )

            await ctx.send(embeds=customize_kick_command_embed, components=kick_customs_menu, ephemeral= True)
        
        except Exception as e:
            await self.error_handler(e, ctx)

    @component_callback("kick_custom_list")
    async def kick_custom_list(self, ctx: ComponentContext):
        selected_option = ctx.values[0]
        if selected_option == "1" and kick_list_value == "Enable":
            await ctx.send_modal(modal = kick_custom_modal)
            # TODO: Make an option for embed messages and stuff for other options