import discord
import sys
import os
import json
import asyncio
from discord.ext import commands
from discord.ui import Button,Select,View

#https://discordpy.readthedocs.io/en/master/interactions/api.html

import random
from cog import Cog_Extension
import time

sys.path.append(os.pardir)
from command_file.control import control

class barview(View):
  @discord.ui.button(label='Click me!', style=discord.ButtonStyle.green)
  async def Click_button_callback(self,ctx,button):
    info_msg = await ctx.channel.send('Good click!')
    await ctx.response.defer()

    await asyncio.sleep(5)
    await info_msg.delete()
    return

  @discord.ui.button(label="關閉指令大全", style=discord.ButtonStyle.gray, emoji='❌')
  async def delete_button_callback(self,ctx,button):
    await ctx.message.delete()

class help(Cog_Extension): 
  @commands.command()
  async def help(self,ctx):
    chou_wo = random.choice(['https://i.imgur.com/fHTtLm5.gif','https://c.tenor.com/nkCsX1ctiO8AAAAi/ayame-nakiri.gif','https://emoji.gg/assets/emoji/9848-ookamimio-guitar.gif','https://i.imgur.com/VK4XORR.gif','https://c.tenor.com/ZprD3ck1BkkAAAAC/shirakami-fubuki-hololive.gif','https://c.tenor.com/h0buQ0BdWBYAAAAd/subaru-duck-dance-subaru-duck.gif','https://thumbs.gfycat.com/MerryDecisiveAlligatorsnappingturtle-max-1mb.gif','https://media.discordapp.net/attachments/905434610203242517/952782204709240842/16472313742471012137899.gif','https://media.discordapp.net/attachments/905434610203242517/952807569255174144/ezgif-1-01d3a25b08.gif','https://cdn.discordapp.com/attachments/905434610203242517/952840192266473472/16472451837281553604402.gif','https://cdn.discordapp.com/attachments/905434610203242517/952842571045036042/1647245747052-205406297.gif','https://cdn.discordapp.com/attachments/905434610203242517/952842721511497758/1647245801676-425791542.gif','https://cdn.discordapp.com/attachments/905434610203242517/952842821558218772/1647245823451-46419864.png','https://cdn.discordapp.com/attachments/905434610203242517/952843002206904340/1647245870434-703104535.gif','https://cdn.discordapp.com/attachments/905434610203242517/952843742300225596/1647246035041-1789659675.png','https://cdn.discordapp.com/attachments/905434610203242517/952844051714027540/1647246107399-56214674.gif','https://cdn.discordapp.com/attachments/905434610203242517/952807569255174144/ezgif-1-01d3a25b08.gif','https://cdn.discordapp.com/attachments/905434610203242517/952782204709240842/16472313742471012137899.gif','https://c.tenor.com/LtRKM0XjCLkAAAAC/ninomae-inanis-smug.gif','https://i.pinimg.com/originals/b4/76/5f/b4765f9afdbbce895c60f504810ebe90.gif'])
    
    embed = {"color": 0x00FFFF,
             "author": {"name": '指令大全2.0',
                        "icon_url": chou_wo
                      },
             "footer": {"text": "此機器人由 wannaZzz#8989 維護", "icon_url": "https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png"}
            }

    test_embed = discord.Embed.from_dict(embed)

    """select = Select(options=[
      discord.SelectOption(label='find', emoji='🔭', description='搜尋已經消失的暴言與秘密'),
      discord.SelectOption(label='voice', emoji='🗣', description='友善啞巴的神奇功能'),
      discord.SelectOption(label='randomeme', emoji='🌄', description='找出讓你印象深刻的迷因'),
      discord.SelectOption(label='randomwaifu', emoji='🌹', description='從茫茫人海中找到你/妳的老婆'),
      discord.SelectOption(label='keyword', emoji='🔑', description='給我關鍵字，我給你張圖'),
      discord.SelectOption(label='word_maker', emoji='⌨', description='生產出一張帶文字圖片'),
      discord.SelectOption(label='other', emoji='🔍', description='雜項，無法分類的神奇指令聚集地'),
      discord.SelectOption(label='setting', emoji='⚙', description='設定指令')
    ])
    emoji = informations[Classification]['emoji'],
        description = informations[Classification]['description']
    
    """
    
    select = Select(placeholder="請選擇指令分類")

    with open('author_datafile/information.json',encoding="utf-8") as f:
      informations = json.load(f)

    async def help_commands_information(interaction):
      chose = select.values[0]
      
      commands_embed = discord.Embed(title=f'指令類別 {chose}', description=f"指令概述: {informations[chose]['infomation']}",color=0x00ffff)
      commands_embed.set_author(name="指令大全2.0", icon_url= chou_wo)

      commands_embed.add_field(name='\u200B', value='\u200B')

      commands_embed.set_footer(text="此機器人由 wannaZzz#8989 維護", icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")

      commands = informations[chose]['commands']

      for commands_num in range(0,len(commands)):
        commands_embed.add_field(name=commands[commands_num]['name'], value=commands[commands_num]['vaule'], inline=False)

      await interaction.response.edit_message(embed=commands_embed)

    for Classification in informations.keys():
      select.append_option(discord.SelectOption(
        label = Classification,
        emoji = informations[Classification]['emoji'],
        description = informations[Classification]['description']
      ))

    select.callback = help_commands_information

    view = barview()
    view.add_item(select)
    
    send_message = await ctx.send(embed=test_embed,view=view)
    await ctx.message.add_reaction("✅")

    await view.wait()
    try:
      await send_message.delete()
    except:
      pass
    
async def setup(bot):
  await bot.add_cog(help(bot))