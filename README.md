# Comics publisher

This is the app automatically posting a random XCKD comic to your VK group wall.

### How to use

You'll need to create two environment variables with your VK access token and group ID where to post:
```
ACCESS_TOKEN='your access token'
GROUP_ID='your group ID'
```
You can put them into .env file next to main.py.

Just run the python script main.py with the following concole command:
```
python3 main.py
```

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
