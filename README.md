# Workshop-Alerts

```
A Discord Bot that will alert users in a specific channel to specified Steam workshop mods that need to be downloaded and updated,
this will inform them of the Name, URL, When it was updated &amp; Size of the file in GB to download.
```
# Pre-Requisites 
Install the package below:
```console
pip install discord.py steam
```

## Obtain Steam API Key from steam visit URL:

https://steamcommunity.com/dev/apikey 

NOTE: You do not need to use a valid domain name to register the key, you can use domain.com if you wish. 

Copy Key Somewhere safe, perhaps password manager or Keepass DB etc. 


## Create Discord Bot:

https://discord.com/developers/applications

1. Click Create Application and fill out the details and description etc.
2. Go to Bot Sub Menu > General, Create the bot name eg. 'Workshop Alerts' & Click on Reset Token.
3. Copy Token Somewhere safe, perhaps password manager or Keepass DB etc.
4. Navigate to OAuth2 Sub Menu > URL Generator, Select Bot and give your Bot the neccesary permissions.
5. Copy the invite URL and paste it into your browser and invite the bot to your Discord. 
6. If you wish to use the bot in a specific channel you can go to the channel and type #ChannelName (Replace ChannelName with your actual Channel Name) but before the # place a \ and hit enter it will give you a unique ID for your channel to use.


# Simply amend the code as below to use it yourself:


```python
STEAM_API_KEY = 'Add your Steam API Key Here'
BOT_TOKEN = 'Add your Discord Bot Token Here'
CHANNEL_ID = 1234567890 #Replace numbers on the left with your actual Discord ChannelID  
# Examples below but you can add/remove any workshop mods you want to be notified about here..
WORKSHOP_DICT = {
    "TraderPlus":"https://steamcommunity.com/sharedfiles/filedetails/?id=2458896948",
    "DisableCarLock":"https://steamcommunity.com/sharedfiles/filedetails/?id=2458852374"
}
```
## Other things to note
```
a file named mod_updates.json will be created in the same directory you are running the script in,
This is designed to hold mod data for a particular update. 
It's designed to hold the mod info so that if you run the mod locally on your pc it won't keep spamming the same info on the mods, it will hold that info until it changes and update it then.
It would be better suited to run this on a server where it can constantly be running but you can run it locally on your machine if you wish.
```
