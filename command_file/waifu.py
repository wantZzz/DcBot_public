"""
power by:https://waifu.im/

This command were used waifu.im api to made, all code was write by myself.
If want to used more powerfull and completeable, please use waifu.im official bot.
"""

import discord
import os, sys
import json
import asyncio
from discord.ext import commands
from discord.ui import Button,View
from discord import app_commands

import time_myself

import requests
from cog import Cog_Extension

sys.path.append(os.pardir)

class random_barview(View):
  def load_embed_message(self,embed_message):
    self.embed_message = embed_message
  
  @discord.ui.button(label='加入最愛', style=discord.ButtonStyle.gray, emoji='📥')#add picture in user favorites
  async def favorites_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    user_id = str(ctx.user.id)
    waifu_url = favorites_embed['image']['url']
    waifu_source = favorites_embed['fields'][0]['value']
    is_nsfw = (favorites_embed['title'][0] == '🔞')

    with open('users_datafile/favorites_file.json','r') as f:#open user favorites data
      favorites = json.load(f)

    data = {'url':waifu_url,'source':waifu_source}

    if is_nsfw:#picture classification
      Classification = 'nsfw'
    else:
      Classification = 'waifu'


    try:#if user already have favorites data, just append into it. otherwise build new key to save it.
      favorites[user_id][Classification].append(data)
    except:
      favorites[user_id] = {"waifu":[],"nsfw":[]}
      favorites[user_id][Classification].append(data)

    with open('users_datafile/favorites_file.json','w') as f:
      f.write(json.dumps(favorites))

    await ctx.response.defer()

    info_msg = await ctx.channel.send('**添加成功!**')
    await asyncio.sleep(5)
    await info_msg.delete()

  @discord.ui.button(label='更新卡片', style=discord.ButtonStyle.gray, emoji='🔄', custom_id = "randomnext_button")#refresh picture (send new message)
  async def randomnext_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()
    
    if favorites_embed['title'].startswith('🔞'):#picture classification check
      Classification = "nsfw"
    else:
      Classification = "waifu"

    model = favorites_embed['title'].split('(')[1][:-1]

    #print(model)

    if Classification == "nsfw":#quest picture from api
      url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=true"
    else:
      url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=false"

    r = requests.get(url)
  
    if r.status_code == requests.codes.ok:
      try:
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

        with open('users_datafile/count.json') as f:#user usage count
          user_count_reload = json.load(f)

        try:
          user_count_reload[str(ctx.user.id)] = user_count_reload[str(ctx.user.id)]+1
        except:
          user_count_reload[str(ctx.user.id)] = 1
        with open('users_datafile/count.json','w') as f:
          #print(user_count_reload)
          if user_count_reload[str(ctx.user.id)]%100 == 0:
            await send_message.reply(f'<@{ctx.user.id}>恭喜，這是你第 {user_count_reload[str(ctx.user.id)]} 位老婆')
          f.write(json.dumps(user_count_reload))

        remove_button = [x for x in self.children if x.custom_id == "randomnext_button"][0]#remove refresh button
        
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
      
  @discord.ui.button(label="刪除卡片", style=discord.ButtonStyle.gray, emoji='❌')#delete picture (delete this message)
  async def delete_button_callback(self,ctx,button):
    await ctx.message.delete()

  async def on_timeout(self):
    await self.embed_message.edit(view=None)

