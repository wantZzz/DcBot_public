import discord
import sys
import os
import re
import json
from discord.ext import commands

import random
from cog import Cog_Extension
import time
import asyncio
import requests

sys.path.append(os.pardir)
from command_file.control import control

class msg_keyword(Cog_Extension): 
  @commands.command()
  async def seekeyword(self,ctx):
      with open('author_datafile/keyword.json',encoding="utf-8") as f:
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
  async def newkeyword(self,ctx,*key_name):
    with open('author_datafile/keyword.json',encoding="utf-8") as f:
      keywords = json.load(f)

    try:
      key = key_name[0].lower()

      if key == "":
        await ctx.reply('關鍵字不可為空')
        await ctx.message.add_reaction("❌")
        return
      if len(key) <= 3 and (ord(key[0]) <= 126 and ord(key[0]) >= 32):
        await ctx.reply('英數關鍵字不可少於3')
        await ctx.message.add_reaction("❌")
        return

    except Exception as e:
      print(e)
      await ctx.reply('無關鍵字或程式錯誤')
      await ctx.message.add_reaction("❌")
      return

    try:
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

    with open('author_datafile/keyword.json','w',encoding="utf-8") as f:
      f.write(json.dumps(keywords))
    
    await ctx.message.add_reaction("✅")

  @commands.Cog.listener()
  async def on_message(self, message):
    with open(control.state_file) as f:
      state = json.load(f)

    r_18_id = state['r_18_id']
    
    if message.author.bot:
      return

    if message.channel.id in r_18_id:
      return

    percent = random.randint(1,11)
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
      
    if (state['noise'] and not (mess.startswith(">") or mess.startswith("!a"))) and percent <= 3:
      #mess = message.content

      data_pick = []
      mess = mess.lower()

      if ("不可以色色" in mess)or("不可以澀澀" in mess):
        chou_wo = random.choice(['https://cdn.discordapp.com/attachments/869714477510193183/907078587268612116/FB_IMG_1634486965934.jpg', 'https://cdn.discordapp.com/attachments/869714477510193183/909753962436128838/images.jpg','https://media.discordapp.net/attachments/611591145511976992/919095611368800266/1638152389.gif','https://media.discordapp.net/attachments/873837336851533854/932212954940723210/FB_IMG_1642319239027.jpg','https://cdn.discordapp.com/attachments/873837336851533854/939135603692417154/777yx-2sx4i.gif','https://cdn.discordapp.com/attachments/865887212205768714/875273799950548992/Screen_Shot_2020-04-28_at_12.21.48_PM.png','https://cdn.discordapp.com/attachments/873837336851533854/898710052163186708/image0.gif','https://images-ext-2.discordapp.net/external/D8xZTDTrwMy1z2tkVsGU5kTxkOQs5uJm_P-XHU8PjfA/https/media.discordapp.net/attachments/869714477510193183/897650650295468084/5387651fdc9b8c3676c7ec8cc7f41590.gif'])
        #message_send = await message.reply(chou_wo)
        data_pick.append(chou_wo)

      if ("可以色色" in mess)or("可以澀澀" in mess):
        #message_send = await message.reply(file=discord.File('./picture/2MUqaS8h.jpg'))
        data_pick.append(discord.File('./picture/2MUqaS8h.jpg'))

      if (("ㄌㄌ" in mess)or("蘿莉" in mess))and(("香" in mess)or("棒" in mess)):
        chou_wo = random.choice(['https://cdn.discordapp.com/attachments/901476467660185672/939175074785808415/image0.jpg', 'https://cdn.discordapp.com/attachments/865887212205768714/874294568709939210/FB_IMG_1608901401410.jpg',discord.File('./picture/image0.jpg')])
        #message_send = await message.reply(file=discord.File('./picture/image0.jpg'))
        data_pick.append(chou_wo)

      if ("在共三小" in mess) or ("在供三小" in mess) or ("在公三小" in mess):
        chou_wo = random.choice(['https://cdn.discordapp.com/attachments/869714477510193183/924126538260181022/cachedImage.png', 'https://cdn.discordapp.com/attachments/869714477510193183/922686097564262410/hjt9fxd47d371.jpg','https://cdn.discordapp.com/attachments/869714477510193183/913711903522570260/received_208860701256124.jpeg'])
        #message_send = await message.reply(chou_wo)
        data_pick.append(chou_wo)

      if ("哭阿" in mess)or("哭啊" in mess):
        chou_wo = random.choice(['./picture/cowa.jpg', './picture/rcdqp.jpg'])
        #message_send = await message.reply(file=discord.File(chou_wo))
        data_pick.append(discord.File(chou_wo))

      if ("我不知道" in mess)or("窩不知道" in mess):
        chou_wo = random.choice(['https://tenor.com/view/%E7%AA%A9%E4%B8%8D%E7%9F%A5%E9%81%93-gif-19458071', 'https://cdn.discordapp.com/attachments/886787844067172372/901762366730010644/Screenshot_20210415-000200_1.png'])
        #message_send = await message.reply(chou_wo)
        data_pick.append(chou_wo)

      if ("看戲" in mess)or("吃瓜" in mess):
        #message_send = await message.reply("https://cdn.discordapp.com/attachments/869714477510193183/909405586813235270/FB_IMG_1634917244780.jpg")
        data_pick.append("https://cdn.discordapp.com/attachments/869714477510193183/909405586813235270/FB_IMG_1634917244780.jpg")

      if ("怕暴" in mess)or("怕豹" in mess):
        #message_send = await message.reply("https://cdn.discordapp.com/attachments/869714477510193183/913034037893926952/37972766.jpg")
        data_pick.append("https://cdn.discordapp.com/attachments/869714477510193183/913034037893926952/37972766.jpg")

      if ("西臺灣" in mess)or("辱華" in mess)or("西台灣" in mess)or("乳滑" in mess):
        #message_send = await message.reply("https://media.discordapp.net/attachments/869714477510193183/932238943188054106/FB_IMG_1630822306731.jpg")
        data_pick.append("https://media.discordapp.net/attachments/869714477510193183/932238943188054106/FB_IMG_1630822306731.jpg")

      if ("我不行了" in mess)or("painpeko" in mess)or("pekopain" in mess):
        #message_send = await message.reply("https://media.discordapp.net/attachments/873837336851533854/932569826172473354/received_987742081953298.jpeg")
        data_pick.append("https://media.discordapp.net/attachments/873837336851533854/932569826172473354/received_987742081953298.jpeg")

      if "路過" in mess:
        #message_send = await message.reply(file=discord.File('./picture/TOP10.gif'))
        data_pick.append(discord.File('./picture/TOP10.gif'))

      if ("為什麼?" in mess)or("為什麼？" in mess):
        #message_send = await message.reply(file=discord.File('./picture/why.jpg'))
        data_pick.append(discord.File('./picture/why.jpg'))
      
      if "只是看著" in mess:
        #message_send = await message.reply(file=discord.File('./picture/watch.png'))
        data_pick.append(discord.File('./picture/watch.png'))

      if ("抽" in mess)and(("暴" in mess)or("死" in mess)):
        chou_wo = random.choice(["https://img.doutuwang.com/2020/11/006srDtYgy1giib5h93nej30dw0dwt9h.jpg", "https://img.nga.178.com/attachments/mon_202101/22/-klbw3Q16o-6ai1Z1hT3cSm8-ci.png"])
        #message_send = await message.reply(chou_wo)
        data_pick.append(chou_wo)

      
      with open('author_datafile/keyword.json',encoding="utf-8") as f:
          keyword_data = json.load(f)
          keywords = keyword_data.keys()
      for keyword in keywords:
          if keyword in mess:
            chou_wo = random.choice(keyword_data[keyword])
            #message_send = await message.reply(chou_wo)
            data_pick.append(chou_wo)
            #break

      pisk = random.choice(data_pick)
      if isinstance(pisk, discord.File):
        message_send = await message.reply(file=pisk)
      else:
        message_send = await message.reply(pisk)

    """if state['record']:
      id_inp = message.id
      now = time.localtime(time.time())
      mse_send_time = now.tm_sec + now.tm_min * 100 + ((now.tm_hour + 8 + 24) % 24) * 10000
      #print(mse_send_time)
      db_re[str(id_inp)] = mse_send_time"""

    if message.author.id in state["weird_quest"]:
      id = message.author.id
      with open('author_datafile/weird_quest.json',encoding="utf-8") as f:
        weird_quest_json = json.load(f)
      
      state["weird_quest"].remove(id)
    
      with open('author_datafile/state.json', 'w',encoding="utf-8") as f:
        f.write(json.dumps(state))
    
      await message.reply(f"{weird_quest_json[str(id)]['nes']}\n{random.choice(weird_quest_json[str(id)]['ran'])}")

    if percent <= 3:
      try:
        await asyncio.sleep(180)
        await message_send.delete()
      except:
        pass
      
  @commands.command()
  async def keyword_diedlink(self, ctx):
    try:
      message_reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
      diedlink = message_reply.content
    except:
      await ctx.reply('無回覆訊息')
      await ctx.message.add_reaction("❌")
      return
    
    if not message_reply.author.id == 901468849587765288:
      await ctx.reply('回覆訊息錯誤')
      await ctx.message.add_reaction("❌")
      return
    
    try:
      keyword_msg = await ctx.message.channel.fetch_message(message_reply.reference.message_id)
      mess = keyword_msg.content
    except:
      await ctx.reply('原始觸發訊息已被刪除，無法擷取關鍵字')
      await ctx.message.add_reaction("❌")
      return
    
    with open('author_datafile/keyword.json',encoding="utf-8") as f:
      keyword_data = json.load(f)
      keywords = keyword_data.keys()
      
    is_found = False
      
    for keyword in keywords:
      if keyword in mess:
        if diedlink in keyword_data[keyword]:
          keyword_data[keyword].remove(diedlink)
          is_found = True
          break
    
    if is_found:
      with open('author_datafile/keyword.json','w',encoding="utf-8") as f:
        f.write(json.dumps(keyword_data))
      await ctx.message.add_reaction("✅")
    else:
      await ctx.message.add_reaction("❌")

  @commands.command()
  async def emoji_grab(self,ctx,*input):
    try:
      message_reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
    except:
      try:
        self.channel = self.bot.get_channel(int(input[1]))
        message_reply = await self.channel.fetch_message(input[0])

      except:
        await ctx.message.add_reaction("❌")
        return
    
    result = re.findall("<:\w+:\d+>|<a:\w+:\d+>",message_reply.content)

    out_put_string = ""

    for emoji_code in result:
      emoji_id = emoji_code.split(':')[2][:-1]
      r = requests.get(f"https://cdn.discordapp.com/emojis/{emoji_id}.gif")
  
      if r.status_code == requests.codes.ok:
        out_put_string += f"https://cdn.discordapp.com/emojis/{emoji_id}.gif?size=96&quality=lossless\n"
      else:
        out_put_string += f"https://cdn.discordapp.com/emojis/{emoji_id}.png?size=96&quality=lossless\n"

    stickers = message_reply.stickers
    for stick in stickers:
      sticker_id = stick.id
      out_put_string += f"https://cdn.discordapp.com/stickers/{sticker_id}.png\n"

    await ctx.reply(out_put_string)
    await ctx.message.add_reaction("✅")
    

async def setup(bot):
  await bot.add_cog(msg_keyword(bot))