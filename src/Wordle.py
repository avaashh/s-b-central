from db import *
from random import choice


async def RecordWordle(ctx):

    if str(ctx.channel) not in ["wordle", "bot-check"]:
        return

    WordsHere = ctx.content.split(" ")
    if WordsHere[0] == "Wordle":
        WordleID, Score = (
            WordsHere[1],
            (WordsHere[2].split("\n")[0].replace("/6", "")).strip(),
        )

        if Score == "X":
            Score = 0

        WordleID, Score = int(WordleID), int(Score)

        Tier1 = [
            "That score is kinda sus.\n⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n⬛⬛🟩🟩🟩🟩🟩🟩⬛⬛\n⬛⬛🟩🟩🟩🟩🟩🟩⬛⬛\n⬛⬛🟩🟨🟨🟨🟨🟨🟨⬛\n⬛⬛🟩🟨🟨🟨🟨🟨🟨⬛\n⬛⬛🟩🟨🟨🟨🟨🟨🟨⬛\n⬛⬛🟩🟩🟩🟩🟩🟩⬛⬛\n⬛⬛🟩🟩🟩🟩🟩🟩⬛⬛\n⬛⬛🟩🟩🟩🟩🟩🟩⬛⬛\n⬛⬛🟩🟩⬛⬛🟩🟩⬛⬛\n⬛⬛🟩🟩⬛⬛🟩🟩⬛⬛",
            "College degree? Please. This is the kind of thing to put on a resume.",
            "https://www.meme-arsenal.com/memes/40a55446d127fa4774f78769566ebbd7.jpg",
            "https://starecat.com/content/wp-content/uploads/what-if-we-used-100-percent-of-the-brain-meme-original.jpg",
        ]
        Tier2 = [
            "https://pbs.twimg.com/media/FKBFX0RXMAMvaWN?format=jpg&name=900x900",
            "im really 🟩🟩🟩🟩🟩 for u",
            "http://www.quickmeme.com/img/89/896af38f50bb853cd4faa9bd05a7865899c891915061a4e316a936c9eef5b466.jpg",
            "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5b52c318-b9ee-40d7-b65e-bb8813c086dc/d47iu97-be50a3d0-1133-4764-b677-87faf8206c27.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzViNTJjMzE4LWI5ZWUtNDBkNy1iNjVlLWJiODgxM2MwODZkY1wvZDQ3aXU5Ny1iZTUwYTNkMC0xMTMzLTQ3NjQtYjY3Ny04N2ZhZjgyMDZjMjcuanBnIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.LgImdR2bv1KNsTfhlBlOu04Ym_C95KbLVfMKbo-Z7LI",
        ]
        Tier3 = [
            "sorry that 🟨⬛⬛🟨🟨",
            "https://www.google.com/search?q=how+to+play+wordle",
        ]
        Tier4 = [
            "https://pbs.twimg.com/media/FJ3f3X8akAIO0M6?format=jpg&name=medium",
            "https://pbs.twimg.com/media/FKCY98hXMAcgRq5?format=jpg&name=small",
            "https://i.ytimg.com/vi/oiHXNCT3kaQ/maxresdefault.jpg",
        ]

        if isinstance(WordleID, int) and isinstance(Score, int):

            ThisScore = {"UserID": ctx.author.id, "WordleDate": WordleID}
            ValidGame = FindOne("wordle-scores", ThisScore)

            if ValidGame != None:
                await ctx.channel.send("You have already submitted that game.")
                return

            ThisScore["Score"] = Score
            # InsertOne("wordle-scores", ThisScore)

            if Score in [1, 2]:
                await ctx.channel.send(random.choice(Tier1))
            elif Score in [3, 4]:
                await ctx.channel.send(random.choice(Tier2))
            elif Score in [5, 6]:
                await ctx.channel.send(random.choice(Tier3))
            elif Score in [0]:
                await ctx.channel.send(random.choice(Tier4))


async def WordleCommands(ctx):
    print(ctx.content)
