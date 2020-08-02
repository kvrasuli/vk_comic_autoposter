import requests
from pathlib import Path
import json
import os
from dotenv import load_dotenv
import random
from pathlib import Path



def get_file_extension(url):
    return Path(url).suffix


def download_a_pic(url, filename):
    response = requests.get(url)
    response.raise_for_status()

    with open(Path.cwd().joinpath(filename), 'wb') as image:
        image.write(response.content)


def get_a_comic(number_of_comic):
    url = f'http://xkcd.com/{number_of_comic}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_pic = response.json()
    pic_extension = get_file_extension(comic_pic['img'])
    pic_filename = f"{comic_pic['title']}{pic_extension}"
    download_a_pic(comic_pic['img'], pic_filename)
    return pic_filename, comic_pic['alt']


def get_upload_url(token, group_id):
    vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    vk_params = {'access_token': token, 'v': '5.122', 'group_id': group_id}
    response = requests.get(vk_url, params=vk_params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def post_a_comic(upload_url, token, message, pic_filename, group_id):
    """put all three requests to VK api in one function cause they can be used only together"""
    
    with open(pic_filename, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        uploaded_pic = response.json()

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {'server': uploaded_pic['server'], 'photo': uploaded_pic['photo'], 'hash': uploaded_pic['hash'],
    'access_token': token, 'v': '5.122', 'group_id': group_id}
    response = requests.post(url, params=params)
    response.raise_for_status()
    saved_pic = response.json()
    
    url = 'https://api.vk.com/method/wall.post'
    params = {'attachments': f"photo{saved_pic['response'][0]['owner_id']}_{saved_pic['response'][0]['id']}",
    'access_token': token, 'v': '5.122', 'owner_id': f'-{group_id}', 'from_group': '1', 'message': message}
    response = requests.post(url, params=params)
    response.raise_for_status()


def get_number_of_comics():
    url = f'http://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_pic = response.json()
    return random.randint(0, last_pic['num'])


def main():
    load_dotenv()
    vk_token = os.getenv('ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    number_of_comic = get_number_of_comics()
    pic_filename, message = get_a_comic(number_of_comic)
    upload_url = get_upload_url(vk_token, group_id)
    post_a_comic(upload_url, vk_token, message, pic_filename, group_id)
    Path.unlink(Path.cwd().joinpath(pic_filename))


if __name__ == '__main__':
    main()