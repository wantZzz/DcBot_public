import discord
import sys
import os
import json
import asyncio
from discord.ext import commands
from discord.ui import Button,View
from discord import app_commands
from discord.app_commands import Choice

import time_myself
import traceback

from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont

import requests
from cog import Cog_Extension

sys.path.append(os.pardir)

with open('author_datafile/waifu_tag.json',encoding="utf-8") as e:
  WAIFU_TAG = json.load(e)

WAIFU_TAGS_SAFE = []
WAIFU_TAGS_NSFW = []

count_tags = 0
TAGS_LIST = []

for tags in WAIFU_TAG['tags_list']:
  WAIFU_TAGS_SAFE.append(Choice(name=tags, value=count_tags))
  WAIFU_TAGS_NSFW.append(Choice(name=tags, value=count_tags))
  
  TAGS_LIST.append(tags)
  count_tags += 1

for tags in WAIFU_TAG['nsfw_list']:
  WAIFU_TAGS_NSFW.append(Choice(name=tags, value=count_tags))
  
  TAGS_LIST.append(tags)
  count_tags += 1
  
def log_write(error, error_tag):
  with open('author_datafile/state.json',encoding="utf-8") as f:
      state = json.load(f)
      
  with open(state['log_name'], 'a') as f:
    f.write(str(time_myself.time_str_hour_to_second_add_colon())+" ")
    f.write(f'{error_tag} function: {error} \n')
    
  try:
    error_output_str = f'type_of_error: {type(error)}\nIgnoring exception in command:\n\n'
    file_name = f"error_event/{time_myself.time_str_year_to_day()}_{time_myself.time_str_hour_to_second()}.txt"
    with open(file_name, 'w') as f:
      f.write(error_output_str)
    
    traceback.print_exception(type(error), error, error.__traceback__, file=open(file_name, 'a'))
  except:
    return
  
def requests_waifu_data(nsfw_mode, model):
  if nsfw_mode:
    url = f"https://api.waifu.im/search?included_tags={model}&is_nsfw=true"
  else:
    url = f"https://api.waifu.im/search?included_tags={model}&is_nsfw=false"
        
  r = requests.get(url)
  
  if r.status_code == requests.codes.ok:
    try:
      requests_json_data = r.json()
      
      img_url = requests_json_data['images'][0]['url']
      source_url = requests_json_data['images'][0]['source']
      is_nsfw = requests_json_data['images'][0]['is_nsfw']
      
      if is_nsfw:
        title = f"🔞random waifu({model})"
      else:
        title = f"random waifu({model})"
        
      embed = discord.Embed(title=title, color=0xe77ed9)
      embed.add_field(name='source:', value=source_url)

      embed.set_image(url=img_url)
      
      embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')
      
      view = waifu_data_barview(img_url, source_url, is_nsfw, model)
      
      return embed, view
    
    except Exception as e:
      embed = discord.Embed(title=title, color=0xe77ed9)
      embed.add_field(name='執行中出現錯誤，錯誤訊息:', value=e)
      embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')
      
      log_write(e, "requests_waifu_data")
      alert_view = alert_barview()
      return embed, alert_view
      
  else:
    embed = discord.Embed(title=title, color=0xe77ed9)
    embed.add_field(name='執行中出現錯誤，錯誤訊息:', value=f"連線至 API 時出現錯誤，狀態碼:{r.status_code}")
    embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')

    alert_view = alert_barview()
    return embed, alert_view
    
class alert_barview(View):
  def load_alert(self, send_message, is_delete):
    self.send_message = send_message
    self.is_delete = is_delete
    
  async def load_embed_data(self, embed_message, author_id):
    self.load_alert(embed_message, True)
    
  @discord.ui.button(label='關閉', style=discord.ButtonStyle.gray)
  async def verify_no_button_callback(self, interaction, feed_button):
    await self.send_message.delete()
   
  async def on_timeout(self):
    if self.is_delete:
      await self.send_message.delete()
    else
      await self.send_message.edit(view=None)
    
