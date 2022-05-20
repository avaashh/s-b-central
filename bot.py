import os, time, datetime
import discord
from discord.ext import tasks, commands

from dotenv import load_dotenv
from db import *

from src.Birthdays import RecordBirthday, BirthdayCommands, checkbirthdays
from src.Weather import IowaWeather
from src.News import SandBNews
from src.Slay import RecordSlay, SlayLeaderboards


load_dotenv()
features = FindOne("grinnell-bot", {})

bot = commands.Bot(command_prefix="-")


@bot.event
async def on_ready():
    print(f"Logged in successfully // {bot.user} // {time.time()} ")

    DailyRun.start()
    NewsFlash.start()


@bot.event
async def on_message(ctx):

    if ctx.author == bot.user:
        return

    if "-birthday" in ctx.content.lower():
        await BirthdayCommands(ctx)

    elif "-weather" in ctx.content.lower():
        await IowaWeather(ctx, userRequest=True)

    elif "-slay" in ctx.content.lower():
        await SlayLeaderboards(ctx)
    else:
        await RecordSlay(ctx)
        await RecordBirthday(ctx)


@tasks.loop(seconds=86400)  # task runs every 86400 seconds, ie everyday
async def DailyRun():
    # await checkbirthdays(bot)
    # await IowaWeather(bot)
    pass


@tasks.loop(seconds=15 * 60)  # 15 minutes
async def NewsFlash():
    await SandBNews(bot=bot)


def RunBot():
    bot.run(os.getenv("TOKEN"))
