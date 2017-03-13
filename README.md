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

In case you have both python2 and python3 installed, you may need to use the ```pip2``` command instead.
```capture-bot``` is implemented in python2.

Alternatively, you can install the dependencies with the following:

```
make deps
```

Also, you need to have ```phantomjs``` installed. Use your package manager for that.
For example, if you use Ubuntu:

```
sudo apt-get install phantomjs
```

You also need to create a Reddit account and register an app from the account preferences.
Last but not least, you need an account in Imgur to host the images.

## Edit the configuration

Edit ```capture_bot.cfg```:

### [Capture]
- ```watched_subreddits```, a JSON formatted string containing the subreddits you want the bot to watch
- ```captured_domain_names```, a JSON formatted string containing domains that you want to get captured
- ```dump_directory```, the directory the screenshots will be temporarily saved

### [Reddit]
- ```id```, the application ID
- ```secret```, the application secret
- ```username```, the Reddit account username
- ```password```, the Reddit account password
- ```comment_text```, the text of the comment that will be posted

### [Image Host]
- ```id```, the Imgur account API ID
- ```secret```, the Imgur account API secret

## Other configuration options

In ```capture_bot.cfg```:

### [Generic]
- ```version```, the version of the application
- ```verbose```, display debugging messages
- ```persist_parsed_threads```, if set to False, examined posts and comments will be examined again the next time you run the application
  (caution: you will double-post if you disable this)

## Run the code

Clone or download the source code and then run:

```
make run
```

or:

```
cd capturebot # supposes you already are in the project's root directory
./capturebot.py
```

To view the available options while executing:

```
cd capturebot
./capturebot.py --help
```