class waifu_barview(View):
  with open('author_datafile/favorites_file.json','r',encoding="utf-8") as f:
    __FAVORITES_LIST = json.load(f)
    
  def load_embed_message(self, embed_message):
    self.embed_message = embed_message
  
  def get_favorites_list(self, user_id, classification: str):
    try:
      favorite_Class = self.__FAVORITES_LIST[str(user_id)][classification]
      return favorite_Class
    except:
      return None
    
  def update_favorites_list(self, user_id, classification: str, data):
    try:
      self.__FAVORITES_LIST[str(user_id)][classification].append(data)
    except:
      self.__FAVORITES_LIST[str(user_id)] = {"waifu":[],"nsfw":[]}
      self.__FAVORITES_LIST[str(user_id)][classification].append(data)
      
    with open('author_datafile/favorites_file.json','w',encoding="utf-8") as f:
      f.write(json.dumps(self.__FAVORITES_LIST))
      
  def remove_favorites_list(self, user_id, classification: str, index):
    remove_favorites = self.__FAVORITES_LIST[str(user_id)][classification][index]
    self.__FAVORITES_LIST[str(user_id)][classification].remove(remove_favorites)
    
    with open('author_datafile/favorites_file.json','w',encoding="utf-8") as f:
      f.write(json.dumps(self.__FAVORITES_LIST))
  
  async def on_timeout(self):
    try:
      await self.embed_message.edit(view=None)
    except:
      pass
      
class waifu_data_barview(waifu_barview):
  with open('author_datafile/count.json',encoding="utf-8") as f:
    __USER_COUNT = json.load(f)
  
  def __init__(self, waifu_url, waifu_source, is_nsfw, model):
    super().__init__()
    
    self.waifu_url = waifu_url
    self.waifu_source = waifu_source
    self.is_nsfw = is_nsfw
    self.model = model
    
  async def load_embed_data(self, embed_message, author_id):
    self.load_embed_message(embed_message)
    
    await self.__record_user_count(author_id)
    
  async def __record_user_count(self, author_id):
    try:
      self.__USER_COUNT[str(author_id)] = self.__USER_COUNT[str(author_id)]+1
    except:
      self.__USER_COUNT[str(author_id)] = 1
      
    with open('author_datafile/count.json','w',encoding="utf-8") as f:
      if self.__USER_COUNT[str(author_id)]%100 == 0:
        embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
        embed.add_field(name='嗚呼!:', value=f'<@{author_id}>恭喜，這是你第 {self.__USER_COUNT[str(author_id)]} 位老婆')
        embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
        
        await interaction.response.defer()
        await interaction.message.edit(view=None)
        
        alert_view = alert_barview()
        
        info_msg = await send_message.reply(embed=embed,view=alert_view)
        alert_view.load_alert(info_msg, False)
        
      f.write(json.dumps(self.__USER_COUNT))
          
  @discord.ui.button(label='加入最愛', style=discord.ButtonStyle.gray, emoji='📥')
  async def favorites_button_callback(self, interaction, feed_button):
    user_id = str(interaction.user.id)
      
    try:
      data = {'url':self.waifu_url,'source':self.waifu_source}
      
      if self.is_nsfw:
        classification = 'nsfw'
      else:
        classification = 'waifu'
        
      self.update_favorites_list(user_id, classification, data)

      await interaction.response.defer()

      info_msg = await interaction.channel.send('**添加成功!**')
      await asyncio.sleep(5)
      await info_msg.delete()
    except Exception as e:
      log_write(e, "waifu_barview 加入最愛")

      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='執行中出現錯誤，錯誤訊息:', value=e)
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
      
      await interaction.response.defer()
      await interaction.message.edit(view=None)
      
      alert_view = alert_barview()
      
      info_msg = await interaction.channel.reply(embed=embed,view=alert_view)
      alert_view.load_alert(info_msg, True)
    
  @discord.ui.button(label='更新卡片', style=discord.ButtonStyle.gray, emoji='🔄', custom_id = "randomnext_button")
  async def randomnext_button_callback(self, interaction, feed_button):
    try:
      search_button = [x for x in self.children if x.custom_id == "randomnext_button"][0]
      search_button.label = "更新中..."
      search_button.disabled = True
      await interaction.message.edit(view=self)
      await interaction.response.defer()
      
      embed, view = requests_waifu_data(self.is_nsfw, self.model)
    
      send_message = await interaction.message.reply(embed=embed,view=view)
      await view.load_embed_data(send_message, interaction.user.id)
      
      remove_button = [x for x in self.children if x.custom_id == "randomnext_button"][0]
      self.remove_item(remove_button)
      
      await interaction.message.edit(view=self)
    except Exception as e:
      log_write(e, "waifu_barview 更新卡片")

      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='執行中出現錯誤，錯誤訊息:', value=e)
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
      
      await interaction.response.defer()
      await interaction.message.edit(view=None)
      
      alert_view = alert_barview()
      
      info_msg = await interaction.message.reply(embed=embed,view=alert_view)
      alert_view.load_alert(info_msg, True)

  @discord.ui.button(label='搜尋類似圖片', style=discord.ButtonStyle.gray, emoji='🔎', custom_id = "search_button")
  async def search_button_callback(self, interaction, feed_button):
    embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
    embed.add_field(name='該功能須等版本更新', value='需更新: image_search')
    embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
    
    await interaction.response.defer()
    
    search_button = [x for x in self.children if x.custom_id == "search_button"][0]
    search_button.label = "需要版本更新"
    search_button.disabled = True
    await interaction.message.edit(view=self)
    
    alert_view = alert_barview()
    
    info_msg = await interaction.message.reply(embed=embed,view=alert_view)
    alert_view.load_alert(info_msg, True)
    
  @discord.ui.button(label="刪除卡片", style=discord.ButtonStyle.gray, emoji='❌')
  async def delete_button_callback(self, interaction, button):
    await interaction.message.delete()

