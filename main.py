import requests
from pathlib import Path
import pprint
import json
import os
from dotenv import load_dotenv



def get_file_extension(url):
    return Path(url).suffix


def download_a_pic(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    pic_extension = get_file_extension(url)

    with open(Path.cwd().joinpath(f'{filename}{pic_extension}'), 'wb') as image:
        image.write(response.content)

def get_a_comic(number_of_comic):
    url = f'http://xkcd.com/{number_of_comic}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_pic = response.json()
    download_a_pic(comic_pic['img'], comic_pic['title'])
    # print(comic_pic['alt'])

def get_upload_url(token):
    vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    vk_params = {'access_token': token, 'v': '5.122', 'group_id': '197617370'}
    response = requests.get(vk_url, params=vk_params)
    return response.json()['response']['upload_url']

def post_a_comic(upload_url, token):
    with open('Python.png', 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        uploaded_pic = response.json()

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {'server': uploaded_pic['server'], 'photo': uploaded_pic['photo'], 'hash': uploaded_pic['hash'],
    'access_token': token, 'v': '5.122', 'group_id': '197617370'}
    response = requests.post(url, params=params)
    saved_pic = response.json()
    pprint.pprint(saved_pic)

    url = 'https://api.vk.com/method/wall.post'
    params = {'attachments': f"photo{saved_pic['response'][0]['owner_id']}_{saved_pic['response'][0]['id']}",
    'access_token': token, 'v': '5.122', 'group_id': '197617370'}
    response = requests.post(url, params=params)
    pprint.pprint(response.json())

def main():
    load_dotenv()
    vk_token = os.getenv('ACCESS_TOKEN')
    # get_a_comic(353)
    upload_url = get_upload_url(vk_token)
    # print(upload_url)
    post_a_comic(upload_url, vk_token)


if __name__ == '__main__':
    main()