import db, time, pandas
import discord


async def RecordSlay(ctx):
    msg = ctx.content.lower()
    SlayCounter = 0

    for m in range(4, len(msg) + 1):
        if msg[m - 4 : m] == "slay":
            SlayCounter += 1

    Current = db.FindOne("Slays", {"UserID": ctx.author.id})
    if SlayCounter > 0:
        if Current:
            if Current["Last"] + 60 < time.time():
                db.UpdateOne(
                    "Slays",
                    {"UserID": ctx.author.id},
                    {"SlayCount": Current["SlayCount"] + 1, "Last": time.time()},
                )
        else:
            db.InsertOne(
                "Slays",
                {
                    "UserID": ctx.author.id,
                    "SlayCount": SlayCounter,
                    "Last": time.time(),
                },
            )

        await ctx.add_reaction("<:slay:976652250594283620>")


async def SlayLeaderboards(ctx):
    Scores = db.FindAll("Slays", {}).sort("SlayCount", -1)
    SF = pandas.DataFrame([x for x in Scores])

    if ctx.content.lower() == "-slayest":
        Message = f"🥇 <@{SF['UserID'][0]}> is the slayest Gwinnellian with {SF['SlayCount'][0]} slayy xp 🥵.\n"
        Message += f"🥈 <@{SF['UserID'][1]}> ({SF['SlayCount'][1]} slay xp)\n"
        Message += f"🥉 <@{SF['UserID'][2]}> ({SF['SlayCount'][2]} slay xp)"

        await ctx.reply(Message)
    elif "-slay <@" in ctx.content.lower():
        UID = ctx.content.lower().split("<@")[1].replace(">", "")
        SS = SF[SF["UserID"] == int(UID)]

        try:
            Rank = SS.index[0] + 1
            Message = f"<@{UID}> is slaying at rank {Rank} with {SF['SlayCount'][Rank-1]} slayy xp 🥵\n"
            await ctx.reply(Message)
        except:
            await ctx.reply(f"<@{UID}> has 0 slay xp.")

    elif ctx.content.lower() == "-slay rank all":

        SF["UID"] = "<@" + SF["UserID"].astype(str) + ">"
        UID = SF["UID"].tolist()
        Ranks = "\n".join(["🥇", "🥈", "🥉"] + [str(x) for x in range(4, len(SF) + 1)])
        UN = "\n".join(UID)
        Sc = "\n".join(SF["SlayCount"].astype(str).tolist())

        embed = discord.Embed(title="Slay Count Leaberboard", color=0xEE905D)
        embed.add_field(name="Rank", value=Ranks, inline=True)
        embed.add_field(name="Username", value=UN, inline=True)
        embed.add_field(name="Score", value=Sc, inline=True)
        await ctx.reply(embed=embed)
