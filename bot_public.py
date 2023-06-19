import discord
from discord.ext import commands
import requests
import asyncio
import datetime
import json

intents = discord.Intents.default()
intents.typing = False  # Disable typing event to reduce bot permissions
intents.presences = False  # Disable presence event to reduce bot permissions

STEAM_API_KEY = 'STEAMKEY'
BOT_TOKEN = 'BOTTOKEN'
CHANNEL_ID = 1234567890

WORKSHOP_DICT = {
    "TraderPlus":"https://steamcommunity.com/sharedfiles/filedetails/?id=2458896948",
    "DisableCarLock":"https://steamcommunity.com/sharedfiles/filedetails/?id=2458852374",
    "BaseBuildingPlus":"https://steamcommunity.com/sharedfiles/filedetails/?id=1710977250",
    "ZookTest":"https://steamcommunity.com/sharedfiles/filedetails/?id=2991695632"
}

bot = commands.Bot(command_prefix='!', intents=intents)

mod_updates = {}

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user.name}')
    await load_mod_updates()
    await check_workshop_updates()

async def load_mod_updates():
    global mod_updates
    try:
        with open('mod_updates.json', 'r') as file:
            mod_updates = json.load(file)
    except FileNotFoundError:
        mod_updates = {}

async def save_mod_updates():
    with open('mod_updates.json', 'w') as file:
        json.dump(mod_updates, file)

async def check_workshop_updates():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)

    while not bot.is_closed():
        for mod_name, mod_url in WORKSHOP_DICT.items():
            try:
                item_id = mod_url.split('=')[-1]
                url = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
                params = {
                    'key': STEAM_API_KEY,
                    'itemcount': 1,
                    'publishedfileids[0]': item_id,
                }
                response = requests.post(url, data=params)
                data = response.json()

                item_details = data['response']['publishedfiledetails'][0]
                item_title = item_details['title']
                item_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_details['publishedfileid']}"
                item_updated = int(item_details['time_updated'])
                item_size = int(item_details['file_size'])
                thumbnail_url = item_details['preview_url']

                if mod_name in mod_updates and mod_updates[mod_name] >= item_updated:
                    continue  # Skip this mod if the update is not newer

                mod_updates[mod_name] = item_updated

                embed = discord.Embed(
                    title=item_title,
                    url=item_url,
                    description=f'New update for {mod_name}!',
                    color=discord.Color.blue()
                )

                embed.add_field(name='Updated', value=f'{calculate_time_since_update(item_updated)} ago', inline=True)
                #print("Item Size:", item_size) # for troubleshooting size not displaying correctly. 
                embed.add_field(name='Size', value=f'{format_size(item_size)}', inline=True)

                embed.set_thumbnail(url=thumbnail_url)

                await channel.send(embed=embed)
            except Exception as e:
                print(f'Error checking Steam Workshop for {mod_name}:', e)

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
    size_gb = size / (1024 * 1024 * 1024)  # Convert bytes to gigabytes
    formatted_size = f'{size_gb:.2f}GB'
    return formatted_size

bot.run(BOT_TOKEN)
