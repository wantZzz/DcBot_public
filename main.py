import discord
from discord import app_commands
from discord.ext import commands

import json
import asyncio
import random, requests

import os, sys
import types
import traceback
import psutil
import atexit

from ping_wb import pinging

import time_myself

from data_size_unit import data_size_convert

already_send_error = False

open_time = ""

intents = discord.Intents().default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = ">",intents = intents,help_command = None)
tree = bot.tree

from command_file.time_on import time_on
log_name = time_on.log_name

with open('users_datafile/state.json',encoding="utf-8") as f:
  state = json.load(f)

close_time = 0
try:
  with open("Console_Log/time_stamp.txt", 'r') as f:
    close_time = f.read()
  with open(log_name, 'a') as f:
    f.write('上次系統關閉時間紀錄：'+ close_time +'\n')
  with open("Console_Log/time_stamp.txt", 'w') as f:
            f.write(time_myself.time_str_year_to_day_add_slash()+ " " +time_myself.time_str_hour_to_second_add_colon())
except:
  pass

def load_state():
  global state
  with open('users_datafile/state.json',encoding="utf-8") as f:
    state = json.load(f)

@bot.event
async def on_ready():
  global open_time
  print('目前登入身份：', bot.user)
  print('目前discord.py版本：',discord.__version__)
  status_w = discord.Status.online

  load_state()

  await bot.change_presence(status= status_w, activity=activity_w)

  open_time = time_myself.time_str_year_to_day_add_slash() + " " + time_myself.time_str_hour_to_second_add_colon()

  for slash_command in tree.get_commands():
    print(slash_command.name)

  await tree.sync()

  with open(log_name, 'a') as f:
    f.write('啟動時間：'+ open_time +'\n')

@bot.event
async def on_command_error(ctx, error, /) -> None:
  global already_send_error

  if isinstance(error, commands.CommandNotFound):
    await ctx.send("**Invalid command. Try using** `>help` **to figure out commands!**")

  error_output_str = f'type_of_error: {type(error)}\nIgnoring exception in command {ctx.command}:\n\n'
  file_name = f"error_event/{time_myself.time_str_year_to_day()}_{time_myself.time_str_hour_to_second()}.txt"
  with open(file_name, 'w') as f:
    f.write(error_output_str)

  traceback.print_exception(type(error), error, error.__traceback__, file=open(file_name, 'a'))

  print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
  traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@bot.command()
async def ping(ctx,*cmd):
  mode = 'None'
  if len(cmd) > 0:
    if cmd[0] == '-w':
      embed=discord.Embed(title="pong",description = '📶網路回應模式',color=0xff9ebb)
      mode = 'w'

    elif cmd[0] == '-m':
      embed=discord.Embed(title="pong",description = '🛠伺服器狀態模式',color=0xff9ebb)
      mode = 'm'
    
    else:
      await ctx.reply('ping-未知參數: '+cmd[0])
      return

  else:
    embed=discord.Embed(title="pong", color=0xff9ebb)
  
  embed.add_field(name="⌛訊號延遲", value=f'└ {round(bot.latency, 1)}(ms)', inline=False)
  embed.add_field(name="🔌啟動時間", value='└ '+open_time, inline=False)
  embed.add_field(name="📡系統版本", value='└ '+discord.__version__, inline=False)

  if mode == 'w':
    waifu_ping_de = pinging("https://api.waifu.im/random/?selected_tags=waifu")
    meme_ping_de = pinging('https://memes.tw')
    crawl_ping_de = pinging('http://wannazzz.pythonanywhere.com')

    web_delay_str = '├ **randomwaifu(waifu.im):** ' + waifu_ping_de + '\n└ **randomeme(memes.tw):** ' + meme_ping_de

    embed.add_field(name="📨網路來回回應耗時", value=web_delay_str, inline=False)

    crawl_delay_str = '└ '+crawl_ping_de

    embed.add_field(name="📨網頁爬蟲來回回應耗時", value=crawl_delay_str, inline=False)

  elif mode == 'm':

    cpu_percent_str = '└ '+str(psutil.cpu_percent(2))+'%'
    
    embed.add_field(name="💽CPU使用率", value=cpu_percent_str, inline=False)

    virtual_memory = psutil.virtual_memory()

    ram_percent_str = '└ '+str(virtual_memory.percent)+'%'
    
    embed.add_field(name="🎛RAM使用率", value=ram_percent_str, inline=False)

    ram_str = '└ '+data_size_convert(virtual_memory.used) + ' /' + data_size_convert(virtual_memory.total)
    
    embed.add_field(name="🎛RAM占用", value=ram_str, inline=False)
   
  embed.set_footer(text="此機器人由 wannaZzz#8989 製作")

  await ctx.send(embed=embed)

