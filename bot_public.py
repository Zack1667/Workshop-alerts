import discord
from discord.ext import commands
import requests
import asyncio
import datetime
import json

intents = discord.Intents.default()
intents.typing = False  # Disable typing event to reduce bot permissions
intents.presences = False  # Disable presence event to reduce bot permissions

# Key's tokens and Other Variables below: 

STEAM_API_KEY = 'YOURSTEAMAPIKEY'
BOT_TOKEN = 'YOURDISCORDBOTTOKEN'
CHANNEL_ID = 1234567890 # YOUR DISCORD CHANNEL ID HERE  

WORKSHOP_DICT = {
    "TraderPlus":"https://steamcommunity.com/sharedfiles/filedetails/?id=2458896948",
    "DisableCarLock":"https://steamcommunity.com/sharedfiles/filedetails/?id=2458852374",
    "BaseBuildingPlus":"https://steamcommunity.com/sharedfiles/filedetails/?id=1710977250"
}


bot = commands.Bot(command_prefix='!', intents=intents)

# Storing Mod Updates in a Dict so if the bot goes offline it will retain the info here 
mod_updates = {}


@bot.event
async def on_ready():
    # This function is called when the bot is ready and logged in.
    print(f'Bot logged in as {bot.user.name}')
    await load_mod_updates()
    await check_workshop_updates()

async def load_mod_updates():
    # This function loads the existing mod updates from the mod_updates.json file.
    # If the file doesn't exist, it initializes an empty mod_updates dictionary.
    global mod_updates
    try:
        with open('mod_updates.json', 'r') as file:
            mod_updates = json.load(file)
    except FileNotFoundError:
        mod_updates = {}

async def save_mod_updates():
    # This function saves the mod_updates dictionary to the mod_updates.json file.
    with open('mod_updates.json', 'w') as file:
        json.dump(mod_updates, file)

async def check_workshop_updates():
    # This function checks for updates in the Steam Workshop for each mod in WORKSHOP_DICT.
    # It runs in a loop until the bot is closed.
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)

    while not bot.is_closed():
        for mod_name, mod_url in WORKSHOP_DICT.items():
            try:
                # Extract the item ID from the mod_url
                item_id = mod_url.split('=')[-1]
                url = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
                params = {
                    'key': STEAM_API_KEY,
                    'itemcount': 1,
                    'publishedfileids[0]': item_id,
                }
                # Send a POST request to the Steam API to get the mod details
                response = requests.post(url, data=params)
                data = response.json()

                # Extract relevant details from the API response
                item_details = data['response']['publishedfiledetails'][0]
                item_title = item_details['title']
                item_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_details['publishedfileid']}"
                item_updated = int(item_details['time_updated'])
                item_size = int(item_details['file_size'])
                thumbnail_url = item_details['preview_url']

                # Skip this mod if the update is not newer than the last recorded update
                if mod_name in mod_updates and mod_updates[mod_name] >= item_updated:
                    continue

                # Update the mod_updates dictionary with the new update timestamp
                mod_updates[mod_name] = item_updated

                # Create an embed with mod update information
                embed = discord.Embed(
                    title=item_title,
                    url=item_url,
                    description=f'New update for {mod_name}!',
                    color=discord.Color.blue()
                )

                embed.add_field(name='Updated', value=f'{calculate_time_since_update(item_updated)} ago', inline=True)
                embed.add_field(name='Size', value=f'{format_size(item_size)}', inline=True)

                embed.set_thumbnail(url=thumbnail_url)

                # Send the embed message to the specified channel
                await channel.send(embed=embed)
            except Exception as e:
                # If an error occurs during the update check, print the error message
                print(f'Error checking Steam Workshop for {mod_name}:', e)

        # Save the updated mod_updates dictionary to the mod_updates.json file
        await save_mod_updates()
        await asyncio.sleep(3600)  # Check for updates every hour

# Calculate time difference since update
def calculate_time_since_update(updated_time):
    current_time = datetime.datetime.now()
    time_since_update = current_time - datetime.datetime.fromtimestamp(updated_time)
    minutes_since_update = int(time_since_update.total_seconds() / 60)
    return f'{minutes_since_update} minutes'

# Format size in human-readable format
def format_size(size):
    size_gb = size / 1024 / 1024 / 1024
    formatted_size = f'{size_gb:.2f}GB'
    return formatted_size

bot.run(BOT_TOKEN)
