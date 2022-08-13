import time

def time_str_year_to_day():
  now = time.localtime(time.time())

  day_2num = now.tm_mday+((now.tm_hour + 8)//24)
  mon_2num = now.tm_mon

  if day_2num < 10:
    day_str = "0"+str(day_2num)
  else:
    day_str = str(day_2num)

  if mon_2num < 10:
    mon_str = "0"+str(mon_2num)
  else:
    mon_str = str(mon_2num)

  collect_name = str(now.tm_year) + mon_str + day_str
  return collect_name

def time_str_year_to_day_add_slash():
  now = time.localtime(time.time())

  day_2num = now.tm_mday+((now.tm_hour + 8)//24)
  mon_2num = now.tm_mon

  if day_2num < 10:
    day_str = "0"+str(day_2num)
  else:
    day_str = str(day_2num)

  if mon_2num < 10:
    mon_str = "0"+str(mon_2num)
  else:
    mon_str = str(mon_2num)

  collect_name = str(now.tm_year) +"/"+ mon_str +"/"+ day_str
  return collect_name

def time_str_hour_to_second_add_colon():
  now = time.localtime(time.time())
  hour_str_nu = (now.tm_hour + 8 + 24) % 24

  if hour_str_nu//10 == 0:
    hour_str = '0'+ str(hour_str_nu)
  else:
    hour_str = str(hour_str_nu)

  if now.tm_min < 10:
    min_str = '0'+ str(now.tm_min)
  else:
    min_str = str(now.tm_min)

  if now.tm_sec < 10:
    sec_str = '0'+ str(now.tm_sec)
  else:
    sec_str = str(now.tm_sec)

  document_name = hour_str + ":" + min_str + ":" + sec_str
  return document_name

def time_str_hour_to_second():
  now = time.localtime(time.time())
  hour_str_nu = (now.tm_hour + 8 + 24) % 24

  if hour_str_nu//10 == 0:
    hour_str = '0'+ str(hour_str_nu)
  else:
    hour_str = str(hour_str_nu)

  if now.tm_min < 10:
    min_str = '0'+ str(now.tm_min)
  else:
    min_str = str(now.tm_min)

  if now.tm_sec < 10:
    sec_str = '0'+ str(now.tm_sec)
  else:
    sec_str = str(now.tm_sec)

  document_name = hour_str + min_str + sec_str
  return document_name

def time_pan():
  now = time.localtime(time.time())
  return now.tm_sec + now.tm_min * 100 + ((now.tm_hour + 8 + 24) % 24) * 10000 + now.tm_mday * 1000000 + now.tm_mon * 100000000 + now.tm_year * 10000000000

def time_pane():
  now = time.localtime(time.time())
  return now.tm_min + ((now.tm_hour + 8 + 24) % 24) * 100