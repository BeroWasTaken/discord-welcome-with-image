token = "your-token-here" # <- Your Bot Token found on Discord's Application Website (https://discord.com/developers/applications)
prefix = "&" # <- Bot Prefix. Doesn't matter because we don't use any Commands here


# All these Packages have to be installed on your Pc for the Bot to work. (Usually: 'pip install ...' in your CMD when using Windows 10. If not, look it up)

import discord
from discord.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
import asyncio
import os
import numpy as np

intents = discord.Intents.default() # <- Discord Intents have to be enabled on Discord's Application Website for the Bot to work.
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command("help") # Removes the default 'help' Command from Discord

print("Loading..")

@bot.event
async def on_ready():
    print("Bot Ready!")

    
# Code to round the Image (Profilepicture)

def circle(pfp,size = (215,215)): 
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


@bot.event
async def on_member_join(member):
    
    guild = bot.get_guild(999999999999999) # <- Your Server (Guild) ID (Right-Click on Server Icon -> Copy ID)
    text = guild.get_channel(999999999999999) # <- Your Welcome-Channel ID (Right-Click on Text-Channel -> Copy ID)
    filename = "your-file.png" # <- The name of the file that will be saved and deleted after (Should be PNG)

    background = Image.open("welcome.png") # <- Background Image (Should be PNG)

    asset = member.avatar_url_as(size=1024) # This loads the Member Avatar
    data = BytesIO(await asset.read())

    pfp = Image.open(data).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((265,265)) # Resizes the Profilepicture so it fits perfectly in the circle

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("LemonMilkMedium-mLZYV.otf",42) # <- Text Font of the Member Count. Change the text size for your preference
    member_text = ("#" + str(guild.member_count) + "  USER") # <- Text under the Profilepicture with the Membercount
    draw.text((383,410),member_text,font=font)

    background.paste(pfp, (379,123), pfp) # Pastes the Profilepicture on the Background Image
    background.save(filename) # Saves the finished Image in the folder with the filename

    msg = await text.send(file = discord.File(filename),content ="WELCOME " + member.mention + "! Please read the rules! :heart:") # <- The welcome Message Content put above the Image. "member.mention" @mentions the user
    await asyncio.sleep(5) # 5 Seconds of waiting time
    try: 
        os.remove('C:/path/' + filename) # <- Change your path to where the Bot is located. Tries to delete the file again so your folder won't be full of Images. If it's already deleted nothing will happen
    except:
        pass
    

# ====================================================

bot.run(token)
