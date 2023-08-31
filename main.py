import discord
from discord.ext import commands
from keep_alive import keep_alive

ticket_types = {
    "staff_application": {
        "emoji": "🔮",
        "description": "Apply for a staff position in our community.",
        "message": "Hello! Please provide details about your experience and why you want to join our staff team.",
    },
    "media_application": {
        "emoji": "📷",
        "description": "Apply for a media-related role (make sure to read #ranks before creating a ticket).",
        "message": "Hello! Please provide the video in which you got above 10k views.",
    },
    "bug_finding": {
        "emoji": "🐛",
        "description": "Report bugs and issues you have encountered for in-game rewards.",
        "message": "Hello! Please provide detailed information about the bug or issue you have encountered.",
    },
    "general_support": {
        "emoji": "📞",
        "description": "General support or questions about our services.",
        "message": "Hello! Please describe your support request or ask any questions you may have.",
    },
    "player_reporting": {
        "emoji": "🚩",
        "description": "Report a player for violations or misconduct.",
        "message": "Hello! Please provide evidence and detailed information about the player you are reporting.",
    },
    "ban_appeals": {
        "emoji": "⛔",
        "description": "Submit an appeal if you have been banned.",
        "message": "Hello! Please explain the situation and provide any relevant details for your ban appeal.",
    },
}

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="Ticket System",
        description="React with the corresponding emoji to create a ticket:",
    )

    for ticket_type, data in ticket_types.items():
        embed.add_field(
            name=f"{data['emoji']} - {ticket_type.replace('_', ' ').title()}",
            value=data["description"],
            inline=False,
        )

    message = await ctx.send(embed=embed)
    for ticket_type, data in ticket_types.items():
        await message.add_reaction(data["emoji"])


@bot.command()
async def rules(ctx):
    # Specify the channel where you want to send the rules embed
    channel_id = 1126043196506525746  # Replace with the actual channel ID

    # Fetch the channel object using the channel ID
    channel = bot.get_channel(channel_id)

    # Create the main embed for rules
    main_embed = discord.Embed(
        title="Server Rules", description="These are the rules of our server:"
    )

    # Add the Client Rules section with emoji
    main_embed.add_field(
        name=":desktop: Client Rules",
        value=(
            "- Use only approved and legal modifications.\n"
            "- Do not exploit or cheat in any form.\n"
            "- Do not use hacked clients or unfair advantages.\n"
            "- Respect the integrity of the game and other players.\n"
            "- Report any bugs or issues to the staff members."
        ),
        inline=False,
    )

    # Add the Chat Rules section with emoji
    main_embed.add_field(
        name=":speech_balloon: Chat Rules",
        value=(
            "- Use appropriate language and avoid offensive or vulgar content.\n"
            "- Be respectful to others and avoid harassment or discrimination.\n"
            "- Do not spam or flood the chat with excessive messages.\n"
            "- Do not advertise or promote other servers or websites.\n"
            "- Respect the topic and purpose of each chat channel."
        ),
        inline=False,
    )

    # Add the General Rules section with emoji
    main_embed.add_field(
        name=":page_facing_up: General Rules",
        value=(
            "- Be respectful to others.\n"
            "- Follow the guidelines and instructions given by staff members.\n"
            "- Do not share personal information or sensitive data.\n"
            "- Respect the privacy and confidentiality of others.\n"
            "- Use appropriate channels for discussions and topics.\n"
            "- Do not create multiple accounts or use alternate accounts without permission.\n"
            "- Report any issues or violations to the staff members.\n"
            "- Use English language in public channels for better communication.\n"
            "- Participate in a constructive and friendly manner.\n"
            "- Observe and follow the server-specific rules and guidelines."
        ),
        inline=False,
    )

    # Add the note at the bottom of the embed
    main_embed.set_footer(
        text="Note: We reserve the right to change these rules at any time without prior notice."
    )

    # Send the main embed in the specified channel
    await channel.send(embed=main_embed)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member == bot.user:
        return

    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author == bot.user:
        for ticket_type, data in ticket_types.items():
            if payload.emoji.name == data["emoji"]:
                guild = bot.get_guild(payload.guild_id)
                ticket_category = discord.utils.get(guild.categories, name="Tickets")

                if not ticket_category:
                    ticket_category = await guild.create_category("Tickets")

                ticket_channel = await ticket_category.create_text_channel(
                    f'{ticket_type.replace(" ", "-").lower()}-ticket-{payload.member.name}'
                )

                await ticket_channel.set_permissions(
                    guild.default_role, read_messages=False
                )
                await ticket_channel.set_permissions(payload.member, read_messages=True)

                embed = discord.Embed(
                    title="Ticket Created",
                    description=f'Hello, {payload.member.mention}! Your {ticket_type.replace("_", " ")} ticket has been created in {ticket_channel.mention}.',
                )
                embed.add_field(name="Issue", value=data["description"])
                embed.set_footer(text="Support will be with you shortly.")

                # Send the additional message in the ticket channel
                additional_message = await ticket_channel.send(data["message"])
                await additional_message.pin()


keep_alive()
bot.run("BOT_CODE")
