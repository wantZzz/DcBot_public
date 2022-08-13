import discord
import os, sys
import re
import json
from discord.ext import commands
from discord.ui import Button,View

import requests
from bs4 import BeautifulSoup
import random
import asyncio
from cog import Cog_Extension

sys.path.append(os.pardir)
show = 8#setting one page show how many theme(for display meme themes)

class list_view(View):
  def load_embed_message(self,embed_message):
    self.embed_message = embed_message
    
  @discord.ui.button(label='上一頁', style=discord.ButtonStyle.gray, emoji='🔙')#uppage
  async def uppage_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    pages = favorites_embed['title'][15:-1].split('/')

    pages[0] = int(pages[0])-1

    with open('users_datafile/meme_theme_list.json') as f:#open meme theme data
      meme_types = json.load(f)

    next_page = (pages[0] - 1) % int(pages[1])
    
    embed = discord.Embed(title=f"radomeme_list ({next_page+1}/{pages[1]})",color=0xffffff)
        
    embed.set_footer(text="powerby:https://memes.tw/",icon_url='https://memes.tw/ms-icon-310x310.png')

    limit = (next_page) * show
    meme_keys = list(meme_types.keys())
    for key in range(1, show + 1):
      if len(meme_types) < limit + key:
          break
      name = str(limit + key) + '. ' + meme_keys[limit + key - 1]
      meme_count = '共有 ' + meme_types[meme_keys[limit + key - 1]][1] + ' 張圖片'
      embed.add_field(name=name, value=meme_count, inline=True)

    await ctx.message.edit(embed=embed)
    await ctx.response.defer()

  @discord.ui.button(label="下一頁", style=discord.ButtonStyle.gray, emoji='🔜')#downpage
  async def downpage_button_callback(self,ctx,button): 
    favorites_embed = ctx.message.embeds[0].to_dict()#get page number form message
    pages = favorites_embed['title'][15:-1].split('/')

    pages[0] = int(pages[0])-1

    with open('users_datafile/meme_theme_list.json') as f:#open meme theme data
      meme_types = json.load(f)

    next_page = (pages[0] + 1) % int(pages[1])
    
    embed = discord.Embed(title=f"radomeme_list ({next_page+1}/{pages[1]})",color=0xffffff)
        
    embed.set_footer(text="powerby:https://memes.tw/",icon_url='https://memes.tw/ms-icon-310x310.png')

    limit = (next_page) * show
    meme_keys = list(meme_types.keys())
    for key in range(1, show + 1):
      if len(meme_types) < limit + key:
          break
      name = str(limit + key) + '. ' + meme_keys[limit + key - 1]
      meme_count = '共有 ' + meme_types[meme_keys[limit + key - 1]][1] + ' 張圖片'
      embed.add_field(name=name, value=meme_count, inline=True)

    await ctx.message.edit(embed=embed)
    await ctx.response.defer()
    
  async def on_timeout(self):
    await self.embed_message.delete()

