# Python imports
import logging
import datetime
import asyncio
# Third Party imports
from interactions import (
    Extension, slash_command, slash_option, 
    OptionType, InteractionContext, User, Permissions
)


class BasicMod(Extension):
    """Commands: kick, ban, soft_ban, warn, timeout\n
    Listeners: None\n
    Handlers: error_handler"""


    def __init__(self, bot):
        self.set_extension_error(self.error_handler)

    # Handy extension level error handler
    async def error_handler(self, error: Exception, ctx: InteractionContext):
        logging.error(f"Error in BasicMod: {error}")
        await ctx.send("An error occurred while processing the command. Please try again.")

 

# Kick
    @slash_command(
        name = 'kick',
        description = 'Kick the troublemakers',
        default_member_permissions= Permissions.KICK_MEMBERS
        )
    @slash_option(
        name = 'user', 
        description = "Who's being a pain?",
        required = True, 
        opt_type = OptionType.USER 
        )
    @slash_option(
        name = "reason",
        description = "Reason for kick",
        required= False,
        opt_type = OptionType.STRING
        )
    async def kick(self, ctx: InteractionContext, user: User = None, reason: str = "moderators thought so") -> None:
        try:
            if not ctx.guild.me.guild_permissions.KICK_MEMBERS:
                await ctx.send(f"I don't have the permission to do that, you must grant them to me")
                logging.warn("Bot doesn't have the required permissions.")
                return

            if user.top_role >= ctx.author.top_role:
                await ctx.send(f"Nuh uh, you don't get to kick **{user.display_name}**! They have more authority over you!")
                logging.warn("User has lower authority than the targeted user.")
                return

            await ctx.guild.kick(user.id, reason=reason)

            # await user.send(f"**YOU WERE KICKED FROM {ctx.guild.name}\nReason: **{reason}")
            
            server_name = ctx.guild.name
            user_name = user.display_name
            member_count = ctx.guild.member_count
            author_name = ctx.author.display_name
            await ctx.send(f"{user_name} has been yeeted out of {server_name}! \nBecause {reason}")
        
        except Exception as e:
            await self.error_handler(e, ctx)



# Ban
    @slash_command(
        name = 'ban',
        description = 'Ban the troublemakers',
        default_member_permissions= Permissions.BAN_MEMBERS
    )
    @slash_option(
        name = 'user', 
        description = "Who's being a pain?",
        required = True, 
        opt_type = OptionType.USER 
        )
    @slash_option(
        name = "reason",
        description = "Reason for ban",
        required= False,
        opt_type = OptionType.STRING
    )
    @slash_option(
        name = "clear",
        description="Clear messages from the user",
        required=False,
        opt_type=OptionType.INTEGER
    )

    async def ban(self, ctx: InteractionContext, user: User = None, reason: str = "moderators thought so", clear: int = 0) -> None:
        try:
            if not ctx.guild.me.guild_permissions.BAN_MEMBERS:
                await ctx.send(f"I don't have the permission to do that, you must grant them to me")
                logging.warn("Bot doesn't have the required permissions.")
                return

            if user.top_role >= ctx.author.top_role:
                await ctx.send(f"Nuh uh, you don't get to kick **{user.display_name}**! They have more authority over you!")
                logging.warn("User has lower authority than the targeted user.")
                return
            await ctx.guild.ban(user.id, reason=reason, delete_message_seconds=clear*60*60)

            # await user.send(f"**YOU WERE BANNED FROM {ctx.guild.name}\nReason: **{reason}")

            await ctx.send(f"{user.display_name} has been permanenetly yeeted out from Outer Haven! \nBecause {reason}")
        except Exception as e:
            await self.error_handler(e, ctx)



# unban 
    @slash_command(
        name = 'unban',
        description = 'Unban the changed souls',
        default_member_permissions= Permissions.BAN_MEMBERS
    )
    @slash_option(
        name = 'user', 
        description = "Who's got bail?",
        required = True, 
        opt_type = OptionType.USER 
    )
    async def unban(self, ctx: InteractionContext, user: User = None) -> None:
        try:
            if not ctx.guild.me.guild_permissions.BAN_MEMBERS:
                await ctx.send(f"I don't have the permission to do that, you must grant them to me")
                logging.warn("Bot doesn't have the required permissions.")
                return
            await ctx.guild.unban(user.id)
            await ctx.send(f"{user.display_name} has been bailed out of the ban list!")
        except Exception as e:
            await self.error_handler(e, ctx)



