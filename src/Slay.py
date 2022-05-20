import db


async def RecordSlay(ctx):
    msg = ctx.content.lower()
    SlayCounter = 0

    for m in range(4, len(msg) + 1):
        if msg[m - 4 : m] == "slay":
            SlayCounter += 1

    if SlayCounter > 0:
        if db.FindOne("Slays", {"UserID": ctx.author.id}):
            db.IncrementOne("Slays", {"UserID": ctx.author.id}, {"SlayCount": 1})
        else:
            db.InsertOne("Slays", {"UserID": ctx.author.id, "SlayCount": SlayCounter})

        await ctx.add_reaction("<:slay:976652250594283620>")


async def SlayLeaderboards(ctx):
    return
