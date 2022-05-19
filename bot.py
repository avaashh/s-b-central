import os, time, datetime
import discord
from discord.ext import tasks, commands

from dotenv import load_dotenv
from db import *

from src.Birthdays import RecordBirthday, BirthdayCommands, checkbirthdays
from src.Wordle import RecordWordle, WordleCommands
from src.Weather import IowaWeather
from src.News import SandBNews


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

    elif "-wordle" in ctx.content.lower():
        await WordleCommands(ctx)

    elif "-weather" in ctx.content.lower():
        await IowaWeather(ctx=ctx)

    else:
        await RecordBirthday(ctx)
        await RecordWordle(ctx)


@tasks.loop(seconds=86400)  # task runs every 86400 seconds, ie everyday
async def DailyRun():
    await checkbirthdays(bot)
    await IowaWeather(bot=bot)


@tasks.loop(seconds=15 * 60)  # 15 minutes
async def NewsFlash():
    await SandBNews(bot=bot)


def RunBot():
    bot.run(os.getenv("TOKEN"))
