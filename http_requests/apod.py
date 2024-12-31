import requests
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

apod_endpoint = 'https://api.nasa.gov/planetary/apod'
apod_key = os.environ.get('APOD_KEY')

def save_description(dir: str, data):
  explanation = data['explanation'].split('.')
  explanation_lines = list(map(lambda line: line.strip() + '\n', explanation))
  with open(f'{dir}/Description.txt', mode='w') as file:
    file.write(f'{data['date']}\n\n')
    
    file.write(f'\n{data['title']}\n\n\n')
    file.writelines(explanation_lines)

    if 'hdurl' in data:
      file.write(f'\nImage HD URL: {data['hdurl']}\n\n\n')
    else:
      file.write(f'\nVideo URL: {data['url']}\n\n\n')
      
    if 'copyright' in data: 
      file.write(f'{data['copyright']}')
    else: 
      file.write('NASA')

def save_image(dir: str, url: str):
  res = requests.get(url)

  with open(f'{dir}/APOD.jpg', mode='wb') as image:
    image.write(res.content)

def save_apod(data):
  dir_path = f'./APODs/{data['date']}'
  new_img_dir = Path(dir_path)
  new_img_dir.mkdir(exist_ok=True)
  save_description(dir_path, data)
  
  if 'hdurl' in data:
    save_image(dir_path, data['hdurl'])
  else:
    save_image(dir_path, data['thumbnail_url'])

  print(f'{data['date']} APOD CREATED at {dir_path}')

def get_apod(endpoint: str, date='today'):
  res = requests.get(f'{endpoint}?api_key={apod_key}&date={date}&thumbs=true')
  data = res.json()
  save_apod(data)


if __name__ == '__main__':
  get_apod(apod_endpoint, sys.argv[1])