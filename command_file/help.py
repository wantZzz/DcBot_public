import discord
import os, sys
import json
import asyncio
from discord.ext import commands
from discord.ui import Button,Select,View

import random
from cog import Cog_Extension
import time

sys.path.append(os.pardir)

class barview(View):
  @discord.ui.button(label='Click me!', style=discord.ButtonStyle.green)#just for testing and fun
  async def Click_button_callback(self,ctx,button):
    info_msg = await ctx.channel.send('Good click!')
    await ctx.response.defer()

    await asyncio.sleep(5)
    await info_msg.delete()
    return

  @discord.ui.button(label="關閉指令大全", style=discord.ButtonStyle.gray, emoji='❌')#close page
  async def delete_button_callback(self,ctx,button):
    await ctx.message.delete()

class help(Cog_Extension): 
  @commands.command()
  async def help(self,ctx):#command list and info
    chou_wo = random.choice(['https://i.imgur.com/fHTtLm5.gif','https://c.tenor.com/nkCsX1ctiO8AAAAi/ayame-nakiri.gif','https://emoji.gg/assets/emoji/9848-ookamimio-guitar.gif','https://i.imgur.com/VK4XORR.gif','https://c.tenor.com/ZprD3ck1BkkAAAAC/shirakami-fubuki-hololive.gif','https://c.tenor.com/h0buQ0BdWBYAAAAd/subaru-duck-dance-subaru-duck.gif','https://thumbs.gfycat.com/MerryDecisiveAlligatorsnappingturtle-max-1mb.gif','https://c.tenor.com/LtRKM0XjCLkAAAAC/ninomae-inanis-smug.gif','https://i.pinimg.com/originals/b4/76/5f/b4765f9afdbbce895c60f504810ebe90.gif'])
    
    embed = {"color": 0x00FFFF,
             "author": {"name": '指令大全2.0',
                        "icon_url": chou_wo
                      },
             "footer": {"text": "this bot code was written by wannaZzz#8989", "icon_url": "https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png"}
            }

    test_embed = discord.Embed.from_dict(embed)
    
    select = Select(placeholder="請選擇指令分類")

    with open('users_datafile/information.json') as f:#open command info data
      informations = json.load(f)

    async def help_commands_information(interaction):
      chose = select.values[0]
      
      commands_embed = discord.Embed(title=f'指令類別 {chose}', description=f"指令概述: {informations[chose]['infomation']}",color=0x00ffff)
      commands_embed.set_author(name="指令大全2.0", icon_url= chou_wo)

      commands_embed.add_field(name='\u200B', value='\u200B')

      commands_embed.set_footer(text="this bot code was written by wannaZzz#8989", icon_url="https://cdn.discordapp.com/attachments/886787844067172372/931423453133799424/image.png")

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