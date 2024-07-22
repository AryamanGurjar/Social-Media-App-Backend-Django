# Social Media App Backend
Created the backend for the social media app which has the functionality like
 - Registration
 - Friend Request Handling
 - Search

Made by:\
Name  = Aryaman Gurjar\
Contact = +91 9351407773, aryamangurjar6@gmail.com

Technologies Used: `Django` `Django Rest Framework` `Postgresql` `Docker`


## How to run

1. Create a virtual environment.

```shell
pip install virtualenv
python -m venv env
```
for windows:
```shell
.\env\Scripts\activate
```
for mac and linux
```shell
source env/bin/activate
```

2. Make the initial setup, Run Docker on your system, if you don't have docker please install it from here: https://docs.docker.com/engine/install/

Run this command inside working directory \
for linux and mac just run.
```shell
make dosetup
```
for windows:
```shell
dosetup.bat
```
Now the setup is done successfully

3. Now using Postman(https://www.postman.com/downloads/) execute the request as shown in social_media_app.postman_collection.json or https://www.postman.com/payload-meteorologist-65911660/workspace/backend-social-media-app
