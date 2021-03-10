import os 
import time
import shutil
from pathlib import Path
from datetime import datetime


def get_free_space():     #считаем свободное место
  total, used, free = shutil.disk_usage("/")
  return used/total * 100

def get_days():           #формируем словарь [дни:путь]
  days = {}
  tree = os.walk('storage')
  for i in tree:
    if i[2]:
      try:
        file_date = datetime.strptime(i[0][i[0].index('/')+1:], "%Y/%m/%d")
      except ValueError:
        with open('log.txt', 'a') as log:  
          log.write('''%s \t [ERROR] \t '%s' Invalid date\n''' % (datetime.now(), i[0]))
      
      days[(datetime.today() - file_date).days] = i[0] 
  return days

def create_path(path, dest = 'archive'):  #создаем путь для переноса файлов
  new_path = dest

  for i in path[path.index('/')+1:].split                                 ('/'):
      new_path = os.path.join(new_path, i)
      if not os.path.exists(new_path):
        os.mkdir(new_path)  

def clear_path(old_path):                   #удаляем старую папку
  if not (os.listdir(old_path)):
    os.rmdir(old_path)
    path = Path(old_path)
    clear_path(path.parent)


def archive(free_space, days, days_list, dest = 'archive'):

  while get_free_space() < free_space or max(days_list) > 90:

    path = days.pop(days_list.pop(0))
    files = [os.path.join(path, f) for f in os.listdir(path)]

    create_path(path)
        
    for file in files:
      with open('log.txt', 'a') as log:  
        log.write('''%s \t File \t '%s' \t was moved from \t '%s' \t to \t'%s'\t\n''' % (datetime.now(), file.split('/')[-1], path, path.replace('storage','archive')))

      shutil.move(file, file.replace('storage','archive'))
    
    clear_path(path)


free_space = 10
days = {}
with open('log.txt', 'w') as log:  
  log.write('%s \t Service started.\n' % (datetime.now()))



while True:       #Главный цикл

  days = get_days()
  days_list = sorted(days, reverse=True)
  if get_free_space() < free_space or max(days_list) > 90:
    archive(free_space, days, days_list)
  
  time.sleep(5)





