import discord
import os, sys
import asyncio

import json
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
import asyncio

from discord.ext import commands
from discord.ui import Button,View
import requests

from cog import Cog_Extension

sys.path.append(os.pardir)

class picture_search(Cog_Extension):
  @commands.command()
  async def image_search(self, ctx,*web_url):
    #------- command source: https://www.pyget.cn/p/185266 -------
    def circle_corner(img, radii):
    
      # draw a circle（for separating 4 corners）
      circle = Image.new('L', (radii * 2, radii * 2), 0)  # Create a canvas with a black background
      draw = ImageDraw.Draw(circle)
      draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # draw white circle
    
      # original image
      img = img.convert("RGBA")
      w, h = img.size
    
      # draw 4 corners（for separating 4 corners）
      alpha = Image.new('L', img.size, 255)
      alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # upper left corner
      alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # top right corner
      alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # bottom right corner
      alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # bottom left corner
      # alpha.show()
    
      img.putalpha(alpha)
      return img
      
    #--------------
      
    assece_content_type = ['image']
    
    try:
      file_path = web_url[0]
    except:
      mse_attach_file = ctx.message.attachments[0].content_type
      mse_attach_file = mse_attach_file.split('/')
      
      if mse_attach_file[0] in assece_content_type or mse_attach_file[1] == 'jpeg':#check source isn't it picture
        file_path = ctx.message.attachments[0].url

      else:
        await ctx.message.add_reaction("❌")
        return
      
    #Easter_egg = "https://cdn.waifu.im/d98c3be77f29f8c3.png"
    search_url = 'https://yandex.ru/images/search'
    
    file_tag = file_path.split('.')[-1]
    
    picture_get = requests.get(file_path)
    with open(f"picture/yandex/imagesearch.{file_tag}","wb") as f:#upload to yandex search picture
      f.write(picture_get.content)
    
    #------- command source: https://stackoverflow.com/questions/61978049/reverse-search-an-image-in-yandex-images-using-python -------
    files = {'upfile': ('blob', open(f"picture/yandex/imagesearch.{file_tag}", 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(search_url, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = search_url + '?' + query_string
    #print(img_search_url)
    #--------------
    
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
      data_list = k['thumbs']#get json similar to image

      try:#display all size of picture
        data = soup.find('div',class_='cbir-section cbir-section_name_other-sizes').find('div',class_='Root').get('data-state')
        k = json.loads(data)
        dups_list = k['items']

        str_image_dups = ""
        for image_dups in dups_list['large_dups']:#large size of picture
          large_str = f"{image_dups['text']}: \n[click link!]({image_dups['url']})\n"
          if len(str_image_dups) + len(large_str) >= 1024:
            break
          str_image_dups += large_str
          
        if not str_image_dups == "":
          embed.add_field(name='large size:', value=str_image_dups, inline=True)

        str_medium_dups = ""
        for medium_dups in dups_list['medium_dups']:#medium size of picture
          medium_str = f"{medium_dups['text']}: \n[click link!]({medium_dups['url']})\n"
          if len(str_medium_dups) + len(medium_str) >= 1024:
            break
          str_medium_dups += medium_str
          
        if not str_medium_dups == "":
          embed.add_field(name='medium size:', value=str_medium_dups, inline=True)

        str_small_dups = ""
        for small_dups in dups_list['small_dups']:#small size of picture
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

      unready_msg = await ctx.reply(embed=unready_msg,file=file)
      
      image_list = []
      count = 0
      
      for image_json in data_list:#make all similar picture to one picture
        imageUrl = image_json['imageUrl']
        height = image_json['height']
        width = image_json['width']
        image = requests.get(f"{'https:'+imageUrl}")
      
        if image.status_code == requests.codes.ok:#get all similar picture thumbnail
          with open(f"picture/yandex/picture/yandex{count}.png",'wb') as f:
            f.write(image.content)
      
          image_list.append({"height": height,"width": width,"path": f"picture/yandex/picture/yandex{count}.png"})
          count += 1
          
        else:
          pass

        await asyncio.sleep(0.2)
          
        #print(f"height: {height}\nwidth: {width}\n{'https:'+imageUrl}\n\n{'https://yandex.ru'+linkUrl}\n")
        
      sum_height = 0
      for image_json in image_list:#get picture thumbnail size to calculate row height
        sum_height += image_json['height']
      
      Specification_height = round(sum_height/len(image_list)*0.5)
      
      sum_width = 0 + len(image_list)*4 + 16
      for image_json in image_list:
        sum_width += image_json['width']*(Specification_height/image_json['height'])
      
      background_width = round(sum_width/4)
        
      background_image = Image.new('RGB',(background_width+8,(Specification_height*4)+20),(255,255,255))
      
      nowwidth_point = 4
      line = 0
      
      for image_k in image_list:#place all similar picture
        image_paste = Image.open(image_k['path'])
        #print(int(image_k['width']*(Specification_height/image_k['height'])))
        #print(Specification_height)
        
        image_paste = image_paste.resize((int(image_k['width']*(Specification_height/image_k['height'])),Specification_height),Image.NEAREST)

        image_paste = circle_corner(image_paste, radii=10)#make circle corner
      
        if nowwidth_point + int(image_k['width']*(Specification_height/image_k['height'])) > background_width:
          nowwidth_point = 4
          line += 1
      
          if line > 4:
            break
          
        background_image.paste(image_paste,(nowwidth_point,line*(Specification_height+4)+4),image_paste)
      
        nowwidth_point += int(image_k['width']*(Specification_height/image_k['height'])) + 4
      
      background_image.save(f'picture/yandex/output.png')
        
      file = discord.File(f'picture/yandex/output.png', filename="image.png")
      embed.set_image(url="attachment://image.png")

      await unready_msg.delete()

      await ctx.reply(embed=embed,file=file)
      await ctx.message.add_reaction("✅")

    else:
      await ctx.message.add_reaction("❌")
  
async def setup(bot):
  await bot.add_cog(picture_search(bot))