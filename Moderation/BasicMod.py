import logging
from interactions import Extension, slash_command, slash_option, OptionType, InteractionContext, User, Permissions


class BasicMod(Extension):
    def __init__(self, bot):
        self.set_extension_error(self.error_handler)

    async def error_handler(self, error: Exception, ctx: InteractionContext):
        logging.error(f"Error in BasicMod: {error}")
        await ctx.send("An error occurred while processing the command. Please try again.")

 

# Kick
    @slash_command(
        name = 'kick',
        description = 'Yeet the naughty kids!',
        default_member_permissions= Permissions.KICK_MEMBERS
        )
    @slash_option(
        name = 'user', 
        description = "Who's being naughty?",
        required = True, 
        opt_type = OptionType.USER 
        )
    @slash_option(
        name = "reason",
        description = "..and why do you think so?",
        required= True,
        opt_type = OptionType.STRING
        )
    async def kick(self, ctx: InteractionContext, user: User = None, reason: str = None) -> None:
        try:
            if not ctx.guild.me.guild_permissions.KICK_MEMBERS:
                await ctx.send(f"I don't have the permission to do that sweety!")
                logging.warn("Bot doesn't have the required permissions.")
                return

            if user.top_role >= ctx.author.top_role:
                await ctx.send(f"Nuh uh, you don't get to kick **{user.display_name}**! They have more authority over you!")
                logging.warn("User has lower authority than the targeted user.")
                return

            await ctx.guild.kick(user.id, reason=reason)
            await ctx.send(f"{user.display_name} has been yeeted out from Outer Haven! Because {reason}")
        
        except Exception as e:
            await self.error_handler(e, ctx)
        
# Ban
    @slash_command(
        name = 'ban',
        description = 'Permanently yeet the naughty kids!'
    )
    @slash_option(
        name = 'user', 
        description = "Who's being naughty?",
        required = True, 
        opt_type = OptionType.USER 
        )
    @slash_option(
        name = "reason",
        description = "..and why do you think so?",
        required= True,
        opt_type = OptionType.STRING
        )
    async def ban(self, ctx: InteractionContext, user: User = None, reason: str = None) -> None:
        try:
            await ctx.guild.ban(user.id, reason=reason)
            await ctx.send(f"{user.display_name} has been permanenetly yeeted out from Outer Haven! Because {reason}")
        except Exception as e:
            await self.error_handler(e, ctx)