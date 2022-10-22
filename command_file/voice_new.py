import discord
from discord.ext import commands
import nacl
import asyncio
import re
import os
import json
from gtts import gTTS 
from eyed3 import load
from discord.ui import Button,View

import requests

import time_myself
import random

from command_file.control import control
from cog import Cog_Extension

#https://yout.com/ 時間軸剪輯

class view_bar(View):
  @discord.ui.button(label="關閉報時", style=discord.ButtonStyle.gray, emoji='❌')
  async def timevoice_callback(self,ctx,button):
    await ctx.message.delete()

  @discord.ui.button(label="關閉進出頻道通知", style=discord.ButtonStyle.gray, emoji='❌')
  async def intochannelvoice_callback(self,ctx,button):
    await ctx.message.delete()

  @discord.ui.button(label="更換文字頻道範圍", style=discord.ButtonStyle.gray, emoji='❌')
  async def translatemodevoice_callback(self,ctx,button):
    await ctx.message.delete()

  @discord.ui.button(label="關閉文字頻道通知", style=discord.ButtonStyle.gray, emoji='❌')
  async def wordtranslatevoice_callback(self,ctx,button):
    await ctx.message.delete()

  async def on_timeout(self):
    await self.embed_message.edit(view=None)

class voice(Cog_Extension):
  play_sequence = []
  requests_is_colddown = True
  requests_is_colddown_ara = True
  voice_new = 0
  voice_entering = False
  newest_msg_info = [0,0]

  class embed_tem:
    def embed(self, voicechannel):
      with open(control.state_file) as f:
        state = json.load(f)
  
      embed = discord.Embed(title="語音初始設定", color=0x00aeae)
      embed.add_field(name="進入頻道名稱", value=voicechannel)
  
      if state['voice']:
        wordtranslate = "啟動"
      else:
        wordtranslate = "關閉"
  
      if state['timevoice']:
        timevoice = "啟動"
      else:
        timevoice = "關閉"
  
      if state['listen_all']:
        translatemode = "啟動"
      else:
        translatemode = "關閉"
  
      if state['intochannel']:
        intochannel = "啟動"
      else:
        intochannel = "關閉"
      
      embed.add_field(name="報時功能", value=timevoice)
      embed.add_field(name="進出頻道通知", value=intochannel)
      embed.add_field(name="文字頻道通知", value=wordtranslate)
      embed.add_field(name="文字頻道範圍", value=translatemode)

      return embed

  def __init__(self,*arge,**kwargs):
    super().__init__(*arge,**kwargs)
    
    async def time_counter():

      await self.bot.wait_until_ready()

      """with open(control.state_file) as f:
        state = json.load(f)
      if not state['voice_connect'] == 0:
        self.channel = self.bot.get_channel(944199319731462154)
        await self.channel.send()"""
      
      while not self.bot.is_closed():
        now = time_myself.time_pane()
        if now % 100 == 0 and not voice.voice_new == 0:
          with open(control.state_file) as f:
            state = json.load(f)

          if state['timevoice']:
            pass
        
          elif now == 0:
            tts = gTTS(f"現在時間...凌晨0點整", lang="zh-tw")
          elif now/100 >= 18:
            tts = gTTS(f"現在時間...晚上{round(now/100-12)}點整", lang="zh-tw")
          elif now/100 <= 4:
            tts = gTTS(f"現在時間...凌晨{round(now/100)}點整", lang="zh-tw")
          elif now/100 <= 11:
            tts = gTTS(f"現在時間...上午{round(now/100)}點整", lang="zh-tw")
          elif now/100 == 12:
            tts = gTTS(f"現在時間...中午12點整", lang="zh-tw")
          else:
            tts = gTTS(f"現在時間...下午{round(now/100-12)}點整", lang="zh-tw")

          tts.save(f"./sound/time_{now}.mp3")

          voice.play_sequence.append({'path': f"./sound/time_{now}.mp3", 'is_deleteing': True})

          await asyncio.sleep(60)

        else:          
          await asyncio.sleep(60)

    self.bot.loop.create_task(time_counter())
            

  @commands.command()
  async def voice_in(self, ctx):
    voice.voice_entering = True
    channel = ctx.author.voice

    """with open(control.state_file) as f:
      state = json.load(f)"""
    
    if channel == None:
      await ctx.reply("你沒有已連接的頻道")
      await ctx.message.add_reaction("❌")
      return
      
    try:
      voice.voice_new = await channel.channel.connect()
      voice.voice_entering = False
      
      await ctx.message.add_reaction("✅")
    except:
      voice.voice_new = 0
      voice.voice_entering = False
      await ctx.message.add_reaction("❌")
      return

    await asyncio.sleep(3)

    """state['voice_connect'] = channel.channel.id
    with open(control.state_file, 'w') as f:
      f.write(json.dumps(state))"""

    """embed = voice.embed_tem.embed(channel.channel.name)
    view = view_bar()
    await ctx.reply(embed=embed, view=view)"""
    
    while not voice.voice_new == 0:
      
      if len(voice.play_sequence) > 0:
        while len(voice.play_sequence) > 0:
          try:
            going_play = voice.play_sequence[0]
            voice.voice_new.play(discord.FFmpegPCMAudio(going_play['path']))
  
            sound_time = load(going_play['path'])
            await asyncio.sleep(sound_time.info.time_secs+1)
            
            if going_play['is_deleteing']:
              os.remove(going_play['path'])

          except:
            pass

          try:
            voice.play_sequence.remove(going_play)
          except:
            pass
          
          await asyncio.sleep(0.5)
          
      await asyncio.sleep(5)
      
  @commands.command()
  async def voice_out(self, ctx):
    """with open(control.state_file) as f:
      state = json.load(f)"""
      
    try:
      await ctx.voice_client.disconnect()
      voice.voice_new = 0
      await ctx.message.add_reaction("✅")

      """state['voice_connect'] = 0
      with open(control.state_file, 'w') as f:
        f.write(json.dumps(state))"""
      
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def voice_nick(self, ctx, nick_name=None):
    with open('author_datafile/data.json',encoding="utf-8") as f:
      user_data = json.load(f)

    if nick_name == None:
      await ctx.message.add_reaction("❌")
      return

    if len(nick_name) > 8 or len(nick_name) <= 0:
      await ctx.reply("綽號短名過長，上限: 8")
      await ctx.message.add_reaction("❌")
      return

    p = re.compile('<:\w+:\d+>|<a:\w+:\d+>')
      
    em = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    if len(p.findall(nick_name)) == 0 and len(em.findall(nick_name)) == 0:
      user_data[str(ctx.author.id)] = nick_name
      try:
        with open('author_datafile/data.json', 'w',encoding="utf-8") as f:
          f.write(json.dumps(user_data))
        await ctx.message.add_reaction("✅")
      except Exception as e:
        print(e)
        await ctx.message.add_reaction("❌")
        
      return
      
    else:
      await ctx.reply("綽號短名只接受中英數文字")
      await ctx.message.add_reaction("❌")
      return
      
  @commands.Cog.listener()
  async def on_message(self, message):
    Speech = "zh-tw"
    list_vaule_in = False
    
    with open(control.state_file) as f:
      state = json.load(f)

    r_18_id = state['r_18_id']

    assect_chanel_id = state['assect_chanel_id']

    if message.channel.id in r_18_id:
      return

    if (not message.channel.id in assect_chanel_id) and (not state['listen_all']):
      return
      
    if state['voice'] and (not voice.voice_new == 0 and not message.author.bot):
      text_message = message.content
      if text_message.startswith(">") or text_message.startswith("!a"):
        return
      if text_message.startswith("http"):
        return

      vaule_only = ['-ve','-v']#,'-vs','-vp','-vf'

      for list_vaule in vaule_only:
        if text_message.endswith(list_vaule):
          list_vaule_in = True
          break

      if state['voice_mode'] == 'only' and not (message.author.id in state['only_voice'] and list_vaule_in):
        return

      if text_message[-3:] == '-vf':
        Speech = 'fr'
        
      elif text_message[-3:] == '-ve':
        Speech = 'en-US'

      elif text_message[-3:] == '-vs':
        Speech = 'es'

      elif text_message[-3:] == '-vp':
        Speech = 'pt'
        
      text_channel = message.channel.name

      with open('./author_datafile/data.json','r') as f:
        user_data = json.load(f)
        
      if str(message.author.id) in list(user_data.keys()):
        text_name = user_data[str(message.author.id)]
      else:
        try:
          text_name = str(message.author.nick)
        except:
          text_name = str(message.author.name)

      #print(text_name+'在'+text_channel+'說'+text_message)

      #p = re.compile('<:\w+:\d+>|<a:\w+:\d+>')
      
      em = re.compile("<:\w+:\d+>|<a:\w+:\d+>|["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
      
      #text_message = p.subn('', text_message)[0]
      text_message = em.subn('', text_message)[0]

      #text_name = p.subn('', text_name)[0]
      text_name = em.subn('', text_name)[0]

      #text_channel = p.subn('', text_channel)[0]
      text_channel = em.subn('', text_channel)[0]

      exclamations = re.compile('[!！]+')
      text_message = exclamations.subn('!', text_message)[0]

      questions = re.compile('[?？]+')
      text_message = questions.subn('?', text_message)[0]

      symbols = re.compile('[\&\$\^!?！？#%/,@.=\+\-\*\\\'\"\`]{3,}|[\_\~\|]{2,}')
      text_message = symbols.subn('', text_message)[0]

      www = re.compile('[wW]{3,}')
      text_message = www.subn('www', text_message)[0]

      text_message = text_message.replace("%", "啪")
      text_message = text_message.replace("百分號", "啪")
      text_message = text_message.replace("?", "問號")
      text_message = text_message.replace("!", "驚嘆號")
      text_message = text_message.replace(".", "點")
      #text_channel = em.subn('', text_channel)[0]

      #print(text_name+'在'+text_channel+'說'+text_message)

      tag = re.compile('<@\d+>|ta\d+g')
      user_id_list = tag.findall(text_message)

      for tag_str in user_id_list:
        try:
          user_info = self.bot.get_user(int(tag_str[2:-1]))
          if str(tag_str[2:-1]) in list(user_data.keys()):
            user = user_data[str(tag_str[2:-1])]
          else:
            try:
              user = user_info.nick
            except:
              user = user_info.name

            #user = p.subn('', user)[0]
            user = em.subn('', user)[0]

          text_message = re.compile(tag_str).subn('tag' + user +'...', text_message)[0]
        except:
          pass

      if text_message == '':
        return

      try:
        is_reply_msg = await message.channel.fetch_message(message.reference.message_id)
        
        if str(is_reply_msg.author.id) in list(user_data.keys()):
          reply_user = user_data[str(is_reply_msg.author.id)]
        else:
          try:
            reply_user = is_reply_msg.author.nick
          except:
            reply_user = is_reply_msg.author.name
          
        is_reply_addstr = f"回覆了{reply_user}的訊息並說："
      except:
        is_reply_addstr = ""

      try:
        waiting_code = len(voice.play_sequence)
        if state['voice_mode'] == 'only' and (message.author.id in state['only_voice']):
          tts = gTTS(text_name+is_reply_addstr[:-2]+"說："+text_message[:-2], lang=Speech) 
          tts.save(f"./sound/{waiting_code}.mp3")

        elif voice.newest_msg_info[1] == message.channel.id:
          tts = gTTS(text_name+is_reply_addstr[:-2]+"說："+text_message, lang=Speech) 
          tts.save(f"./sound/{waiting_code}.mp3")
          
        else:
          tts = gTTS(text_name+'在'+text_channel+is_reply_addstr[:-2]+'說:'+text_message, lang=Speech) 
          tts.save(f"./sound/{waiting_code}.mp3")

        #os.remove(f"./sound/{waiting_code}.mp3")

        voice.play_sequence.append({'path': f"./sound/{waiting_code}.mp3", 'is_deleteing': True})
        voice.newest_msg_info = [message.author.id,message.channel.id]

      except Exception as e:
        print(e)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    #if member.bot:
      #return
    await asyncio.sleep(1)
    if voice.voice_entering:
      return

    with open('author_datafile/state.json',encoding="utf-8") as f:
      state = json.load(f)
      
    if not state['intochannel']:
      return
    
    if voice.voice_new == 0:
      return

    try:
      member_voice_before = before.channel.id
    except:
      member_voice_before = None
    try:
      member_voice_after = after.channel.id
    except:
      member_voice_after = None

    if member_voice_before == member_voice_after:
      return

    with open('./author_datafile/data.json','r') as f:
      user_data = json.load(f)
      
    if str(member.id) in list(user_data.keys()):
        user = user_data[str(member.id)]
    else:
      try:
        user = member.nick
        if user == None:
          raise
      except:
        user = member.name
  
      p = re.compile('<:\w+:\d+>|<a:\w+:\d+>')
        
      em = re.compile("["
          u"\U0001F600-\U0001F64F"  # emoticons
          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
          u"\U0001F680-\U0001F6FF"  # transport & map symbols
          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                             "]+", flags=re.UNICODE)
        
      user = p.subn('', user)[0]
      user = em.subn('', user)[0]

    try:
      if member_voice_after == voice.voice_new.channel.id:
        model = '剛剛進入了頻道'
      if member_voice_before == voice.voice_new.channel.id:
        model = '剛剛離開了頻道'
        
      waiting_code = len(voice.play_sequence)
          
      with open('./sound/sequence.txt','w') as f:
        f.write(str(waiting_code))
          
      tts = gTTS(f'{user}{model}', lang="zh-tw") 
      tts.save(f"./sound/{waiting_code}.mp3")

      #os.remove(f"./sound/{waiting_code}.mp3")

      voice.play_sequence.append({'path': f"./sound/{waiting_code}.mp3", 'is_deleteing': True})

    except Exception as e:
      print(e)
  
  @commands.command()
  async def test_voice_play(self, ctx):
    with open(control.state_file) as f:
      state = json.load(f)

    if not state['voice']:
      await ctx.reply("語音功能已關閉")
      await ctx.message.add_reaction("❌")
      return
      
    if voice.voice_new == 0:
      await ctx.reply("無已連接頻道")
      await ctx.message.add_reaction("❌")
      return
      
    try:
      is_going_wait = len(voice.play_sequence) == 0
      voice.play_sequence.append({'path': "./sound/The_World_Of_Sound_Demo_Dolby_Atmos_Dolby.mp3", 'is_deleteing': False})
      #voice.voice_new.play(discord.FFmpegPCMAudio("./video/TEST VIDEO_v144P.mp4"))
      await ctx.message.add_reaction("✅")
      
      if is_going_wait:
        hint_msg = await ctx.reply("已加入撥放序列")
        await asyncio.sleep(3)
        await hint_msg.delete()
        
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def meme_rick(self, ctx):
    with open(control.state_file) as f:
      state = json.load(f)

    if not state['voice']:
      await ctx.reply("語音功能已關閉")
      await ctx.message.add_reaction("❌")
      return
      
    if voice.voice_new == 0:
      await ctx.reply("無已連接頻道")
      await ctx.message.add_reaction("❌")
      return
    
    try:
      chou_wo = random.choice(["rick_roll_long","rick_roll_short"])
      
      is_going_wait = len(voice.play_sequence) == 0
      voice.play_sequence.append({'path': "./sound/"+chou_wo+".mp3", 'is_deleteing': False})
      await ctx.message.add_reaction("✅")
      
      if is_going_wait:
        hint_msg = await ctx.reply("已加入撥放序列")
        await asyncio.sleep(3)
        await hint_msg.delete()
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def meme_padoru(self, ctx):
    with open(control.state_file) as f:
      state = json.load(f)

    if not state['voice']:
      await ctx.reply("語音功能已關閉")
      await ctx.message.add_reaction("❌")
      return
    if voice.voice_new == 0:
      await ctx.reply("無已連接頻道")
      await ctx.message.add_reaction("❌")
      return
    
    try:
      is_going_wait = not (len(voice.play_sequence) == 0)
      voice.play_sequence.append({'path': "./sound/"+"padoru"+".mp3", 'is_deleteing': False})
      await ctx.message.add_reaction("✅")
      
      if is_going_wait:
        hint_msg = await ctx.reply("已加入撥放序列")
        await asyncio.sleep(3)
        await hint_msg.delete()
      #chou_wo = random.choice(["rick_roll_long","rick_roll_short"""])
      
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def Buddhist_scriptures(self, ctx):
    with open(control.state_file) as f:
      state = json.load(f)

    if not state['voice']:
      await ctx.reply("語音功能已關閉")
      await ctx.message.add_reaction("❌")
      return
    if voice.voice_new == 0:
      await ctx.reply("無已連接頻道")
      await ctx.message.add_reaction("❌")
      return
    
    try:
      is_going_wait = not (len(voice.play_sequence) == 0)
      voice.play_sequence.append({'path': "./sound/Buddhist_scriptures.mp3", 'is_deleteing': False})
      await ctx.message.add_reaction("✅")
      
      if is_going_wait:
        hint_msg = await ctx.reply("已加入撥放序列")
        await asyncio.sleep(3)
        await hint_msg.delete()
      
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def wah(self, ctx, *times):
    if not voice.requests_is_colddown:
      await ctx.reply("請等候冷卻,wah!")
      await ctx.message.add_reaction("❌")
      return
    
    with open(control.state_file) as f:
      state = json.load(f)

    if not state['voice']:
      await ctx.reply("語音功能已關閉,wah!")
      await ctx.message.add_reaction("❌")
      return
    if voice.voice_new == 0:
      await ctx.reply("無已連接頻道,wah!")
      await ctx.message.add_reaction("❌")
      return
    
    voice.requests_is_colddown = False
    await ctx.message.add_reaction("🔄")

    try:
      for_times = int(times[0])
      if for_times > 25:
        for_times = 20
        
    except:
      for_times = 1
      
    try:
      for i in range(0,for_times):
        wah_get = str(random.randint(1,481))
  
        wah_get = wah_get.zfill(3)
        
        #print(f"https://inanoises.com/resources/noises/WAH_0{wah_get}.mp3")
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) Safari/537.36'}
        wah_sound = requests.get(f"https://inanoises.com/resources/noises/WAH_0{wah_get}.mp3", headers = headers)
        
        if wah_sound.status_code in [requests.codes.ok, requests.codes.not_modified, requests.codes.already_reported]:
          with open(f"sound/wah_0{wah_get}.mp3","wb") as f:
            f.write(wah_sound.content)

          await asyncio.sleep(0.5)

          """if random.randint(1,11) <= 3:
            with open(f"sound/wah_file/wah_0{wah_get}.mp3","wb") as f:
              f.write(wah_sound.content)"""

          voice.play_sequence.append({'path': f"sound/wah_0{wah_get}.mp3", 'is_deleteing': True})
          
        else:
          wah_file_get = random.choice(os.listdir("./sound/wah_file/"))
            
          voice.play_sequence.append({'path': f"./sound/wah_file/{wah_file_get}", 'is_deleteing': False})

          await asyncio.sleep(0.5)

      await ctx.message.add_reaction("✅")
      
    except:
      await ctx.message.add_reaction("❌")

    finally:
      await asyncio.sleep(1)
      voice.requests_is_colddown = True
  
  @commands.command()
  async def ara(self, ctx, *times):
    if not voice.requests_is_colddown_ara:
      await ctx.reply("請等候冷卻")
      await ctx.message.add_reaction("❌")
      return
    
    with open(control.state_file) as f:
      state = json.load(f)

    if not state['voice']:
      await ctx.reply("語音功能已關閉,wah!")
      await ctx.message.add_reaction("❌")
      return
    if voice.voice_new == 0:
      await ctx.reply("無已連接頻道")
      await ctx.message.add_reaction("❌")
      return
    
    voice.requests_is_colddown_ara = False
    await ctx.message.add_reaction("🔄")

    try:
      for_times = int(times[0])
      if for_times > 25:
        for_times = 20
        
    except:
      for_times = 1
      
    try:
      for i in range(0,for_times):
        ara_get = str(random.randint(10,512))
  
        #ara_get = ara_get.zfill(3)
        
        #print(f"https://faunaraara.com/sounds/ara-{ara_get}.mp3")
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) Safari/537.36'}
        ara_sound = requests.get(f"https://faunaraara.com/sounds/ara-{ara_get}.mp3", headers = headers)
        
        if ara_sound.status_code in [requests.codes.ok, requests.codes.not_modified, requests.codes.already_reported]:
          with open(f"sound/ara-{ara_get}.mp3","wb") as f:
            f.write(ara_sound.content)

          await asyncio.sleep(0.5)

          """if random.randint(1,11) <= 3:
            with open(f"sound/wah_file/wah_0{ara_get}.mp3","wb") as f:
              f.write(wah_sound.content)"""

          voice.play_sequence.append({'path': f"sound/ara-{ara_get}.mp3", 'is_deleteing': True})
          
        else:
          await ctx.message.add_reaction("❌")

      await ctx.message.add_reaction("✅")
      
    except:
      await ctx.message.add_reaction("❌")

    finally:
      await asyncio.sleep(1)
      voice.requests_is_colddown_ara = True
    
async def setup(bot):
  await bot.add_cog(voice(bot))