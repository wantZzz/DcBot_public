import discord
import os, sys
import asyncio

import requests

import re
import json, base64

from cog import Cog_Extension

sys.path.append(os.pardir)

class web_risk(Cog_Extension):
  @commands.Cog.listener()
  async def on_message(self, message):      
    message_content = message.content
    urls = re.findall(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', message_content)#find all urls

    for hyperlink in urls:#remove specific domain urls
      if 'https://cdn.discordapp.com' in hyperlink[0]:
        urls.remove(hyperlink)

    if len(urls) <= 0:
      return

    def scan_url(url: str):#send url to virustotal scan isn't it malicious
      scan_api = "https://www.virustotal.com/api/v3/urls"
      scan_headers = {
            "Accept": "application/json",
            "x-apikey": os.environ['virustotal_key'],
            "Content-Type": "application/x-www-form-urlencoded"
        }
      payload = f"url={url}"

      scan_back = requests.post(scan_api, data=payload, headers=scan_headers)

      if scan_back.status_code == requests.codes.ok:
        return True
      else:
        return False

    def report_url(url: str):#get url scan report form virustotal
      url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
      report_api = f"https://www.virustotal.com/api/v3/urls/{url_id}"
      report_headers = {
            "Accept": "application/json",
            "x-apikey": os.environ['virustotal_key']
        }

      report_back = requests.get(report_api, headers=report_headers)

      if report_back.status_code == requests.codes.ok:
        return True, json.loads(report_back.text)
      else:
        return False, None
      
    urls_risk_emoji = '✅'

    for hyperlink in urls:
      #print(hyperlink[0])
      code, report = report_url(hyperlink[0])

      if not code: 
        if scan_url(hyperlink[0]):
          await asyncio.sleep(3)
          code, report = report_url(hyperlink[0])

          if not code:
            continue

        else:
          continue

      risk_votes = report['data']['attributes']['total_votes']
      security_votes = report['data']['attributes']['last_analysis_stats']
      
      #print(risk_votes)

      Security_Vendors = security_votes['malicious'] > 0 or security_votes['suspicious'] > 0

      Detections = risk_votes['harmless'] < risk_votes['malicious']
      
      if Detections or Security_Vendors:#check isn't it malicious
        urls_risk_emoji = '⚠'

    await message.add_reaction(urls_risk_emoji)
      
async def setup(bot):
  await bot.add_cog(web_risk(bot))