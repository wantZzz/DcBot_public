import discord
from discord.ext import commands
import os, json

import time_myself
from cog import Cog_Extension

import firebase_admin
from firebase_admin import credentials, initialize_app, storage

with open('author_datafile/state.json',encoding="utf-8") as f:
  #file_json = f.read()
  state = json.load(f)

def load_state():
  global state
  with open('author_datafile/state.json',encoding="utf-8") as f:
    #file_json = f.read()
    state = json.load(f)

class control(Cog_Extension):

  record = True
  noise = True
  administrator = {521312587825020928,659769555115311104}
  Maintainer = {521312587825020928}
  Maintain = False
  findEvent = True
  voice = True
  state_file = 'author_datafile/state.json'

  @commands.command()
  async def onrecord(self, ctx):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['record'] = True
        f.write(json.dumps(state))
      control.record = True
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def stoprecord(self, ctx):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['record'] = False
        f.write(json.dumps(state))
      control.record = False
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")
  
  @commands.command()
  async def onmaintain(self, ctx):
    load_state()
    if ctx.author.id in state['Maintainer']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['Maintain'] = True
        f.write(json.dumps(state))
      control.Maintain = True
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def stopmaintain(self, ctx):
    load_state()
    if ctx.author.id in state['Maintainer']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['Maintain'] = False
        f.write(json.dumps(state))
      control.Maintain = False
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")
    
  @commands.command()
  async def onnoise(self, ctx):
    load_state()
    with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['noise'] = True
        f.write(json.dumps(state))
    control.noise = True
    await ctx.message.add_reaction("🆗")

  @commands.command()
  async def stopnoise(self, ctx):
    load_state()
    with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['noise'] = False
        f.write(json.dumps(state))
    control.noise = False
    await ctx.message.add_reaction("🆗")
  
  @commands.command()
  async def on_findEvent(self, ctx):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['findEvent'] = True
        f.write(json.dumps(state))
      control.findEvent = True
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def stop_findEvent(self, ctx):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['findEvent'] = False
        f.write(json.dumps(state))
      control.findEvent = False
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")
      
  @commands.command()
  async def onvoice(self, ctx):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['voice'] = True
        f.write(json.dumps(state))
      control.voice = True
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def stopvoice(self, ctx):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['voice'] = False
        f.write(json.dumps(state))
      control.voice = False
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def listen_all(self, ctx):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['listen_all'] = not state['listen_all']
        f.write(json.dumps(state))
      await ctx.message.add_reaction("🆗")
      
      if state['listen_all']:
        await ctx.message.add_reaction("🟢")
      else:
        await ctx.message.add_reaction("🔴")
        
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def voice_mode(self, ctx, mode_code):
    load_state()
    mode_code_list = ['only','all']
    if ctx.author.id in state['administrator'] and mode_code in mode_code_list:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['voice_mode'] = mode_code
        f.write(json.dumps(state))
        
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def listen_only(self, ctx):
    load_state()
    try:
      if id[2:-1] in state['only_voice']:
        with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
          state['only_voice'].remove(ctx.author.id)
          f.write(json.dumps(state))
        await ctx.message.add_reaction("🔇")
  
      else:
        with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
          state['only_voice'].append(ctx.author.id)
          f.write(json.dumps(state))
        await ctx.message.add_reaction("🔊")
          
      await ctx.message.add_reaction("🆗")
    except:
      await ctx.message.add_reaction("🆖")

  """@commands.command()
  async def delete_event_mode(self, ctx, mode_code):
    load_state()
    mode_code_list = ['all','nopicture']
    if ctx.author.id in state['administrator'] and mode_code in mode_code_list:
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        state['delete_event_mode'] = mode_code
        f.write(json.dumps(state))
        
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")"""

  @commands.command()
  async def change_voicenick(self, ctx, user_id, change_nick):
    load_state()
    if ctx.author.id in state['administrator']:
      with open('author_datafile/data.json', 'r',encoding="utf-8") as f:
        data = json.load(f)
        
      with open('author_datafile/data.json', 'w',encoding="utf-8") as f:
        data[user_id] = change_nick
        f.write(json.dumps(data))

      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def read_statefile(self, ctx):
    load_state()
    if ctx.author.id in state['Maintainer']:
      await ctx.send(file=discord.File('author_datafile/state.json'))
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def overwrite_statefile(self, ctx):
    load_state()
    if ctx.author.id in state['Maintainer']:
      try:
        file = await ctx.message.attachments[0].read()
      except:
        await ctx.message.add_reaction("🆖")
        return
        
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        f.write(file.decode("utf-8"))

      await ctx.send(file=discord.File('author_datafile/state.json'))
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def overwrite_weirdfile(self, ctx):
    load_state()
    if ctx.author.id in state['Maintainer']:
      try:
        file = await ctx.message.attachments[0].read()
      except:
        await ctx.message.add_reaction("🆖")
        return
        
      with open(f"author_datafile/weird_quest.json",'w',encoding="utf-8") as f:
        f.write(file.decode("utf-8"))

      await ctx.send(file=discord.File('author_datafile/weird_quest.json'))
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")
  
  @commands.command()
  async def refresh_authorfiles(self, ctx):
    load_state()
    if ctx.author.id in state['Maintainer']:
      print('downloading author file......')
        
      try:
        try:
          bucket = storage.bucket()
        except:
          cred = credentials.Certificate(r"author_datafile/credentials.json")
          initialize_app(cred, {'storageBucket': 'tako-deletebase.appspot.com'})
          bucket = storage.bucket()

        for filelist in os.listdir("./author_datafile"):
          destination_file_name = f"author_datafile/{filelist}"
          blob = bucket.blob(destination_file_name)
          blob.download_to_filename(destination_file_name)
        
        print('done!')
        await ctx.message.add_reaction("🆗")
        
      except Exception as e:
        await ctx.reply(f'error detail: {e}')
        print(e)
        await ctx.message.add_reaction("🆖")
    else:
      await ctx.message.add_reaction("🆖")
      
  @commands.command()
  async def upload_authorfiles(self, ctx):
    load_state()
    if ctx.author.id in state['Maintainer']:
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
           
        await ctx.reply(f"資料庫更新成功! 開始上傳時間: {updata_time}, 上傳完成時間:{time_myself.time_str_hour_to_second_add_colon()}")
          
      except Exception as e:
        await ctx.reply(f"資料庫更新失敗! {e}")
    else:
      await ctx.message.add_reaction("🆖")
      
  
  
  @commands.command()
  async def ask_where(self, ctx):
    await ctx.reply(ctx.channel)
    print(ctx.channel)

async def setup(bot):
  await bot.add_cog(control(bot))