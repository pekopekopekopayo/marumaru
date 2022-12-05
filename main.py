import os
import pdb
from bs4 import BeautifulSoup as bs
import requests

url_id = '' 
url = 'https://marumaru521.com/bbs/cmoic/' + url_id
req = requests.get(url)
manga_main = bs(req.text, "html.parser").html
manga_path = f"{os.getcwd()}/{manga_main.find('h1', class_='text-left').text}"
manga_main = reversed(manga_main.select('td.list-subject'))
page = 0

if not os.path.exists(manga_path):
  print('디렉토리를 생성합니다')
  os.makedirs(manga_path)
print('다운로드를 시작합니다')

# 다운로드시 디렉토리를 포함 할 것인지에 대한 옵션 
dir_option = False

for manga in manga_main:
  title = manga.find('a').text.strip()
  
  if dir_option and not os.path.exists(f"{manga_path}/{title}"):    
    os.makedirs(f"{manga_path}/{title}")
  print(manga.find('a').text, '다운중')

  req = requests.get('https://marumaru521.com' + manga.find('a')['href'])
  manga_sub = bs(req.text, "html.parser").html
  
  for j, tag in enumerate(manga_sub.select('img.img-tag')):
    if dir_option:
      img_file = open(f"{manga_path}/{title}/{j}.png", 'wb')
    else:
      img_file = open(f"{manga_path}/{page}.png", 'wb')
      page += 1

    # 마루마루는 두개의 포맷을 사용하고있음
    if tag['src'][0] == '/':
      img_file.write(requests.get('https://marumaru521.com'+ tag['src']).content)
    else:
      img_file.write(requests.get(tag['src']).content)
    img_file.close()