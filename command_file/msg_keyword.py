import discord
import os, sys
import re
import json
from discord.ext import commands

import random
from cog import Cog_Extension
import time
import asyncio
import requests

sys.path.append(os.pardir)

class msg_keyword(Cog_Extension):
  @commands.command()
  async def seekeyword(self,ctx):#display all keywords
      with open('users_datafile/keyword.json') as f:#open keyword file
        keywords = json.load(f)
      
      try:
        embed = discord.Embed(title="keyword_list (15秒後刪除)", color=0xffffff)

        embed.set_footer(text="此機器人由 wannaZzz#8989 維護")

        
        key_count = len(keywords)

        meme_keys = list(keywords.keys())

        value = meme_keys[0]
        
        for key in range(1,key_count):
          value += ', ' + meme_keys[key]
          
        embed.add_field(name='關鍵字清單',value=value,inline=True)

        tmpmsg = await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")
        await asyncio.sleep(15)
        await tmpmsg.delete()
        return

      except Exception as e:
        print(e)
        await ctx.message.add_reaction("❌")

  @commands.command()
  async def newkeyword(self,ctx,*key_name):#append new keyword in list
    with open('users_datafile/keyword.json') as f:
      keywords = json.load(f)

    try:
      key = key_name[0].lower()

      if key == "":
        await ctx.reply('關鍵字不可為空')
        await ctx.message.add_reaction("❌")
        return
      if len(key) <= 3 and (ord(key[0]) <= 126 and ord(key[0]) >= 32):#keyword setting restriction(text limit)
        await ctx.reply('英數關鍵字不可少於3')
        await ctx.message.add_reaction("❌")
        return

    except Exception as e:
      print(e)
      await ctx.reply('無關鍵字或程式錯誤')
      await ctx.message.add_reaction("❌")
      return

    try:#get picture url
      add_vaule = ctx.message.attachments[0].url
    except:
      try:
        add_vaule = key_name[1]
      except:
        await ctx.reply('無圖片來源')
        await ctx.message.add_reaction("❌")
        return

    try:
      old = keywords[key]
    except:
      old = []

    if add_vaule in old:
      await ctx.reply('已有相同圖片來源')
      await ctx.message.add_reaction("❌")
      return
    if not add_vaule[:4] in "http":
      await ctx.reply('圖片來源非網址錯誤')
      await ctx.message.add_reaction("❌")
      return

    vaule = old + [add_vaule]

    keywords[key] = vaule

    with open('author_datafile/keyword.json','w') as f:
      f.write(json.dumps(keywords))
    
    await ctx.message.add_reaction("✅")

  @commands.Cog.listener()
  async def on_message(self, message):#detect keyword
    with open('users_datafile/state.json') as f:
      state = json.load(f)

    r_18_id = state['r_18_id']
    
    if message.author.bot:
      return

    if message.channel.id in r_18_id:#avoid send message in nsfw channel
      return

    percent = random.randint(1,11)#set trigger chance(30%)
    mess = message.content

    if len(message.content) <= 0:
      return

    if mess.startswith("http"):
      return

    try:
      #print(mess[:4])
      if mess.startswith("-key"):
        percent = 0
    except:
      pass
      
    if (state['noise'] and not (mess.startswith(">") or mess.startswith("!a"))) and percent <= 3:#set trigger chance(30%)
      data_pick = []#all can be sended picture list
      mess = mess.lower()
      
      with open('users_datafile/keyword.json') as f:#open keyword file
          keyword_data = json.load(f)
          keywords = keyword_data.keys()
      for keyword in keywords:
          if keyword in mess:
            chou_wo = random.choice(keyword_data[keyword])
            data_pick.append(chou_wo)

      pisk = random.choice(data_pick)

    if percent <= 3:
      try:
        await asyncio.sleep(180)
        await message_send.delete()
      except:
        pass

  @commands.command()
  async def emoji_grab(self,ctx,*input):#use to get emoji and stickers from discord
    try:
      message_reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
    except:
      try:
        self.channel = self.bot.get_channel(int(input[1]))
        message_reply = await self.channel.fetch_message(input[0])

      except:
        await ctx.message.add_reaction("❌")
        return
    
    result = re.findall("<:\w+:\d+>|<a:\w+:\d+>",message_reply.content)#find all discord's emoji in content

    out_put_string = ""

    for emoji_code in result:
      emoji_id = emoji_code.split(':')[2][:-1]
      r = requests.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.gif")
  
      if r.status_code == requests.codes.ok:
        out_put_string += f"https://cdn.discordapp.com/emojis/{emoji_id}.gif?size=96&quality=lossless\n"
      else:
        out_put_string += f"https://cdn.discordapp.com/emojis/{emoji_id}.png?size=96&quality=lossless\n"

    stickers = message_reply.stickers#get sticker in message
    for stick in stickers:
      sticker_id = stick.id
      out_put_string += f"https://cdn.discordapp.com/stickers/{sticker_id}.png\n"

    await ctx.reply(out_put_string)
    await ctx.message.add_reaction("✅")
    

async def setup(bot):
  await bot.add_cog(msg_keyword(bot))