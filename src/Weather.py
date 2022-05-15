import requests, discord, os
from dotenv import load_dotenv


load_dotenv()


async def IowaWeather(bot=None, ctx=None):

    if bot == None:
        bot = ctx

    Key = os.getenv("WeatherAPIKey")
    City = "Grinnell"

    URL = f"https://api.weatherapi.com/v1/forecast.json?key={Key}&q={City}&days=1&aqi=yes&alerts=noxs"

    response = requests.get(URL)
    r = response.json()

    if ctx == None:
        channel = bot.get_channel(953207438096625684)  # the weather channel
    else:
        channel = bot.channel

    day = r["forecast"]["forecastday"][0]["day"]

    async with channel.typing():

        current_temperature = r["current"]["temp_f"]
        current_temperature_c = r["current"]["temp_c"]
        current_temperature_f = r["current"]["temp_f"]

        current_pressure = r["current"]["pressure_mb"]
        current_humidity = r["current"]["humidity"]

        weather_description = r["current"]["condition"]["text"]

        embed = discord.Embed(
            title=f"Weather in {City}, Iowa",
            # color="ee3124",
        )
        embed.add_field(
            name=f"Daily Forecast: {r['forecast']['forecastday'][0]['date']}",
            value=f"**{day['condition']['text']}**",
            inline=False,
        )
        embed.add_field(
            name="Current Temperature",
            value=f"**{current_temperature_f}°F ({current_temperature_c}°C) **",
            inline=False,
        )
        embed.add_field(
            name="Humidity(%)", value=f"**{current_humidity}%**", inline=False
        )
        embed.add_field(
            name="Max Temperature",
            value=f"**{day['maxtemp_f']}°F ({day['maxtemp_c']}°C) **",
            inline=True,
        )
        embed.add_field(
            name="Min Temperature",
            value=f"**{day['mintemp_f']}°F ({day['mintemp_c']}°C) **",
            inline=True,
        )
        embed.add_field(
            name="Daily Chance of Rain (%)",
            value=f"**{day['daily_chance_of_rain']*100}% **",
            inline=True,
        )
        embed.add_field(
            name="Daily Chance of Snow (%)",
            value=f"**{day['daily_chance_of_snow'] * 100}% **",
            inline=True,
        )

        embed.set_thumbnail(url=f"https:{day['condition']['icon']}")

        if ctx == None:
            embed.set_footer(text=f"Is the forecast right? How is the weather today?")
        else:
            embed.set_footer(text=f"Requested by {bot.author.name}")
            await channel.send(embed=embed)
            return

    message = await channel.send(embed=embed)
    await message.add_reaction("☀️")
    await message.add_reaction("❄️")
    await message.add_reaction("🌧️")
    await message.add_reaction("☁️")
    await message.add_reaction("⚡")
