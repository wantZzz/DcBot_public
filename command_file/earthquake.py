import discord
import os, sys
from discord.ext import commands

import asyncio
import requests
from cog import Cog_Extension
import json

sys.path.append(os.pardir)

class earthquake(Cog_Extension):
  def __init__(self,*arge,**kwargs):
    super().__init__(*arge,**kwargs)
    
    async def time_counter():

      await self.bot.wait_until_ready()
      
      while not self.bot.is_closed():
        r = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-F4282791-EEB6-425D-8408-A41249436E4B&limit=1&offset=0&format=JSON&areaName=%E5%8D%97%E6%8A%95%E7%B8%A3&stationName=%E7%8E%89%E5%B1%B1")
        
        if r.status_code == requests.codes.ok:
          with open("users_datafile/earthquake_json.json","r") as f:#open earthquake json data
            old_earthquake = json.load(f)
            
          new_earthquake = r.json()

          if not new_earthquake["records"]["earthquake"][0]["earthquakeNo"] == old_earthquake["records"]["earthquake"][0]["earthquakeNo"]:#if old earthquake id is different then new, post new message of new earthquake info

            info = new_earthquake["records"]["earthquake"][0]

            color = {"綠色": 0x00bb00, "黃色": 0xf9f900, "橙色": 0xea7500, "紅色": 0xea0000}#embed side line color
            if info['reportColor'] in color.keys():
              color_out = color[info['reportColor']]
            else:
              color_out = 0x8e8e8e#gray
    
            embed = discord.Embed(title=f"更新地震資訊 編號:{info['earthquakeNo']}",color=color_out)
            embed.set_author(name="中央氣象局-氣象資料開放平台")
            embed.set_thumbnail(url="http://www.shincheng.com.tw/Templates/TEZ_A107001/images/about/bg07.jpg")
        
            field_info = info['reportContent']
            field_info = field_info.split('，')
                    
            embed.set_image(url=info['reportImageURI'])#picture
                    
            embed.add_field(name=field_info[0],value=field_info[1][:-1],inline=False)
            embed.add_field(name="線上資料連結",value=info['web'],inline=False)#more infomation url
        
            location_info = info['earthquakeInfo']
        
            location = f"北緯 {location_info['epiCenter']['epiCenterLat']['value']} 度, 東經 {location_info['epiCenter']['epiCenterLon']['value']} 度\n{location_info['epiCenter']['location']}"
            depth = f"{location_info['depth']['value']} {location_info['depth']['unit']}"
            magnitude = f"{location_info['magnitude']['magnitudeType']} {location_info['magnitude']['magnitudeValue']}"
                    
            embed.add_field(name="震央位置",value=location,inline=False)#location
            embed.add_field(name="深度",value=depth)#depth
            embed.add_field(name="震度規模",value=magnitude,inline=True)#magnitude
            embed.set_footer(text="power by https://www.cwb.gov.tw/V8/C/", icon_url="http://www.shincheng.com.tw/Templates/TEZ_A107001/images/about/bg07.jpg")
            
            with open('users_datafile/state.json', 'r') as f:
              state = json.load(f)
            
            self.channel = self.bot.get_channel(state['main_channel'])

            await self.channel.send(embed=embed)
  
            with open("users_datafile/earthquake_json.json","w") as f:#rewrite earthquake json data
              f.write(json.dumps(new_earthquake))
        
        await asyncio.sleep(60)

    self.bot.loop.create_task(time_counter())

  @commands.command()
  async def earthquake_view(self, ctx,*input):#display last earthquake
    with open("users_datafile/earthquake_json.json","r") as f:
      old_earthquake = json.load(f)   
    
    info = old_earthquake["records"]["earthquake"][0]
    color = {"綠色": 0x00bb00, "黃色": 0xf9f900, "橘色": 0xea7500, "紅色": 0xea0000}#embed side line color
    if info['reportColor'] in color.keys():
      color_out = color[info['reportColor']]
    else:
      color_out = 0x8e8e8e#gray
      
    embed = discord.Embed(title=f"更新地震資訊 編號:{info['earthquakeNo']}",color=color_out)
    embed.set_author(name="中央氣象局-氣象資料開放平台")
    embed.set_thumbnail(url="http://www.shincheng.com.tw/Templates/TEZ_A107001/images/about/bg07.jpg")

    field_info = info['reportContent']
    field_info = field_info.split('，')
            
    embed.set_image(url=info['reportImageURI'])#picture
            
    embed.add_field(name=field_info[0],value=field_info[1][:-1],inline=False)
    embed.add_field(name="線上資料連結",value=info['web'],inline=False)#more infomation url

    location_info = info['earthquakeInfo']

    location = f"北緯 {location_info['epiCenter']['epiCenterLat']['value']} 度, 東經 {location_info['epiCenter']['epiCenterLon']['value']} 度\n{location_info['epiCenter']['location']}"
    depth = f"{location_info['depth']['value']} {location_info['depth']['unit']}"
    magnitude = f"{location_info['magnitude']['magnitudeType']} {location_info['magnitude']['magnitudeValue']}"
            
    embed.add_field(name="震央位置",value=location,inline=False)#location
    embed.add_field(name="深度",value=depth)#depth
    embed.add_field(name="震度規模",value=magnitude,inline=True)#magnitude
    embed.set_footer(text="power by https://www.cwb.gov.tw/V8/C/", icon_url="http://www.shincheng.com.tw/Templates/TEZ_A107001/images/about/bg07.jpg")
    
    await ctx.send(embed=embed)

async def setup(bot):
  await bot.add_cog(earthquake(bot))