import discord
from discord.ext import commands
import json
import time_myself
from cog import Cog_Extension

with open('users_datafile/state.json') as f:#initial state setting from state file
  state = json.load(f)

def load_state():#update state values form state file
  global state
  with open('users_datafile/state.json') as f:
    state = json.load(f)

class control(Cog_Extension):
  noise = state['noise']
  administrator = state['administrator']
  Maintainer = state['Maintainer']
  voice = state['voice']
    
  @commands.command()
  async def onnoise(self, ctx):#if noise is True, bot won't send message in channel
    load_state()
    with open('users_datafile/state.json', 'w') as f:
        state['noise'] = True
        f.write(json.dumps(state))
    control.noise = True
    await ctx.message.add_reaction("🆗")

  @commands.command()
  async def stopnoise(self, ctx):#if noise is False, bot can send message in channel
    load_state()
    with open('users_datafile/state.json', 'w') as f:
        state['noise'] = False
        f.write(json.dumps(state))
    control.noise = False
    await ctx.message.add_reaction("🆗")
      
  @commands.command()
  async def onvoice(self, ctx):#if voice is True, bot can say in voice channel
    load_state()
    if ctx.author.id in control.administrator:
      with open('users_datafile/state.json', 'w') as f:
        state['voice'] = True
        f.write(json.dumps(state))
      control.voice = True
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def stopvoice(self, ctx):#if voice is False, bot won't say anything in voice channel
    load_state()
    if ctx.author.id in control.administrator:
      with open('users_datafile/state.json', 'w') as f:
        state['voice'] = False
        f.write(json.dumps(state))
      control.voice = False
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def listen_all(self, ctx):#if listen_all is True, bot will received every channel's messages in server(except nsfw channel)
    load_state()
    if ctx.author.id in control.administrator:
      with open('users_datafile/state.json', 'w') as f:
        state['listen_all'] = not state['listen_all']
        f.write(json.dumps(state))
      await ctx.message.add_reaction("🆗")
      
      if state['listen_all']:
        await ctx.message.add_reaction("🟢")
      else:
        await ctx.message.add_reaction("🔴")
        
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def voice_mode(self, ctx, mode_code):#if voice_mode is "only", the bot will just translate message from user who in "listen_only" list. if voice_mode is "all", translate all messages which in this server
    load_state()
    mode_code_list = ['only','all']
    if ctx.author.id in control.administrator and mode_code in mode_code_list:
      with open('users_datafile/state.json', 'w') as f:
        state['voice_mode'] = mode_code
        f.write(json.dumps(state))
        
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def listen_only(self, ctx):#add user to/remove user from "listen_only" list
    load_state()
    try:
      if id[2:-1] in state['only_voice']:
        with open('users_datafile/state.json', 'w') as f:
          state['only_voice'].remove(ctx.author.id)
          f.write(json.dumps(state))
        await ctx.message.add_reaction("🔇")
  
      else:
        with open('users_datafile/state.json', 'w') as f:
          state['only_voice'].append(ctx.author.id)
          f.write(json.dumps(state))
        await ctx.message.add_reaction("🔊")
          
      await ctx.message.add_reaction("🆗")
    except:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def delete_event_mode(self, ctx, mode_code):#change user his's (her's) nickname
    load_state()
    mode_code_list = ['all','nopicture']
    if ctx.author.id in control.administrator and mode_code in mode_code_list:
      with open('users_datafile/state.json', 'w') as f:
        state['delete_event_mode'] = mode_code
        f.write(json.dumps(state))
        
      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

  @commands.command()
  async def change_voicenick(self, ctx, user_id, change_nick):#change anyone nickname(just for administrator)
    load_state()
    if ctx.author.id in control.administrator:
      with open('users_datafile/data.json', 'r') as f:
        data = json.load(f)
        
      with open('users_datafile/data.json', 'w') as f:
        data[user_id] = change_nick
        f.write(json.dumps(data))

      await ctx.message.add_reaction("🆗")
    else:
      await ctx.message.add_reaction("🆖")

async def setup(bot):
  await bot.add_cog(control(bot))