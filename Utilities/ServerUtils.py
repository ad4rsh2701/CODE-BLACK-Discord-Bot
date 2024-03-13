# Python imports
import logging

# Third Party imports
from interactions import (
    Extension, slash_command, slash_option, 
    OptionType, InteractionContext, User, Permissions,
    SlashCommandChoice
)


# Auto Response

class ServerUtils(Extension):
    """Commands: /create auto response, /delete auto response, /modify auto response\n
    Listeners: None\n
    Handlers: error_handler"""


    def __init__(self, bot):
        self.set_extension_error(self.error_handler)

    # Handy extension level error handler
    async def error_handler(self, error: Exception, ctx: InteractionContext):
        logging.error(f"Error in ServerUtils: {error}")
        await ctx.send("An error occurred while processing the command. Please try again.")

    
# auto re    
    slash_command(
        name='auto_re',
        description='auto responder',
    )
    @slash_option(
            name="trigger",
            opt_type=str,
            description="Enter the word/sentence Ms. Haven will respond to!",
            required=True
    )
    @slash_option(
        name="type",
        description="The type of auto responder to be created... same, loose, precise",
        opt_type=str,
        required=True,
        autocomplete=True,
        choices=[SlashCommandChoice(name="Same", value=4),
                 SlashCommandChoice(name="Exact", value=5),
                 SlashCommandChoice(name="Loose", value=6)]
    )
    @slash_option(
        name="rule",
        description="Would you like to add some 'rules', as to when Ms. Haven will respond.",
        opt_type=str,
        autocomplete=True,
        choices= [SlashCommandChoice(name="Send once in 5 times", value=1),
                  SlashCommandChoice(name="Send only when used by {user}", value=2),
                  SlashCommandChoice(name="Send only when not used by {user}", value=3)]
    )
    async def auto_response(self, ctx: InteractionContext) -> None:
        await ctx.send("yep, works so far!")