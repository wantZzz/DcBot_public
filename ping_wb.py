import requests
import time

def pinging(url):
  r = requests.get(url)
    
  if str(r.status_code)[0] == '5':
    delay = 'http error:'+ str(r.status_code)
  else:
    delay = round((r.elapsed.seconds*1000000+r.elapsed.microseconds)/1000,2) #執行所花時間
    #delay = round(int(delay)*1000,2)

  return str(delay) + "(ms)[" + str(r.status_code) + "]"