@bot.command()
async def ask_log(ctx,get_time):
  global state
  load_state()
  Maint = bot.get_user(state['Maintainer'])
  
  if ctx.author.id in state['Maintainer']:
    try:
      await ctx.send(file=discord.File(f"Console_Log/{get_time}.txt"))
      with open(log_name, 'a') as f:
        f.write(str(time_myself.time_str_hour_to_second_add_colon())+" ")
        f.write(f'get {get_time}.txt success\n')
      await Maint.send(f'get {get_time}.txt event success')
      await ctx.message.add_reaction("🆗")
    except:
      with open(log_name, 'a') as f:
        f.write(str(time_myself.time_str_hour_to_second_add_colon())+" ")
        f.write(f'get {get_time}.txt fail\n')
      await Maint.send(f'get {get_time}.txt event fail')
      await ctx.message.add_reaction("🆖")
  else:
    with open(log_name, 'a') as f:
      f.write(str(time_myself.time_str_hour_to_second_add_colon())+" ")
      f.write(f'get {get_time}.txt fail(權限)\n')
    await Maint.send(f'get {get_time}.txt event fail(權限')
    

def out_event():
  with open(log_name,'a') as f:
    f.write("程式關閉："+time_myself.time_str_year_to_day_add_slash()+" "+time_myself.time_str_hour_to_second_add_colon()+"\n")

atexit.register(out_event)

async def main():
    async with bot:
      for filelist in os.listdir("./command_file"):
        if filelist.endswith(".py"):
          if not(filelist[:-3] in classes_none):
            print(filelist)
            await bot.load_extension(f"command_file.{filelist[:-3]}")

      try:
        await bot.start(os.environ['dc_key'])
      except Exception as e:
        Retry_After = e.__dict__['response'].headers['Retry-After']
        status = e.__dict__['response'].status
    
        with open(log_name, 'a') as f:
          f.write(time_myself.time_str_hour_to_second_add_colon() + ' http-error:' + str(status) + ';Retry_After:' + str(Retry_After) + '\n')
      
        print(time_myself.time_str_hour_to_second_add_colon() + ' http-error:' + str(status) + ' ; Retry_After:' + str(Retry_After) + '\n')
    
        await_time = "預估等待時間: "+str(int(Retry_After)//3600)+":"+str(int(Retry_After)%3600//60)+":"+str(int(Retry_After)%60)
        print(await_time)
        

keep_alive.keep_alive()
asyncio.run(main())
      

#                   _oo0oo_
#                  o8888888o
#                  88" . "88
#                  (| -_- |)
#                   0\ = /0
#                 ___/`—‘\___
#                .’ \\| |// ‘.
#              / \\||| : |||// \
#            / _||||| -:- |||||- \
#              | | \\\ – /// | |
#              | \_| ”\—/” |_/ |
#             \ .-\__ ‘-‘ ___/-. /
#           ___’. .’ /–.–\ `. .’___
#       ."" ‘< `.___\_<|>_/___.’ >’ "".
#      | | : `- \`.;`\ _ /`;.`/ – ` : | |
#        \ \ `_. \_ __\ /__ _/ .-` / /
# =====`-.____`.___ \_____/___.-`___.-‘=====
#                    `=—=’
