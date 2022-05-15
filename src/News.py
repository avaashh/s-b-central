import db, requests, re, time, discord
from bs4 import BeautifulSoup


async def FetchNews():
    url = "http://www.thesandb.com/wp-json/wp/v2/posts?per_page=50"
    response = requests.get(url, headers={"User-Agent": ""}).json()

    # APN - Already Posted News
    APN = [x["PostID"] for x in db.FindAll("SandBNews", {})]
    NewsToPost = []

    for News in response:
        if News["id"] not in APN:
            NewsToPost.append(News)

    NTPost = [{"PostID": x["id"], "PostTime": time.time()} for x in NewsToPost]
    if len(NTPost) > 0:
        db.InsertMany("SandBNews", NTPost)

    SandBNews = []

    for NTP in NewsToPost:
        Title = NTP["title"]["rendered"]
        TimePosted = NTP["date"].replace("T", " ")
        Link = NTP["link"]
        Excerpt = NTP["content"]["rendered"]

        try:
            Image = NTP["jetpack_featured_media_url"]
        except:
            Image = None

        Title = re.sub("<[^>]+>", "", BeautifulSoup(Title, "html.parser").text)
        Excerpt = re.sub("<[^>]+>", "", BeautifulSoup(Excerpt, "html.parser").text)
        Excerpt = (Excerpt[:250] + "...").replace("\n", "\n\n")

        Author = requests.get(
            f"http://www.thesandb.com/wp-json/wp/v2/users/{NTP['author']}",
            headers={"User-Agent": ""},
        ).json()
        AuthorName = Author["name"]
        AuthorDes = re.sub(
            "<[^>]+>", "", BeautifulSoup(Author["description"], "html.parser").text
        )

        SandBNews.append(
            {
                "title": Title,
                "time": TimePosted,
                "link": Link,
                "excerpt": Excerpt,
                "image": Image,
                "author": AuthorName,
                "aboutAuthor": AuthorDes,
            }
        )

    return SandBNews


async def SandBNews(bot):
    SandBNews = await FetchNews()
    channel = bot.get_channel(918634538979192864)  # announcements channel

    if len(SandBNews) == 0:
        return

    for SBN in SandBNews:
        embed = discord.Embed(
            title=SBN["title"],
            url=SBN["link"],
            description=SBN["excerpt"],
            color=0xFF0000,
        )
        embed.set_author(name=SBN["author"])
        embed.set_image(url=SBN["image"])
        embed.add_field(name="Updated:", value=SBN["time"], inline=True)
        embed.set_footer(text=SBN["aboutAuthor"])

        message = await channel.send(embed=embed)
