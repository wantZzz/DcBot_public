import discord
import os, sys
import json
from discord.ext import commands
from cog import Cog_Extension

import asyncio
import random
import requests

import time_myself

sys.path.append(os.pardir)

class time_on(Cog_Extension):
  now_day = time_myself.time_str_year_to_day()
  log_name = "Console_Log/" + str(now_day) + ".txt"
  sleep_time= random.randint(0,20)

  def __init__(self,*arge,**kwargs):
    super().__init__(*arge,**kwargs)

    async def time_delete_counter():

      await self.bot.wait_until_ready()
      
      with open("users_file/state.json", "r") as f:
        state = json.load(f)
      
      self.channel = self.bot.get_channel(state['main_channel'])
      Maintainer = self.bot.get_user(state['Maintainer'])
      
      
      while not self.bot.is_closed():
        
        now = time_myself.time_pane()
        if now == 0000:
          await Maintainer.send("00:00 log紀錄")#log file
          await Maintainer.send(file=discord.File(time_on.log_name))

          new_day = time_myself.time_str_year_to_day()
          time_on.log_name = "Console_Log/" + str(new_day) + ".txt"

          with open('users_datafile/state.json') as f:
            state = json.load(f)
          
          with open('users_datafile/state.json', 'w') as f:
            state['only_voice'] = [state['Maintainer']]
            f.write(json.dumps(state))
          await asyncio.sleep(60)

        elif (now == 2300+time_on.sleep_time):#say goodnight
          with open('users_datafile/state.json') as f:
            state = json.load(f)
          if state['noise']:
            await self.channel.send("大家晚安晚安www")
          await asyncio.sleep(60)
        elif (now == 720+time_on.sleep_time):#say goodmorning
          await self.channel.send("早安安!Wah!")
          await asyncio.sleep(60)

        else:
          await asyncio.sleep(30)
          with open("Console_Log/time_stamp.txt", 'w') as f:
            f.write(time_myself.time_str_year_to_day_add_slash()+ " " +time_myself.time_str_hour_to_second_add_colon())
          pass

       
      
  
    self.bot.loop.create_task(time_delete_counter())
        

async def setup(bot):
  await bot.add_cog(time_on(bot))
