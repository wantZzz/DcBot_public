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

from cog import Cog_Extension

#https://yout.com/ 時間軸剪輯

class voice(Cog_Extension):
  play_sequence = []#all already going to play sound files well append in this list
  requests_is_colddown = True#this vaule is for ">wah" command, which use at let this command not use too many times in short time
  voice_channel = 0#if voice_channel is 0, means bot haven't connect any voice channel
  voice_entering = False#if it is True, means bot is trying connect to voice channel
  newest_msg_info = [0,0]#record newest message info

  def __init__(self,*arge,**kwargs):
    super().__init__(*arge,**kwargs)
    
    async def time_counter():#timer

      await self.bot.wait_until_ready()
      
      while not self.bot.is_closed():
        now = time_myself.time_pane()
        if now % 100 == 0 and not voice.voice_new == 0:
          with open('users_datafile/state.json') as f:
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

          voice.play_sequence.append({'path': f"./sound/time_{now}.mp3", 'is_deleteing': True})#append to play list

          await asyncio.sleep(60)

        else:          
          await asyncio.sleep(60)

    self.bot.loop.create_task(time_counter())
            

  @commands.command()
  async def voice_in(self, ctx):#connect to voice channel
    voice.voice_entering = True
    channel = ctx.author.voice
    
    if channel == None:#check user isn't connect to any voice channel
      await ctx.reply("你沒有已連接的頻道")
      await ctx.message.add_reaction("❌")
      return
      
    try:#get user's connect voice channel
      voice.voice_channel = await channel.channel.connect()
      voice.voice_entering = False
      
      await ctx.message.add_reaction("✅")
    except:
      voice.voice_channel = 0
      voice.voice_entering = False
      await ctx.message.add_reaction("❌")
      return

    await asyncio.sleep(3)
    
    while not voice.voice_channel == 0:#run until leave from voice channel
      
      if len(voice.play_sequence) > 0:#check play sequence isn't it empty
        while len(voice.play_sequence) > 0:#play all sound sources in list
          try:
            going_play = voice.play_sequence[0]
            voice.voice_channel.play(discord.FFmpegPCMAudio(going_play['path']))
  
            sound_time = load(going_play['path'])
            await asyncio.sleep(sound_time.info.time_secs+1)#wait for sources finished playing
            
            if going_play['is_deleteing']:#if it is True, it mean this sound sources need to delete
              os.remove(going_play['path'])

          except:
            pass

          try:
            voice.play_sequence.remove(going_play)
          except:
            pass
          
          await asyncio.sleep(0.5)#set the playback interval between all sound sources
          
      await asyncio.sleep(5)#set the interval between every list check
      
  @commands.command()
  async def voice_out(self, ctx): #leave from voice channel   
    try:
      await ctx.voice_client.disconnect()
      voice.voice_channel = 0
      await ctx.message.add_reaction("✅")
      
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def voice_nick(self, ctx, nick_name=None):#set users nickname when bot mentioned them
    with open('users_datafile/data.json') as f:
      user_data = json.load(f)

    if nick_name == None:
      await ctx.message.add_reaction("❌")
      return

    if len(nick_name) > 8 or len(nick_name) <= 0:#nickname setting restriction(word count limit)
      await ctx.reply("綽號短名過長，上限: 8")
      await ctx.message.add_reaction("❌")
      return

    p = re.compile('<:\w+:\d+>|<a:\w+:\d+>')#remove all emoji for discord in content
      
    em = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    if len(p.findall(nick_name)) == 0 and len(em.findall(nick_name)) == 0:#nickname setting restriction(text limit)
      user_data[str(ctx.author.id)] = nick_name
      try:
        with open('users_datafile/data.json', 'w') as f:#write into user nickname file
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
  async def on_message(self, message):#get every message in server, and turn into sound sources
    Speech = "zh-tw"#TTS laguage mode initial setting
    is_accept_laguage = False
    
    with open('users_datafile/state.json') as f:
      state = json.load(f)

    r_18_id = state['r_18_id']

    assect_chanel_id = state['assect_chanel_id']

    if message.channel.id in r_18_id:#avoid translate message in nsfw channel
      return

    if (not message.channel.id in assect_chanel_id) and (not state['listen_all']):#when listen_all is "only", if cached message isn't in accept translate channel list, don't translate this message
      return
      
    if state['voice'] and (not voice.voice_new == 0 and not message.author.bot):#if prefix is other bot prefix, don't translate this message
      text_message = message.content
      if text_message.startswith(">") or text_message.startswith("!a"):
        return
      if text_message.startswith("http"):
        return

      accept_laguage_list = ['-ve','-v']#'-vs','-vp','-vf'

      for accept_laguage in accept_laguage_list:#check laguage mode is accept
        if text_message.endswith(accept_laguage):
          is_accept_laguage= True
          break

      if state['voice_mode'] == 'only' and not (message.author.id in state['only_voice'] and is_accept_laguage):#when listen_all is "only", all not in only_voice list user's message well not be translate
        return

      if text_message[-3:] == '-vf':
        Speech = 'fr'
        
      elif text_message[-3:] == '-ve':
        Speech = 'en-US'

      elif text_message[-3:] == '-vs':
        Speech = 'es'

      elif text_message[-3:] == '-vp':
        Speech = 'pt'
        
      channel_name = message.channel.name

      with open('users_datafile/data.json','r') as f:#open users nickname file
        user_data = json.load(f)
        
      if str(message.author.id) in list(user_data.keys()):#find users nickname
        text_name = user_data[str(message.author.id)]
      else:
        try:
          text_name = str(message.author.nick)
        except:
          text_name = str(message.author.name)
      
      em = re.compile("<:\w+:\d+>|<a:\w+:\d+>|["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)#clear all emoji in content
      
      text_message = em.subn('', text_message)[0]

      text_name = em.subn('', text_name)[0]

      channel_name = em.subn('', channel_name)[0]

      exclamations = re.compile('[!！]+')#nickname setting restriction(avoid too many !)
      text_message = exclamations.subn('!', text_message)[0]

      questions = re.compile('[?？]+')#nickname setting restriction(avoid too many ?)
      text_message = questions.subn('?', text_message)[0]

      symbols = re.compile('[\&\$\^!?！？#%/,@.=\+\-\*\\\'\"\`]{3,}|[\_\~\|]{2,}')#nickname setting restriction(avoid too many symbol)
      text_message = symbols.subn('', text_message)[0]

      www = re.compile('[wW]{3,}')#nickname setting restriction(avoid too many w, short it to 3 word)
      text_message = www.subn('www', text_message)[0]

      text_message = text_message.replace("%", "啪")
      text_message = text_message.replace("百分號", "啪")
      text_message = text_message.replace("?", "問號")
      text_message = text_message.replace("!", "驚嘆號")
      text_message = text_message.replace(".", "點")

      #print(text_name+'在'+channel_name+'說'+text_message)

      tag = re.compile('<@\d+>|ta\d+g')#if message have tag someone
      user_id_list = tag.findall(text_message)

      for tag_id_data in user_id_list:
        try:
          user_info = self.bot.get_user(int(tag_id_data[2:-1]))#get user info
          if str(tag_id_data[2:-1]) in list(user_data.keys()):#find users nickname
            user = user_data[str(tag_id_data[2:-1])]
          else:
            try:
              user = user_info.nick
            except:
              user = user_info.name

            user = em.subn('', user)[0]

          text_message = re.compile(tag_id_data).subn('tag' + user +'...', text_message)[0]
        except:
          pass

      if text_message == '':
        return

      try:#if this message reply other message
        is_reply_msg = await message.channel.fetch_message(message.reference.message_id)
        
        if str(is_reply_msg.author.id) in list(user_data.keys()):#find replyed user nickname
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

        elif voice.newest_msg_info[1] == message.channel.id:#if last message also form same user
          tts = gTTS(text_name+is_reply_addstr[:-2]+"說："+text_message, lang=Speech) 
          tts.save(f"./sound/{waiting_code}.mp3")
          
        else:
          tts = gTTS(text_name+'在'+channel_name+is_reply_addstr[:-2]+'說:'+text_message, lang=Speech) 
          tts.save(f"./sound/{waiting_code}.mp3")

        voice.play_sequence.append({'path': f"sound/{waiting_code}.mp3", 'is_deleteing': True})#append source path into list
        voice.newest_msg_info = [message.author.id,message.channel.id]#record newest message info

      except Exception as e:
        print(e)

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):#report when someont come into/leaf out voice channel
    await asyncio.sleep(1)
    
    if voice.voice_entering:
      return

    with open('users_datafile/state.json') as f:
      state = json.load(f)
      
    if not state['intochannel']:#if it is True, means accept report this event
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

    with open('users_datafile/data.json','r') as f:#open users nickname file
      user_data = json.load(f)
      
    if str(member.id) in list(user_data.keys()):#find come into/leaf out voice channel user nickname
        user = user_data[str(member.id)]
    else:
      try:
        user = member.nick
        if user == None:
          raise
      except:
        user = member.name
        
      em = re.compile("["
          u"\U0001F600-\U0001F64F"  # emoticons
          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
          u"\U0001F680-\U0001F6FF"  # transport & map symbols
          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                             "]+", flags=re.UNICODE)#clear all emoji in content
        
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

      voice.play_sequence.append({'path': f"./sound/{waiting_code}.mp3", 'is_deleteing': True})#append source path into list

    except Exception as e:
      print(e)
  
  @commands.command()
  async def test_voice_play(self, ctx):#play testing sound source
    with open('users_datafile/state.json') as f:
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

      await ctx.message.add_reaction("✅")
      
      if is_going_wait:
        hint_msg = await ctx.reply("已加入撥放序列")
        await asyncio.sleep(3)
        await hint_msg.delete()
        
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def meme_rick(self, ctx):#play rick_roll
    with open('users_datafile/state.json') as f:
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
  async def meme_padoru(self, ctx):#play padoru~padoru~
    with open('users_datafile/state.json') as f:
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
      
    except:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def Buddhist_scriptures(self, ctx):
    with open('users_datafile/state.json') as f:#plar buddhist_scriptures(Zh)
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
  async def wah(self, ctx, *times):#play Ina wah
    if not voice.requests_is_colddown:
      await ctx.reply("請等候冷卻,wah!")
      await ctx.message.add_reaction("❌")
      return
      
    voice.requests_is_colddown = False
    
    with open('users_datafile/state.json') as f:
      state = json.load(f)

    if not state['voice']:
      await ctx.reply("語音功能已關閉,wah!")
      await ctx.message.add_reaction("❌")
      return
    if voice.voice_new == 0:
      await ctx.reply("無已連接頻道,wah!")
      await ctx.message.add_reaction("❌")
      return
      
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
        wah_sound = requests.get(f"https://inanoises.com/resources/noises/WAH_0{wah_get}.mp3", headers = headers)#quest source form inanoises.com database
        
        if wah_sound.status_code in [requests.codes.ok, requests.codes.not_modified, requests.codes.already_reported]:
          with open(f"sound/wah_0{wah_get}.mp3","wb") as f:#download to file
            f.write(wah_sound.content)

          await asyncio.sleep(0.5)

          voice.play_sequence.append({'path': f"sound/wah_0{wah_get}.mp3", 'is_deleteing': True})#append in list
          
        else:#if cannot get source, used source which in local folder
          wah_file_get = random.choice(os.listdir("./sound/wah_file/"))
            
          voice.play_sequence.append({'path': f"./sound/wah_file/{wah_file_get}", 'is_deleteing': False})

          await asyncio.sleep(0.5)

      await ctx.message.add_reaction("✅")
      
    except:
      await ctx.message.add_reaction("❌")

    finally:
      await asyncio.sleep(1)
      voice.requests_is_colddown = True
    
async def setup(bot):
  await bot.add_cog(voice(bot))