class meme(Cog_Extension):
  @commands.command()
  async def randomeme(self, ctx, *uesr_command):
    url = 'https://memes.tw'

    with open('users_datafile/state.json') as f:
      state = json.load(f)
      
    r_18_id = state['r_18_id']

    elif uesr_command[0] == 'list':#check all meme theme
      with open('users_datafile/meme_theme_list.json') as f:#open meme theme data
        meme_types = json.load(f)

      try:
        page = 1
        max = len(meme_types) // show + 1

        if max < page or 0 >= page:
          await ctx.reply('頁數錯誤或頁數過大，最大:' + str(max))
          await ctx.message.add_reaction("❌")
          return

        embed = discord.Embed(title=f"radomeme_list ({page}/{max})",color=0xffffff)
        
        embed.set_footer(text="powerby:https://memes.tw/",icon_url='https://memes.tw/ms-icon-310x310.png')

        limit = (page - 1) * show
        meme_keys = list(meme_types.keys())
        for key in range(1, show + 1):
          if len(meme_types) < limit + key:
              break
          name = str(limit + key) + '. ' + meme_keys[limit + key - 1]
          meme_count = '共有 ' + meme_types[meme_keys[limit + key - 1]][1] + ' 張圖片'
          embed.add_field(name=name, value=meme_count, inline=True)
          

        view = list_view(timeout = 60.0)#timeout setting

        tmpmsg = await ctx.send(embed=embed, view=view)
        await ctx.message.add_reaction("✅")
        
        view.load_embed_message(tmpmsg)

      except:
        await ctx.message.add_reaction("❌")

    elif uesr_command[0] == 'meme':#output a meme suitable for the theme
      with open('users_datafile/meme_theme_list.json') as e:#open meme theme data
        meme_types = json.load(e)

      try:
        contest = int(uesr_command[1])
      except:
        await ctx.message.add_reaction("❌")
        return

      if contest > len(meme_types.keys()):
        await ctx.message.add_reaction("❌")
        return

      if contest in state['ban_meme_id'] and not ctx.channel.id in r_18_id:#avoid nsfw memes appere at Non-nsfw channel
        await ctx.message.add_reaction("❌")
        return
      
      try:      
        meme_keys = list(meme_types.keys())
  
        choise = meme_keys[contest - 1]
        list_type = meme_types[choise]
  
        radom_num = random.randint(1, int(list_type[1]))#pick a meme in random 
  
        page = radom_num // 20 + 1
        #print(radom_num)
        #print(page)
  
        r = requests.get(url + list_type[0] + '&page=' + str(page))#get page which that meme in 
  
        if r.status_code == requests.codes.ok:
          await ctx.message.add_reaction("🔄")
          soup = BeautifulSoup(r.text, 'html.parser')
          meme_type_list = soup.find_all('div',class_="sensitive-content")
          print(len(meme_type_list))
  
          try:
            i = meme_type_list[random.randint(0,len(meme_type_list) - 1)]
          except:#if that meme not found, select new meme in that theme first 3 page
            r = requests.get(url + list_type[0] + '&page=' + str(random.randint(1, 3)))
            
            if r.status_code == requests.codes.ok:
              soup = BeautifulSoup(r.text, 'html.parser')
              meme_type_list = soup.find_all('div', class_="sensitive-content")
              i = meme_type_list[random.randint(0,len(meme_type_list) - 1)]

          img_id = 'id=' + str(i.get('data-id'))#meme's id
          maker_url = 'https://memes.tw/wtf/' + i.get('data-id')#author
          img_url = i.find("img").get('data-src')#source
          images = requests.get(img_url)#get picture
          with open(f'{radom_num}.jpg', 'wb') as f:
            f.write(images.content)
          print(f'{radom_num}.jpg')
  
        else:
          await ctx.send("網路錯誤")
          await ctx.message.add_reaction("❌")
          return
  
        embed = discord.Embed(title=f"random meme({choise})",color=0xffffff)
        embed.add_field(name=f'source({img_id}):', value=maker_url)
      
        file = discord.File(f'{radom_num}.jpg', filename="image.png")
        embed.set_image(url="attachment://image.png")
  
        embed.set_footer(text="powerby:https://memes.tw/",icon_url='https://memes.tw/ms-icon-310x310.png')
      
        await ctx.send(file=file, embed=embed)
        os.remove(f'{radom_num}.jpg')
        await ctx.message.add_reaction("✅")

      except Exception as e:
        print(e)
        await ctx.reply('錯誤訊息:\n' + e)
        await ctx.message.add_reaction("❌")
        
    elif uesr_command[0] == 'wtf':#pick a meme with meme's id
      try:
        picture_id = int(uesr_command[1])
      except:
        await ctx.message.add_reaction("❌")
        return

      radom_num = picture_id 

      r = requests.get(url + '/wtf/' + str(picture_id ))#get meme's page
  
      if r.status_code == requests.codes.ok:
        await ctx.message.add_reaction("🔄")
        soup = BeautifulSoup(r.text, 'html.parser')
        i = soup.find('div',class_="sensitive-content")

        maker_url = 'https://memes.tw/wtf/' + i.get('data-id')#author
        img_title = i.find("a",class_="text-default").find('b').text#title
 
        img_url = i.find("img",class_="img-fluid").get('src')#source
        images = requests.get(img_url)#get picture
        with open(f'{radom_num}.jpg', 'wb') as f:
          f.write(images.content)
        print(f'{radom_num}.jpg')

        embed = discord.Embed(title=f"{img_title}",color=0xffffff)
        embed.add_field(name='source:', value=maker_url)
      
        file = discord.File(f'{radom_num}.jpg', filename="image.png")
        embed.set_image(url="attachment://image.png")

        embed.set_footer(text="powerby:https://memes.tw/",icon_url='https://memes.tw/ms-icon-310x310.png')
      
        await ctx.send(file=file, embed=embed)
        os.remove(f'{radom_num}.jpg')
        await ctx.message.add_reaction("✅")

      else:
        await ctx.send("網路錯誤")
        await ctx.message.add_reaction("❌")
        return

      except Exception as e:
        print(e)
        await ctx.reply('錯誤訊息:\n' + e)
        await ctx.message.add_reaction("❌")

    else:
      await ctx.message.add_reaction("❌")   

async def setup(bot):
  await bot.add_cog(meme(bot))
