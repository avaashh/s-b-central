from db import *
import datetime


async def RecordBirthday(ctx):

    if ctx.channel != "birthdays":
        return

    months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    months_full = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    bMonth, bDate = "", ""

    msg = ctx.content.lower()

    try:
        MSGM = msg.split(" ")
        for m in MSGM:
            if m in months + months_full:
                if m in months:
                    bMonth = months.index(m) + 1
                else:
                    bMonth = months_full.index(m) + 1

                if len(str(bMonth)) == 1:
                    bMonth = f"0{bMonth}"
                else:
                    bMonth = str(bMonth)

        for c in msg:
            if c.isnumeric():
                bDate += c
        if len(bDate) == 1:
            bDate = f"0{bDate}"
        if len(bDate) > 2:
            return

    except:
        pass

    if bMonth != "" and str(bDate) != "":
        BirthDayString = (
            f"Is your (<@{ctx.author.id}>'s) birthday on {bMonth}/{bDate} (mm/dd)?\n\n"
            + "enter '-birthday y' to confirm or ignore this message to not save this information.\n\n\n"
            + "**Beep boop. I am a bot and this action was performed automatically.**"
        )

        DeleteOne("birthdays", {"userID": ctx.author.id})
        InsertOne(
            "birthdays",
            {
                "userID": ctx.author.id,
                "birthday": f"{bMonth}/{bDate}",
                "isVerified": False,
            },
        )

        await ctx.author.send(BirthDayString)


async def BirthdayCommands(ctx):

    if ctx.content.lower() == "-birthday y":
        BDay = FindOne("birthdays", {"userID": ctx.author.id})
        if BDay != None:
            if not BDay["isVerified"]:
                UpdateOne("birthdays", {"userID": ctx.author.id}, {"isVerified": True})

                SavedText = "Saved successfully!\nTo edit this information, type another date in the birthday channel. (Example text: Jan 1)"
                await ctx.author.send(SavedText)

    elif ctx.content.lower() == "-birthday del":
        DeleteOne("birthdays", {"userID": ctx.author.id})

        DeletedText = "Deleted the information. Please provide your correct birthday on the birthday channel. (Example text: Jan 1)"
        await ctx.author.send(DeletedText)

    if ctx.content.lower() == "-birthday when":
        birthdays = FindOne("birthdays", {"userID": ctx.author.id, "isVerified": True})

        if birthdays != None:
            if birthdays["isVerified"]:
                OutputMsg = f"Your birthday is on {birthdays['birthday']}"
                await ctx.channel.send(OutputMsg)
            return

        NoInfo = "I do not have your valid birthday information. Please enter your date of birth (E.g. 'Jan 1') on the birthday channel."
        await ctx.channel.send(NoInfo)

    if ctx.content.lower() == "-birthday set":
        SetText = "Provide your correct birthday on the birthday channel to save it! (Example text: Jan 1)"
        await ctx.channel.send(SetText)


async def checkbirthdays(bot):
    getDate = str(datetime.datetime.now()).split(" ")[0].split("-")
    CheckDate = getDate[1] + "/" + getDate[2]

    TodayBirthdays = FindAll("birthdays", {"birthday": CheckDate, "isVerified": True})
    for TB in TodayBirthdays:
        TextWish = f"🎉 Happy Birthday, <@{TB['userID']}>! 🎉 "
        channel = bot.get_channel(919276382935212043)  # the birthday channel ID
        await channel.send(TextWish)
