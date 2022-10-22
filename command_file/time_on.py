import discord
import sys
import os
import json
from discord.ext import commands
from cog import Cog_Extension

import firebase_admin
from firebase_admin import credentials, initialize_app, storage

import asyncio
import random
import requests

import time_myself

sys.path.append(os.pardir)
from command_file.control import control

#from aioconsole import ainput


class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

class time_on(Cog_Extension):
  now_day = time_myself.time_str_year_to_day()
  log_name = "Console_Log/" + str(now_day) + ".txt"
  sleep_time= random.randint(0,20)

  def __init__(self,*arge,**kwargs):
    super().__init__(*arge,**kwargs)

    async def time_delete_counter():

      await self.bot.wait_until_ready()
    
      login_time = time_myself.time_pane()
      #login_time = ((login_time // 100) + ((58 + (login_time % 100)) // 60) - 1)*100 + ((58 + (login_time % 100)) % 60)#for +8 GMT
      
      self.channel = self.bot.get_channel(873837336851533854)
      Maint = self.bot.get_user(521312587825020928)
      
      await Maint.send(f"next backup time: {login_time}")
        
      while not self.bot.is_closed():
        
        now = time_myself.time_pane()
        if now == 0000:
          """keys = db_re.keys()
          
          for i in keys:
            del db_re[i]
            await asyncio.sleep(0.2)
          for filelist in os.listdir("./msg_delete_file"):
            os.remove(f'./msg_delete_file/{filelist}')
            await asyncio.sleep(0.2)
              
          print(bcolors.OK + "00:00 釋放暫存完成" + bcolors.RESET)
          await Maint.send("00:00 釋放暫存完成")"""
          await Maint.send("00:00 輕量化平台log紀錄")
          await Maint.send(file=discord.File(time_on.log_name))

          new_day = time_myself.time_str_year_to_day()
          time_on.log_name = "Console_Log/" + str(new_day) + ".txt"

          with open(control.state_file,encoding="utf-8") as f:
            state = json.load(f)

          with open('author_datafile/weird_quest.json',encoding="utf-8") as f:
            weird_quest = json.load(f)
          
          with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
            state['weird_quest'] = list(map(int, weird_quest.keys()))
            state['only_voice'] = [521312587825020928]
            f.write(json.dumps(state))
          await asyncio.sleep(60)
        
          """try:
            #with open('credentials.json', 'w',encoding="utf-8") as f:
              #f.write(os.environ["credentials"])
           
            #cred = credentials.Certificate(r"credentials.json")
            #initialize_app(cred, {'storageBucket': 'tako-deletebase.appspot.com'})
            bucket = storage.bucket()
            for filelist in os.listdir("./author_datafile"):
              destination_file_name = f"author_datafile/{filelist}"
              blob = bucket.blob(destination_file_name)
              blob.upload_from_filename(destination_file_name)
           
            await Maint.send("資料庫更新成功!")
          
          except Exception as e:
            await Maint.send(f"資料庫更新失敗! {e}")
            pass"""
        
        if now == login_time:
          try:
            updata_time = time_myself.time_str_hour_to_second_add_colon()
 
            try:
              bucket = storage.bucket()
            except:
              cred = credentials.Certificate(r"author_datafile/credentials.json")
              initialize_app(cred, {'storageBucket': 'tako-deletebase.appspot.com'})
              bucket = storage.bucket()

            for filelist in os.listdir("./author_datafile"):
              destination_file_name = f"author_datafile/{filelist}"
              blob = bucket.blob(destination_file_name)
              blob.upload_from_filename(destination_file_name)
           
            await Maint.send(f"資料庫更新成功! 開始上傳時間: {updata_time}, 上傳完成時間:{time_myself.time_str_hour_to_second_add_colon()}")
          
          except Exception as e:
            await Maint.send(f"資料庫更新失敗! {e}")
            pass
          
          await asyncio.sleep(60)

        elif (now == 2300+time_on.sleep_time):
          with open(control.state_file,encoding="utf-8") as f:
            state = json.load(f)
          if state['noise']:
            await self.channel.send("大家晚安晚安www")
          await asyncio.sleep(60)
        elif (now == 720+time_on.sleep_time):
          with open(control.state_file,encoding="utf-8") as f:
            state = json.load(f)
          if state['noise']:
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