class favorites_barview(View):
  @discord.ui.button(label='上一頁', style=discord.ButtonStyle.gray, emoji='🔙')#uppage
  async def uppage_button_callback(self,ctx,feed_button):
    favorites_embed = ctx.message.embeds[0].to_dict()#get page number form message
    user_id = str(ctx.user.id)
    page = favorites_embed['title'][17:-1].split('/')

    with open('users_datafile/favorites_file.json','r') as f:#open user favorites data
      favorites_list = json.load(f)

    if favorites_embed['title'].startswith('🔞'):#check picture classification
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
      
  @discord.ui.button(label="下一頁", style=discord.ButtonStyle.gray, emoji='🔜')#downpage
  async def downpage_button_callback(self,ctx,button): 
    favorites_embed = ctx.message.embeds[0].to_dict()#get page number form message
    user_id = str(ctx.user.id)
    page = favorites_embed['title'][17:-1].split('/')

    with open('users_datafile/favorites_file.json','r') as f:#open user favorites data
      favorites_list = json.load(f)

    if favorites_embed['title'].startswith('🔞'):#check picture classification
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

  @discord.ui.button(label="從最愛中移除", style=discord.ButtonStyle.gray, emoji='📤')#remove picture form user favorites
  async def delete_button_callback(self,ctx,button):
    favorites_embed = ctx.message.embeds[0].to_dict()#get page number form message
    user_id = str(ctx.user.id)
    page = favorites_embed['title'][17:-1].split('/')

    with open('users_datafile/favorites_file.json','r') as f:#open user favorites data
      favorites_list = json.load(f)

    if favorites_embed['title'][0].startswith('🔞'):#check picture classification
      Classification = "nsfw"
    else:
      Classification = "waifu"

    page[0] = int(page[0]) - 1

    remove_favorites = favorites_list[str(user_id)][Classification][page[0]]#remove
    favorites_list[user_id][Classification].remove(remove_favorites)

    with open('users_datafile/favorites_file.json','w') as f:
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
  @app_commands.command(name="randomwaifu", description="randomwaifu的slash指令延伸")#slash command for check favorite in private or output favorite list to .txt file
  @app_commands.choices(mode = [
    Choice(name = "查看收藏(Non-NSFW)", value = 0),#slash command for check favorite in private(Non-NSFW)
    Choice(name = "查看收藏(NSFW)", value = 1),#slash command for check favorite in private(NSFW)
    Choice(name = "輸出收藏(add_NSFW)", value = 2)#output favorite list to .txt file
  ])
  async def randomwaifu_slash(self, interaction: discord.Interaction, mode: int):
    with open('users_datafile/favorites_file.json','r') as f:
      favorites_list = json.load(f)
      
    if mode <= 1:#check favorite
      index = 0
      
      if mode == 1:#check picture classification
        Classification = "nsfw"
      else:
        Classification = "waifu"
      
      try:#check isn't user have data of his's (her's) favorite
        favorite_Class = favorites_list[str(interaction.user.id)][Classification]
        favorites = favorite_Class[index]
      except:
        await interaction.response.send_message('你還沒有任何收藏喔!', ephemeral = True)
        return

      def embed_build(favorites):#build embed
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

    if mode == 2:#output favorite list
      try:
        favorites = favorites_list[str(interaction.user.id)]#check isn't user have data of his's (her's) favorite. if haven't, raise error (jump to except)
        file_info = ''

        file_info += 'waifu (Non-NSFW):\n'
        for i in favorites['waifu']:
          file_info += f'{i["url"]} {i["source"]}\n'

        file_info += 'waifu (NSFW):\n'
        for i in favorites['nsfw']:
          file_info += f'{i["url"]} {i["source"]}\n'
          
        with open(f'users_datafile/{interaction.user.id}.txt', 'w+') as f:#output favorite list to .txt file in temporary
          f.write(file_info)

        try:
          await interaction.response.send_message(file=discord.File(f'users_datafile/{interaction.user.id}.txt'), ephemeral = True)
          await asyncio.sleep(5)
        except:
          await interaction.response.send_message('輸出失敗，請回報給管理者或工程人員', ephemeral = True)
          
        try:
          os.remove(f'users_datafile/{interaction.user.id}.txt')#delete temporary file
        except:
          pass
      except:
        await interaction.response.send_message('你還沒有任何收藏喔!', ephemeral = True)
        return
    
  @commands.command()
  async def randomwaifu(self, ctx, *uesr_command):
    with open('users_datafile/state.json') as e:#control data
      state = json.load(e)

    try:#get user theme choices
      model = uesr_command[0]
    except:
      model = 'waifu'

    with open('users_datafile/waifu_tag.json') as e:#theme list
      waifu_tag = json.load(e)

    try:
      if uesr_command[1] == '-n':#check user classification choices, waifu_model is True means "Non-nsfw mode"
        waifu_model = False
      else:
        raise
    except:
      waifu_model = True
      
    if model in waifu_tag['tags_list'] or (model in waifu_tag['nsfw_list'] and ctx.channel.id in state['r_18_id']):#if model value is in themes list and check command isn't it enter in nsfw channel
      if ctx.channel.id in state['r_18_id'] and waifu_model:
        url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=true"
      else:
        url = f"https://api.waifu.im/random/?selected_tags={model}&is_nsfw=false"
      #'http://api.waifu.im/sfw/waifu/'
        
      r = requests.get(url)
  
      if r.status_code == requests.codes.ok:
        try:
          await ctx.message.add_reaction("🔄")

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
            
          with open('users_datafile/count.json') as f:#user usage count
            user_count = json.load(f)
  
          try:
            user_count[str(ctx.author.id)] = user_count[str(ctx.author.id)]+1
          except:
            user_count[str(ctx.author.id)] = 1
            
          with open('author_datafile/count.json','w') as f:
            #print(user_count)
            if user_count[str(ctx.author.id)]%100 == 0:
              await send_message.reply(f'<@{ctx.author.id}>恭喜，這是你第 {user_count[str(ctx.author.id)]} 位老婆')
            f.write(json.dumps(user_count))
  
        except Exception as e:
          print(e)
          await ctx.reply('錯誤訊息:\n' + e)
          await ctx.message.add_reaction("❌")
          
      else:
        await ctx.message.add_reaction("❌")

    elif model == 'list':#model value is "list"(check theme list)
      try:
        embed = discord.Embed(title="waifu_tag (15秒後刪除)", color=0xffffff)

        embed.set_footer(text='此程式由 wannaZzz#8989 製作 | powerby:http://waifu.im',icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")#'https://waifu.im/favicon.ico'

        if ctx.channel.id in state['r_18_id']:#check command isn't it enter in nsfw channel
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

    elif model == 'favorites':#check user favorite list public

      with open('author_datafile/favorites_file.json','r') as f:
        favorites_list = json.load(f)

      try:
        if uesr_command[1] == '-n':#check user classification choices, waifu_model is True means "Non-nsfw mode"
          favorites_model = False
        else:
          raise
      except:
        favorites_model = True

      if ctx.channel.id in state['r_18_id'] and favorites_model:#check command isn't it enter in nsfw channel
        Classification = "nsfw"
      else:
        Classification = "waifu"

      try:#check user isn't have favorites record yet
        favorites = favorites_list[str(ctx.author.id)][Classification][0]
      except:
        await ctx.reply('你還沒有任何收藏喔!')
        await ctx.message.add_reaction("❌")
        return
      
      img_url = favorites['url']
  
      source_url = favorites['source']

      page = '1/' + str(len(favorites_list[str(ctx.author.id)][Classification]))

      if ctx.channel.id in state['r_18_id'] and favorites_model:
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
        
    else:#if theme is unfound or command uncorrect
      await ctx.reply(f'{model} 不是randomwaifu的參數或主題類別')
      await ctx.message.add_reaction("❌")
      
async def setup(bot):
  await bot.add_cog(waifu(bot))