class favorites_barview(waifu_barview):
  def __init__(self, user_id, classification: str):
    super().__init__()
    
    favorite_Class = self.get_favorites_list(user_id, classification)
    self.favorite_Class = favorite_Class
    self.classification = classification
    self.index = 0
    self.length = len(favorite_Class)
    self.user_id = user_id
    
    if classification == "nsfw":
      self.pre_title = f"🔞favorites waifu"
    else:
      self.pre_title = f"favorites waifu"
    
  def favorites_embed_build(self):
    if self.favorite_Class != None:
      img_url = self.favorite_Class[self.index]['url']
      source_url = self.favorite_Class[self.index]['source']

      page = '1/' + str(self.length)
      
      title = f"{self.pre_title}({page})"

      embed = discord.Embed(title=title, color=0xe77ed9)
      embed.add_field(name='source:', value=source_url)

      embed.set_image(url=img_url)
          
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
    
      return embed
    else:
      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='歐喔!', value='你還沒有任何收藏喔~')
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
    
      return embed

  @discord.ui.button(label='上一頁', style=discord.ButtonStyle.gray, emoji='🔙')
  async def uppage_button_callback(self, interaction, feed_button):
    if self.user_id == interaction.user.id:
      self.index = (self.index - 1) % self.length
      page = f'{self.index+1}/' + str(self.length)
      
      title = f"{self.pre_title}({page})"
      
      img_url = self.favorite_Class[self.index]['url']
      source_url = self.favorite_Class[self.index]['source']

      embed = discord.Embed(title=title, color=0xe77ed9)
      embed.add_field(name='source:', value=source_url)

      embed.set_image(url=img_url)
          
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

      await interaction.message.edit(embed=embed)
      await interaction.response.defer()
    else:
      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='歐喔!', value=f'<@{interaction.user.id}> 你沒有權限執行這項操作喔')
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
    
      alert_view = alert_barview()
      
      info_msg = await interaction.channel.reply(embed=embed,view=alert_view)
      alert_view.load_alert(info_msg, True)
      await interaction.response.defer()
    
  @discord.ui.button(label="下一頁", style=discord.ButtonStyle.gray, emoji='🔜')
  async def downpage_button_callback(self, interaction, button): 
    if self.user_id == interaction.user.id:
      self.index = (self.index + 1) % self.length
      page = f'{self.index+1}/' + str(self.length)
      
      title = f"{self.pre_title}({page})"
      
      img_url = self.favorite_Class[self.index]['url']
      source_url = self.favorite_Class[self.index]['source']

      embed = discord.Embed(title=title, color=0xe77ed9)
      embed.add_field(name='source:', value=source_url)

      embed.set_image(url=img_url)
          
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

      await interaction.message.edit(embed=embed)
      await interaction.response.defer()
    else:
      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='歐喔!', value=f'<@{interaction.user.id}> 你沒有權限執行這項操作喔')
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
    
      alert_view = alert_barview()
      
      info_msg = await interaction.channel.reply(embed=embed,view=alert_view)
      alert_view.load_alert(info_msg, True)
      await interaction.response.defer()

  @discord.ui.button(label="從最愛中移除", style=discord.ButtonStyle.gray, emoji='📤')
  async def delete_button_callback(self, interaction, button):
    if self.user_id == interaction.user.id:
      try:
        self.remove_favorites_list(self.user_id, self.classification, self.index)
        
        favorite_Class = self.get_favorites_list(self.user_id, self.classification)
        self.favorite_Class = favorite_Class
        self.length = len(favorite_Class)
        
        self.index = self.index % self.length
        page = f'{self.index+1}/' + str(self.length)
        
        title = f"{self.pre_title}({page})"
        
        img_url = self.favorite_Class[self.index]['url']
        source_url = self.favorite_Class[self.index]['source']

        embed = discord.Embed(title=title, color=0xe77ed9)
        embed.add_field(name='source:', value=source_url)

        embed.set_image(url=img_url)
            
        embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

        await interaction.response.defer()
        await interaction.message.edit(embed=embed)
      except Exception as e:
        log_write(e, "favorites_barview 從最愛中移除")

        embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
        embed.add_field(name='執行中出現錯誤，錯誤訊息:', value=e)
        embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
        
        await interaction.response.defer()
        await interaction.message.edit(view=None)
        
        alert_view = alert_barview()
        
        info_msg = await interaction.message.reply(embed=embed,view=alert_view)
        alert_view.load_alert(info_msg, True)
    else:
      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='歐喔!', value=f'<@{interaction.user.id}> 你沒有權限執行這項操作喔')
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
    
      alert_view = alert_barview()
      
      info_msg = await interaction.channel.reply(embed=embed,view=alert_view)
      alert_view.load_alert(info_msg, True)
      await interaction.response.defer()
  
  @discord.ui.button(label="關閉卡片", style=discord.ButtonStyle.gray, emoji='❌')
  async def close_button_callback(self, interaction, button):
    await interaction.message.delete()
  
