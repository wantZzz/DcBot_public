def data_size_convert(size_input):
  if not type(size_input) == type(1):
    raise ValueError(f'correct vaule:{type(1)} ,error input vaule:{type(size_input)}')
  
  size_unit = ('B','KB','MB','GB','TB')
  size_input_mirro = size_input
  count = 0
  while size_input_mirro > 1024:
    size_input_mirro = round(size_input_mirro/1024,2)
    count+=1
    
  return str(size_input_mirro) + size_unit[count]