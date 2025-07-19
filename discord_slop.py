import asyncio

import discord
from discord.ext import commands
import _KUNCI
from gcp_slop import start_vm, stop_vm, restart_vm, get_vm_ip, get_vm_status

intents = discord.Intents.default()
intents.message_content = True

prefixlol = "reihansyahfitra-"
bot = commands.Bot(command_prefix=prefixlol, intents=intents)


@bot.after_invoke
async def update_status(ctx):
    status = get_vm_status()
    if status == "RUNNING":
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="V Rising"))
    else:
        await bot.change_presence(status=discord.Status.dnd, activity=None)


@bot.command(name='ip')
async def ip_command(ctx):
    """Ngirim informasi IP, otomatis mupus sanggeus 30 detik"""
    await ctx.reply(f"{get_vm_ip()}:9876", delete_after=30)


@bot.command(name='status')
async def status_command(ctx):
    """Nembongkeun kaayaan server"""
    await ctx.reply(get_vm_status(), mention_author=False)


@bot.command(name='start')
async def start_command(ctx):
    """Ngahurungkeun server"""
    await ctx.reply(start_vm(), mention_author=False)


@bot.command(name='stop')
async def stop_command(ctx):
    """Mareuman server"""
    await ctx.send(f"<@{ctx.author.id}> : {stop_vm()}")


@bot.command(name='restart')
async def restart_command(ctx):
    """Ngahurungkeun deui server"""
    await ctx.send(f"<@{ctx.author.id}> : {restart_vm()}")


@bot.command(name='tolong')
async def help_command(ctx):
    """Nembongkeun paréntah nu aya"""
    embed = discord.Embed(
        title="tolong",
        description="commands:",
        color=discord.Color.blue()
    )

    for command in bot.commands:
        if command.name != 'help':
            embed.add_field(
                name=f"{prefixlol}{command.name}",
                value=command.help or "-",
                inline=False
            )

    embed.set_footer(text="🤙 slooooooop")
    await ctx.reply(embed=embed, mention_author=False)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await help_command(ctx)
        return
    raise error


def run():
    bot.run(_KUNCI.BOT_TOKEN)