#softban
    @slash_command(
        name = 'softban',
        description = 'Temporarily ban the troublemakers',
        default_member_permissions= Permissions.BAN_MEMBERS
    )
    @slash_option(
        name = 'user', 
        description = "Who's being a pain?",
        required = True, 
        opt_type = OptionType.USER 
    )
    @slash_option(
        name="duration",
        description="For how long?",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name = "reason",
        description = "Reason for soft ban",
        required= True,
        opt_type = OptionType.STRING
    )
    async def softban(self, ctx: InteractionContext, user: User = None, duration: str = None, reason: str = "moderators thought so") -> None:
        try:
            if not ctx.guild.me.guild_permissions.BAN_MEMBERS:
                await ctx.send(f"I don't have the permission to do that, you must grant them to me")
                logging.warn("Bot doesn't have the required permissions.")
                return

            if user.top_role >= ctx.author.top_role:
                await ctx.send(f"Nuh uh, you don't get to ban {user.display_name}!")
                return
            if duration.lower() == "forever":
                await ctx.guild.ban(user.id, reason=reason)
                await ctx.send(f"{user.display_name} has been temporarily banned!\nReason: {reason}")
                return
            time = unit = ''
            for i in duration:
                if i.isdigit():
                    time += i
                elif i.isalpha():
                    unit += i

            if unit.lower() == 'd' or unit.lower() == 'day' or unit.lower() == 'days':
                duration_seconds = int(time) *24*60*60
            elif unit.lower() == 'm' or unit.lower() == 'month' or unit.lower() == 'months':
                duration_seconds = int(time) *30*24*60*60  
            elif unit.lower() == 'h' or unit.lower() == 'hour' or unit.lower() == 'hours':
                duration_seconds = int(time) *60*60
            elif unit.lower() == 'min' or unit.lower() == 'minute' or unit.lower() == 'minutes':
                duration_seconds = int(time) *60
            elif unit.lower() == 'w' or unit.lower() == 'week' or unit.lower() == 'weeks':
                duration_seconds = int(time) * 7*24*60*60
            elif unit.lower() == 'y' or unit.lower() == 'year' or unit.lower() == 'years':
                duration_seconds = int(time) *365*24*60*60  
            else:
                await ctx.send("Wrong duration value")
                return

            await ctx.guild.ban(user.id, reason=reason)
            await ctx.send(f"{user.display_name} has been temporarily banned for {duration}!\nReason: {reason}")
            await asyncio.sleep(duration_seconds)
            await ctx.guild.unban(user.id)
            await ctx.send(f"{user.display_name} has been bailed out of the ban list after {duration}!")
        except Exception as e:
            await self.error_handler(e, ctx)



# Warn
    @slash_command(
        name = 'warn',
        description = 'Warn someone for being a pain',
        default_member_permissions= Permissions.MODERATE_MEMBERS
    )
    @slash_option(
        name = 'user', 
        description = "Who's being a pain?",
        required = True, 
        opt_type = OptionType.USER 
    )
    @slash_option(
        name = "warning",
        description = "What's the warning",
        required= True,
        opt_type = OptionType.STRING
    )

    async def warn(self, ctx:InteractionContext, user:User = None, warning: str=None)->None:
        try:
            await user.send(f"**YOU HAVE BEEN WARNED IN {ctx.guild.name}**\n**Reason:**\n{warning}")
            await ctx.send(f"{user.mention} has been warned\n**Reason:** {warning}")
        except Exception as e:
            await self.error_handler(e, ctx)
    


# purge
    @slash_command(
        name = 'purge',
        description = "Delete messages to clean up the chat",
        default_member_permissions= Permissions.MANAGE_MESSAGES
    )
    @slash_option(
        name = 'number', 
        description = "How many messages to obliterate",
        required = True, 
        opt_type=OptionType.INTEGER
    )
    @slash_option(
        name = "user",
        description = "Delete messages from a specific user",
        required= False,
        opt_type = OptionType.USER
    )
    async def purge(self, ctx: InteractionContext, number: int = None, user: User = None) -> None:
        try:
            await ctx.channel.purge(deletion_limit=number)
            await ctx.send(f"{number} messages have been purged{' from ' + user.display_name if user else ''}.", ephemeral=True)
        except Exception as e:
            await self.error_handler(e, ctx)