class waifu(Cog_Extension):
  @app_commands.command(name="randomwaifu-store", description="看你的randomwaifu收藏的slash指令延伸")
  @app_commands.choices(mode = [
    Choice(name = "查看收藏(Non-NSFW)", value = 0),
    Choice(name = "查看收藏(NSFW)", value = 1)
  ])
  async def randomwaifu_slash_store(self, interaction: discord.Interaction, mode: int):
    if mode == 0:
      try:
        classification = "waifu"
        
        await interaction.response.defer(ephemeral=True)
        view = favorites_barview(interaction.user.id, classification)
        embed = view.favorites_embed_build()
    
        send_message = await interaction.user.send(embed=embed, view=view)
        view.load_embed_message(send_message)
        await interaction.followup.send('清單已私訊您!', ephemeral = True)
        
      except Exception as e:
        log_write(e, "randomwaifu_slash_store")

        embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
        embed.add_field(name='執行中出現錯誤，請回報給管理者或工程人員，錯誤訊息:', value=e)
        embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
        
        await interaction.followup.send(embed=embed, ephemeral = True)
        
    elif mode == 1:
      try:
        classification = "nsfw"
        
        await interaction.response.defer(ephemeral=True)
        view = favorites_barview(interaction.user.id, classification)
        embed = view.favorites_embed_build()
    
        send_message = await interaction.user.send(embed=embed, view=view)
        view.load_embed_message(send_message)
        await interaction.followup.send('清單已私訊您!', ephemeral = True)
        
      except Exception as e:
        log_write(e, "randomwaifu_slash_store")

        embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
        embed.add_field(name='執行中出現錯誤，請回報給管理者或工程人員，錯誤訊息:', value=e)
        embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
        
        await interaction.followup.send(embed=embed, ephemeral = True)
   
  @app_commands.command(name="randomwaifu", description="randomwaifu (Non-NSFW) 的slash指令延伸")
  @app_commands.choices(mode = WAIFU_TAGS_SAFE)
  async def randomwaifu_slash_safe(self, interaction: discord.Interaction, mode: int):
    try:
      id_tag = TAGS_LIST[mode]
      
      await interaction.response.defer(ephemeral=True)
      embed, view = requests_waifu_data(False, id_tag)
    
      send_message = await interaction.user.send(embed=embed, view=view)
      await view.load_embed_data(send_message, interaction.user.id)
      await interaction.followup.send('清單已私訊您!', ephemeral = True)
      
    except Exception as e:
      log_write(e, "randomwaifu_slash_safe")

      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='執行中出現錯誤，請回報給管理者或工程人員，錯誤訊息:', value=e)
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
      
      await interaction.followup.send(embed=embed, ephemeral = True)
   
  @app_commands.command(name="randomwaifu-nsfw", description="randomwaifu (NSFW) 的slash指令延伸")
  @app_commands.choices(mode = WAIFU_TAGS_NSFW)
  async def randomwaifu_slash_nsfw(self, interaction: discord.Interaction, mode: int):
    try:
      id_tag = TAGS_LIST[mode]
      
      await interaction.response.defer(ephemeral=True)
      embed, view = requests_waifu_data(True, id_tag)
    
      send_message = await interaction.user.send(embed=embed, view=view)
      await view.load_embed_data(send_message, interaction.user.id)
      await interaction.followup.send('清單已私訊您!', ephemeral = True)
    except Exception as e:
      log_write(e, "randomwaifu_slash_nsfw")

      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='執行中出現錯誤，請回報給管理者或工程人員，錯誤訊息:', value=e)
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
      
      await interaction.followup.send(embed=embed, ephemeral = True)
      
  @app_commands.command(name="randomwaifu-list", description="randomwaifu list 的slash指令延伸")
  @app_commands.choices(mode = [
    Choice(name = "查看類別清單(Non-NSFW)", value = 0),
    Choice(name = "查看類別清單(NSFW)", value = 1),
  ])
  async def randomwaifu_slash_list(self, interaction: discord.Interaction, mode: int):
    try:
      await interaction.response.defer()
      
      embed = discord.Embed(title="waifu_tag", color=0xffffff)
      embed.set_footer(text='此程式由 wannaZzz#8989 製作 | powerby:http://waifu.im', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

      if mode == 1:
        key_count = WAIFU_TAG['tags'] + WAIFU_TAG['nsfw']
      else:
        key_count = WAIFU_TAG['tags']

      for element in key_count:
        embed.add_field(name=element['name'],value=element['description'],inline=True)

      send_message = await interaction.followup.send(embed=embed, ephemeral = True)
      
    except Exception as e:
      log_write(e, "randomwaifu_slash_list")

      embed = discord.Embed(title="randomwaifu v5", color=0xe77ed9)
      embed.add_field(name='執行中出現錯誤，請回報給管理者或工程人員，錯誤訊息:', value=e)
      embed.set_footer(text='此程式由 wannaZzz#8989 製作', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")
      
      await interaction.followup.send(embed=embed, ephemeral = True)

      return
  
  @commands.command()
  async def randomwaifu(self, ctx, *uesr_command):
    with open('author_datafile/state.json',encoding="utf-8") as f:
      state = json.load(f)
      r_18_id = state['r_18_id']
    
    try:
      model = uesr_command[0]
    except:
      model = 'waifu'
      
    try:
      if uesr_command[1] == '-n':
        waifu_model = False
      else:
        raise
    except:
      waifu_model = True
      
    if model in WAIFU_TAG['tags_list'] or (model in WAIFU_TAG['nsfw_list'] and ctx.channel.id in r_18_id):
      nsfw_mode = ctx.channel.id in r_18_id and waifu_model
        
      await ctx.message.add_reaction("🔄")
      embed, view = requests_waifu_data(nsfw_mode, model)
          
      try:
        send_message = await ctx.reply(embed=embed,view=view)
        await view.load_embed_data(send_message, ctx.author.id)
        
        await ctx.message.add_reaction("✅")
      except Exception as e:
        log_write(e, "randomwaifu model")
        await ctx.message.add_reaction("❌")
        return
        
    elif model == 'favorites':
      try:
        try:
          if uesr_command[1] == '-n':
            classification = "waifu"
          else:
            raise
        except:
          if ctx.channel.id in r_18_id:
            classification = "nsfw"
          else:
            classification = "waifu"
      
        view = favorites_barview(interaction.user.id, classification)
        embed = view.favorites_embed_build()
      
        send_message = await ctx.reply(embed=embed,view=view)
        view.load_embed_message(send_message)
        
        await ctx.message.add_reaction("✅")
      except Exception as e:
        log_write(e, "randomwaifu favorites")
        await ctx.message.add_reaction("❌")
        return
     
    elif model == 'list':
      try:
        if uesr_command[1] == '-n':
          classification = "waifu"
        else:
          raise
      except:
        if ctx.channel.id in r_18_id:
          classification = "nsfw"
        else:
          classification = "waifu"
    
      embed = discord.Embed(title="waifu_tag", color=0xffffff)
      embed.set_footer(text='此程式由 wannaZzz#8989 製作 | powerby:http://waifu.im', icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

      if classification == "nsfw":
        key_count = WAIFU_TAG['tags'] + WAIFU_TAG['nsfw']
      else:
        key_count = WAIFU_TAG['tags']

      for element in key_count:
        embed.add_field(name=element['name'],value=element['description'],inline=True)
      
      alert_view = alert_barview()
      
      try:
        send_message = await ctx.reply(embed=embed, view=alert_view)
        alert_view.load_alert(send_message, True)
        
        await ctx.message.add_reaction("✅")
      except Exception as e:
        log_write(e, "randomwaifu list")
        await ctx.message.add_reaction("❌")
        return
      
    else:
      await ctx.reply(f'{model} 不是randomwaifu的參數或主題類別')
      await ctx.message.add_reaction("❌")

async def setup(bot):
  await bot.add_cog(waifu(bot))
