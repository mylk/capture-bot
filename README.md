# Page Capture Bot

A Reddit bot that captures images of specific websites that are referenced in posts or comments and posts them back in a comment.
The images will be hosted to Imgur.

You can run your own instance. Follow the instructions below:

## Dependencies

```
sudo pip install praw imgurpython selenium
```

You can also use the ```requirements``` file to get all packages installed at the version I used during development:

```
sudo pip install -r requirements
```

or

```
make deps
```

In case you have both python2 and python3 you may need to use ```pip2``` instead.
```capture-bot``` is implemented in python2.

Also, you need to create a Reddit account and register an app, from your account preferences.
Last but not least, you need an account in Imgur to host the images.

## Edit the configuration

Edit ```capture_bot.cfg```:

### [Capture]
- ```watched_subreddits```, a JSON formatted string containing the subreddits you want the bot to watch
- ```captured_domain_names```, a JSON formatted string containing domains that you want to get captured

### [Reddit]
- ```id```, the application ID
- ```secret```, the application secret
- ```username```, the Reddit account username
- ```password```, the Reddit account password

### [Image Host]
- ```id```, the Imgur account API ID
- ```secret```, the Imgur account API secret

## Run the code

- clone or download the code
- get into the ```capture-bot``` directory
- run ```./main.py``` from your terminal