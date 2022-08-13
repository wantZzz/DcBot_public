import discord
import sys
import asyncio
import os

from discord.ext import commands
from discord.ui import Button,View
import requests

from replit import db
db_re = db

from cog import Cog_Extension

sys.path.append(os.pardir)
from command_file.control import control

class template(Cog_Extension):
  pass
  
async def setup(bot):
  await bot.add_cog(template(bot))