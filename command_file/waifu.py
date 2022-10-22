import discord
import sys
import os
import json
import asyncio
from discord.ext import commands
from discord.ui import Button,View
from discord import app_commands
from discord.app_commands import Choice
import traceback

import time_myself

from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont

import requests
from cog import Cog_Extension

from command_file.picture_search import picture_search

sys.path.append(os.pardir)

with open('author_datafile/count.json',encoding="utf-8") as f:
    user_count = json.load(f)

class random_barview(View):

  def load_embed_message(self,embed_message):
    self.embed_message = embed_message
  
  @discord.ui.button(label='加入最愛', style=discord.ButtonStyle.gray, emoji='📥')
  async def favorites_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    user_id = str(ctx.user.id)
    waifu_url = favorites_embed['image']['url']
    waifu_source = favorites_embed['fields'][0]['value']
    is_nsfw = (favorites_embed['title'][0] == '🔞')

    with open('author_datafile/favorites_file.json','r',encoding="utf-8") as f:
      favorites = json.load(f)

    data = {'url':waifu_url,'source':waifu_source}

    if is_nsfw:
      Classification = 'nsfw'
    else:
      Classification = 'waifu'


    try:
      favorites[user_id][Classification].append(data)
    except:
      favorites[user_id] = {"waifu":[],"nsfw":[]}
      favorites[user_id][Classification].append(data)

    with open('author_datafile/favorites_file.json','w',encoding="utf-8") as f:
      f.write(json.dumps(favorites))

    await ctx.response.defer()

    info_msg = await ctx.channel.send('**添加成功!**')
    await asyncio.sleep(5)
    await info_msg.delete()

  @discord.ui.button(label='更新卡片', style=discord.ButtonStyle.gray, emoji='🔄', custom_id = "randomnext_button")
  async def randomnext_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    if favorites_embed['title'].startswith('🔞'):
      Classification = "nsfw"
    else:
      Classification = "waifu"

    model = favorites_embed['title'].split('(')[1][:-1]

    #print(model)

    if Classification == "nsfw":
      url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=true"
    else:
      url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=false"

    r = requests.get(url)
  
    if r.status_code == requests.codes.ok:
      try:
        # 以 BeautifulSoup 解析 HTML 程式碼
        img_url = r.json()['images'][0]['url']
  
        source_url = r.json()['images'][0]['source']

        is_nsfw = r.json()['images'][0]['is_nsfw']

        if is_nsfw:
          title = f"🔞random waifu({model})"
        else:
          title = f"random waifu({model})"
  
        embed = discord.Embed(title=title, color=0xe77ed9)
        embed.add_field(name='source:', value=source_url)
  
        embed.set_image(url=img_url)
          
        embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')
        
        view = random_barview()
        
        send_message = await ctx.channel.send(embed=embed,view=view)
        view.load_embed_message(send_message)

        with open('author_datafile/count.json',encoding="utf-8") as f:
          user_count_reload = json.load(f)

        try:
          user_count_reload[str(ctx.user.id)] = user_count_reload[str(ctx.user.id)]+1
        except:
          user_count_reload[str(ctx.user.id)] = 1
        with open('author_datafile/count.json','w',encoding="utf-8") as f:
          #print(user_count_reload)
          if user_count_reload[str(ctx.user.id)]%100 == 0:
            await send_message.reply(f'<@{ctx.user.id}>恭喜，這是你第 {user_count_reload[str(ctx.user.id)]} 位老婆')
          f.write(json.dumps(user_count_reload))

        remove_button = [x for x in self.children if x.custom_id == "randomnext_button"][0]
        
        self.remove_item(remove_button)
        await ctx.message.edit(view=self)

        await ctx.response.defer()
        
      except Exception as e:
        print(e)
        await ctx.response.defer()
        await ctx.message.edit(view=None)
        info_msg = await ctx.channel.send('**更新失敗**')
        await asyncio.sleep(5)
        await info_msg.delete()
        
    else:
      await ctx.response.defer()
      info_msg = await ctx.channel.send('**連線至資料庫失敗**')
      await asyncio.sleep(5)
      await info_msg.delete()
        
  @discord.ui.button(label='搜尋類似圖片', style=discord.ButtonStyle.gray, emoji='🔎', custom_id = "search_button")
  async def search_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    file_path = favorites_embed['image']['url']
    
    search_button = [x for x in self.children if x.custom_id == "search_button"][0]
    search_button.label = "處理中"
    search_button.disabled = True
    await ctx.message.edit(view=self)
    await ctx.response.defer()
    
    def circle_corner(img, radii):  #把原图片变成圆角，这个函数是从网上找的，原址 https://www.pyget.cn/p/185266
      """
      圆角处理
      :param img: 源图象。
      :param radii: 半径，如：30。
      :return: 返回一个圆角处理后的图象。
      """
    
      # 画圆（用于分离4个角）
      circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
      draw = ImageDraw.Draw(circle)
      draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
    
      # 原图
      img = img.convert("RGBA")
      w, h = img.size
    
      # 画4个角（将整圆分离为4个部分）
      alpha = Image.new('L', img.size, 255)
      alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
      alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
      alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
      alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
      # alpha.show()
    
      img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
      return img
      
    search_url = 'https://yandex.ru/images/search'
    
    file_tag = file_path.split('.')[-1]
    
    picture_get = requests.get(file_path)
    with open(f"picture/yandex/imagesearch.{file_tag}","wb") as f:
      f.write(picture_get.content)
    
    files = {'upfile': ('blob', open(f"picture/yandex/imagesearch.{file_tag}", 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(search_url, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = search_url + '?' + query_string
    #print(img_search_url)
    
    consquense_path = requests.get(img_search_url)

    if consquense_path.status_code == requests.codes.ok:
      await ctx.message.add_reaction("🔄")
      soup = BeautifulSoup(consquense_path.content, 'html.parser')

      embed = discord.Embed(title="yandex.com圖搜結果",color=0xfc0)
      embed.set_author(name="Yandex.Images")
      embed.set_thumbnail(url=file_path)
      embed.add_field(name='圖搜詳細資訊:', value=f"[Images search info]({img_search_url})", inline=False)
      
      data = soup.find('div',class_='cbir-section cbir-section_name_similar').find('div',class_='Root').get('data-state')
      k = json.loads(data)
      data_list = k['thumbs']

      try:
        data = soup.find('div',class_='cbir-section cbir-section_name_other-sizes').find('div',class_='Root').get('data-state')
        k = json.loads(data)
        dups_list = k['items']

        str_image_dups = ""
        for image_dups in dups_list['large_dups']:
          large_str = f"{image_dups['text']}: \n[click link!]({image_dups['url']})\n"
          if len(str_image_dups) + len(large_str) >= 1024:
            break
          str_image_dups += large_str
          
        if not str_image_dups == "":
          embed.add_field(name='large size:', value=str_image_dups, inline=True)

        str_medium_dups = ""
        for medium_dups in dups_list['medium_dups']:
          medium_str = f"{medium_dups['text']}: \n[click link!]({medium_dups['url']})\n"
          if len(str_medium_dups) + len(medium_str) >= 1024:
            break
          str_medium_dups += medium_str
          
        if not str_medium_dups == "":
          embed.add_field(name='medium size:', value=str_medium_dups, inline=True)

        str_small_dups = ""
        for small_dups in dups_list['small_dups']:
          small_str = f"{small_dups['text']}: \n[click link!]({small_dups['url']})\n"
          if len(str_small_dups) + len(small_str) >= 1024:
            break
          str_small_dups += small_str

        if not str_small_dups == "":
          embed.add_field(name='small size:', value=str_small_dups, inline=True)
      except:
        pass

      unready_msg = embed

      unready_msg.add_field(name='可能相似的圖片:', value=f"\u200B", inline=False)
        
      file = discord.File(f'picture/plese_await.png', filename="image.png")
      unready_msg.set_image(url="attachment://image.png")

      unready_msg = await ctx.message.reply(embed=unready_msg,file=file)
      
      image_list = []
      count = 0
      
      for image_json in data_list:
        imageUrl = image_json['imageUrl']
        height = image_json['height']
        width = image_json['width']
        image = requests.get(f"{'https:'+imageUrl}")
      
        if image.status_code == requests.codes.ok:
          with open(f"picture/yandex/picture/yandex{count}.png",'wb') as f:
            f.write(image.content)
      
          image_list.append({"height": height,"width": width,"path": f"picture/yandex/picture/yandex{count}.png"})
          count += 1
          
        else:
          pass

        await asyncio.sleep(0.2)
          
        #print(f"height: {height}\nwidth: {width}\n{'https:'+imageUrl}\n\n{'https://yandex.ru'+linkUrl}\n")
        
      sum_height = 0
      for image_json in image_list:
        sum_height += image_json['height']
      
      Specification_height = round(sum_height/len(image_list)*0.5)
      
      sum_width = 0 + len(image_list)*4 + 16
      for image_json in image_list:
        sum_width += image_json['width']*(Specification_height/image_json['height'])
      
      background_width = round(sum_width/4)
        
      background_image = Image.new('RGB',(background_width+8,(Specification_height*4)+20),(255,255,255))
      
      nowwidth_point = 4
      line = 0
      
      for image_k in image_list:
        image_paste = Image.open(image_k['path'])
        #print(int(image_k['width']*(Specification_height/image_k['height'])))
        #print(Specification_height)
        image_paste = image_paste.resize((int(image_k['width']*(Specification_height/image_k['height'])),Specification_height),Image.NEAREST)

        image_paste = circle_corner(image_paste, radii=10)
      
        if nowwidth_point + int(image_k['width']*(Specification_height/image_k['height'])) > background_width:
          nowwidth_point = 4
          line += 1
      
          if line > 4:
            break
          
        background_image.paste(image_paste,(nowwidth_point,line*(Specification_height+4)+4),image_paste)
      
        nowwidth_point += int(image_k['width']*(Specification_height/image_k['height'])) + 4
        #await asyncio.sleep(0.2)
      
      background_image.save(f'picture/yandex/output.png')

      #embed.add_field(name='可能相似的圖片:', value=f"\u200B", inline=False)
        
      file = discord.File(f'picture/yandex/output.png', filename="image.png")
      embed.set_image(url="attachment://image.png")

      await unready_msg.delete()

      await ctx.message.reply(embed=embed,file=file)
        
      search_button.label = "處理完成"
      await ctx.message.edit(view=self)

    else:
      await ctx.message.add_reaction("❌")  

  @discord.ui.button(label="刪除卡片", style=discord.ButtonStyle.gray, emoji='❌')
  async def delete_button_callback(self,ctx,button):
    await ctx.message.delete()

  async def on_timeout(self):
    await self.embed_message.edit(view=None)

class favorites_barview(View):
  @discord.ui.button(label='上一頁', style=discord.ButtonStyle.gray, emoji='🔙')
  async def uppage_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    user_id = str(ctx.user.id)
    page = favorites_embed['title'][17:-1].split('/')

    with open('author_datafile/favorites_file.json','r',encoding="utf-8") as f:
      favorites_list = json.load(f)

    if favorites_embed['title'].startswith('🔞'):
      Classification = "nsfw"
    else:
      Classification = "waifu"

    page[0] = int(page[0]) - 1

    next_page = (page[0] - 1) % len(favorites_list[str(user_id)][Classification])
    
    favorites = favorites_list[str(user_id)][Classification][next_page]

    img_url = favorites['url']
  
    source_url = favorites['source']

    page = f'{next_page+1}/' + str(len(favorites_list[str(user_id)][Classification]))

    if favorites_embed['title'].startswith('🔞'):
      title = f"🔞favorites waifu({page})"
    else:
      title = f"✅favorites waifu({page})"
  
    embed = discord.Embed(title=title, color=0xe77ed9)
    embed.add_field(name='source:', value=source_url)
  
    embed.set_image(url=img_url)
          
    embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')
  
    await ctx.message.edit(embed=embed)
    await ctx.response.defer()
      
  @discord.ui.button(label="下一頁", style=discord.ButtonStyle.gray, emoji='🔜')
  async def downpage_button_callback(self,ctx,button): 
    favorites_embed = ctx.message.embeds[0].to_dict()
    user_id = str(ctx.user.id)
    page = favorites_embed['title'][17:-1].split('/')

    with open('author_datafile/favorites_file.json','r',encoding="utf-8") as f:
      favorites_list = json.load(f)

    if favorites_embed['title'].startswith('🔞'):
      Classification = "nsfw"
    else:
      Classification = "waifu"

    page[0] = int(page[0]) - 1

    next_page = (page[0] + 1) % len(favorites_list[str(user_id)][Classification])
    
    favorites = favorites_list[str(user_id)][Classification][next_page]

    img_url = favorites['url']
  
    source_url = favorites['source']

    page = f'{next_page+1}/' + str(len(favorites_list[str(user_id)][Classification]))

    if favorites_embed['title'].startswith('🔞'):
      title = f"🔞favorites waifu({page})"
    else:
      title = f"✅favorites waifu({page})"
  
    embed = discord.Embed(title=title, color=0xe77ed9)
    embed.add_field(name='source:', value=source_url)
  
    embed.set_image(url=img_url)
          
    embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')
  
    await ctx.message.edit(embed=embed)
    await ctx.response.defer()

  @discord.ui.button(label="從最愛中移除", style=discord.ButtonStyle.gray, emoji='📤')
  async def delete_button_callback(self,ctx,button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    user_id = str(ctx.user.id)
    page = favorites_embed['title'][17:-1].split('/')

    with open('author_datafile/favorites_file.json','r',encoding="utf-8") as f:
      favorites_list = json.load(f)

    if favorites_embed['title'][0].startswith('🔞'):
      Classification = "nsfw"
    else:
      Classification = "waifu"

    page[0] = int(page[0]) - 1

    remove_favorites = favorites_list[str(user_id)][Classification][page[0]]
    favorites_list[user_id][Classification].remove(remove_favorites)

    with open('author_datafile/favorites_file.json','w',encoding="utf-8") as f:
      f.write(json.dumps(favorites_list))

    next_page = (page[0]) % len(favorites_list[str(user_id)][Classification])
    
    favorites = favorites_list[str(user_id)][Classification][next_page]

    img_url = favorites['url']
  
    source_url = favorites['source']

    page = f'{next_page+1}/' + str(len(favorites_list[str(user_id)][Classification]))

    if favorites_embed['title'].startswith('🔞'):
      title = f"🔞favorites waifu({page})"
    else:
      title = f"✅favorites waifu({page})"
  
    embed = discord.Embed(title=title, color=0xe77ed9)
    embed.add_field(name='source:', value=source_url)
  
    embed.set_image(url=img_url)
    embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')
  
    await ctx.message.edit(embed=embed)

    info_msg = await ctx.channel.send('**刪除成功!**')
    await asyncio.sleep(5)
    await info_msg.delete()
    await ctx.response.defer()

  @discord.ui.button(label="關閉卡片", style=discord.ButtonStyle.gray, emoji='❌')
  async def close_button_callback(self,ctx,button):
    await ctx.message.delete()

class waifu(Cog_Extension):
  @app_commands.command(name="randomwaifu", description="randomwaifu的slash指令延伸")
  @app_commands.choices(mode = [
    Choice(name = "查看收藏(Non-NSFW)", value = 0),
    Choice(name = "查看收藏(NSFW)", value = 1),
    Choice(name = "輸出收藏(add_NSFW)", value = 2)
  ])
  async def randomwaifu_slash(self, interaction: discord.Interaction, mode: int):
    with open('author_datafile/favorites_file.json','r',encoding="utf-8") as f:
      favorites_list = json.load(f)
      
    if mode <= 1:
      index = 0
      
      if mode == 1:
        Classification = "nsfw"
      else:
        Classification = "waifu"
      
      try:
        favorite_Class = favorites_list[str(interaction.user.id)][Classification]
        favorites = favorite_Class[index]
      except:
        await interaction.response.send_message('你還沒有任何收藏喔!', ephemeral = True)
        return

      def embed_build(favorites):
        img_url = favorites['url']
    
        source_url = favorites['source']
  
        page = '1/' + str(len(favorite_Class))
  
        if Classification == "nsfw":
          title = f"🔞favorites waifu({page})"
        else:
          title = f"✅favorites waifu({page})"
    
        embed = discord.Embed(title=title, color=0xe77ed9)
        embed.add_field(name='source:', value=source_url)
    
        embed.set_image(url=img_url)
            
        embed.set_footer(text='此程式由 wannaZzz#8989 製作 | powerby:http://waifu.im',icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

        return embed

      embed = embed_build(favorites)

      view = favorites_barview()

      """upp = Button(label='上一頁', style=discord.ButtonStyle.gray, emoji='🔙')
      dop = Button(label="下一頁", style=discord.ButtonStyle.gray, emoji='🔜')
      ref = Button(label="從最愛中移除", style=discord.ButtonStyle.gray, emoji='📤')
      clo = Button(label="關閉卡片", style=discord.ButtonStyle.gray, emoji='❌')
      slash_def = Slash_def(favorite_Class, favorites_list, Classification, str(interaction.user.id))
      upp.callback = slash_def.upp_callback
      dop.callback = slash_def.dop_callback
      clo.callback = slash_def.clo_callback
      ref.callback = slash_def.ref_callback"""
      
        
      try:
        send_message = await interaction.user.send(embed=embed, view=view)
        await interaction.response.send_message('清單已私訊您!', ephemeral = True)
        
      except Exception as e:
        print(e)
        await interaction.response.send_message('程式發生故障，請回報給管理者或工程人員', ephemeral = True)
        return

      await view.wait()
      try:
        await send_message.edit(view=None)
      except:
        pass

    if mode == 2:
      try:
        favorites = favorites_list[str(interaction.user.id)]
        file_info = ''

        file_info += 'waifu (Non-NSFW):\n'
        for i in favorites['waifu']:
          file_info += f'{i["url"]} {i["source"]}\n'

        file_info += 'waifu (NSFW):\n'
        for i in favorites['nsfw']:
          file_info += f'{i["url"]} {i["source"]}\n'
          
        with open(f'author_datafile/{interaction.user.id}.txt', 'w+') as f:
          f.write(file_info)

        try:
          await interaction.response.send_message(file=discord.File(f'author_datafile/{interaction.user.id}.txt'), ephemeral = True)
          await asyncio.sleep(5)
        except:
          await interaction.response.send_message('輸出失敗，請回報給管理者或工程人員', ephemeral = True)
          
        try:
          os.remove(f'author_datafile/{interaction.user.id}.txt')
        except:
          pass
      except:
        await interaction.response.send_message('你還沒有任何收藏喔!', ephemeral = True)
        return
    
  @commands.command()
  async def randomwaifu(self, ctx, *uesr_command):
    #r_18_id = [866270297052151859,901476467660185672]
    with open('author_datafile/state.json',encoding="utf-8") as f:
      state = json.load(f)
      r_18_id = state['r_18_id']

    try:
      model = uesr_command[0]
    except:
      model = 'waifu'

    with open('author_datafile/waifu_tag.json',encoding="utf-8") as e:
      waifu_tag = json.load(e)

    try:
      if uesr_command[1] == '-n':
        waifu_model = False
      else:
        raise
    except:
      waifu_model = True
      
    if model in waifu_tag['tags_list'] or (model in waifu_tag['nsfw_list'] and ctx.channel.id in r_18_id):
      if ctx.channel.id in r_18_id and waifu_model:
        url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=true"
      else:
        url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=false"
      #'http://api.waifu.im/sfw/waifu/'
        
      r = requests.get(url)
  
      if r.status_code == requests.codes.ok:
        try:
          await ctx.message.add_reaction("🔄")
          # 以 BeautifulSoup 解析 HTML 程式碼
          img_url = r.json()['images'][0]['url']
  
          source_url = r.json()['images'][0]['source']

          is_nsfw = r.json()['images'][0]['is_nsfw']

          if is_nsfw:
            title = f"🔞random waifu({model})"
          else:
            title = f"random waifu({model})"
  
          embed = discord.Embed(title=title, color=0xe77ed9)
          embed.add_field(name='source:', value=source_url)
  
          embed.set_image(url=img_url)
          
          embed.set_footer(text='powerby:http://waifu.im',icon_url='https://waifu.im/favicon.ico')

          view = random_barview()
  
          try:
            send_message = await ctx.send(embed=embed,view=view)
            view.load_embed_message(send_message)
            
            await ctx.message.add_reaction("✅")
          except Exception as e:
            print(e)
            await ctx.message.add_reaction("❌")
            return
  
          try:
            user_count[str(ctx.author.id)] = user_count[str(ctx.author.id)]+1
          except:
            user_count[str(ctx.author.id)] = 1
          with open('author_datafile/count.json','w',encoding="utf-8") as f:
            #print(user_count)
            if user_count[str(ctx.author.id)]%100 == 0:
              await send_message.reply(f'<@{ctx.author.id}>恭喜，這是你第 {user_count[str(ctx.author.id)]} 位老婆')
            f.write(json.dumps(user_count))

          """await view.wait()
          try:
            await send_message.edit(view=None)
          except:
            pass"""
  
        except Exception as e:
          print(e)
          await ctx.reply('錯誤訊息:\n' + e)
          await ctx.message.add_reaction("❌")
          
      else:
        await ctx.message.add_reaction("❌")

    elif model == 'list':
      try:
        embed = discord.Embed(title="waifu_tag (15秒後刪除)", color=0xffffff)

        embed.set_footer(text='此程式由 wannaZzz#8989 製作 | powerby:http://waifu.im',icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

        if ctx.channel.id in r_18_id:
          key_count = waifu_tag['tags'] + waifu_tag['nsfw']
        else:
          key_count = waifu_tag['tags']

        for element in key_count:
          embed.add_field(name=element['name'],value=element['description'],inline=True)

        tmpmsg = await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")
        await asyncio.sleep(15)
        await tmpmsg.delete()
        return

      except Exception as e:
        print(e)
        await ctx.message.add_reaction("❌")

    elif model == 'favorites':

      with open('author_datafile/favorites_file.json','r',encoding="utf-8") as f:
        favorites_list = json.load(f)

      try:
        if uesr_command[1] == '-n':
          favorites_model = False
        else:
          raise
      except:
        favorites_model = True

      if ctx.channel.id in r_18_id and favorites_model:
        Classification = "nsfw"
      else:
        Classification = "waifu"

      try:
        favorites = favorites_list[str(ctx.author.id)][Classification][0]
      except:
        await ctx.reply('你還沒有任何收藏喔!')
        await ctx.message.add_reaction("❌")
        return
      
      img_url = favorites['url']
  
      source_url = favorites['source']

      page = '1/' + str(len(favorites_list[str(ctx.author.id)][Classification]))

      if ctx.channel.id in r_18_id and favorites_model:
        title = f"🔞favorites waifu({page})"
      else:
        title = f"✅favorites waifu({page})"
  
      embed = discord.Embed(title=title, color=0xe77ed9)
      embed.add_field(name='source:', value=source_url)
  
      embed.set_image(url=img_url)
          
      embed.set_footer(text='此程式由 wannaZzz#8989 製作 | powerby:http://waifu.im',icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

      view = favorites_barview()
  
      try:
        send_message = await ctx.send(embed=embed,view=view)
        await ctx.message.add_reaction("✅")
      except Exception as e:
        print(e)
        await ctx.message.add_reaction("❌")
        return

      await view.wait()
      try:
        await send_message.delete()
      except:
        pass
        
    else:
      await ctx.reply(f'{model} 不是randomwaifu的參數或主題類別')
      await ctx.message.add_reaction("❌")
      
async def setup(bot):
  await bot.add_cog(waifu(bot))