# Terrabase 🌳
Terrabase is a discord bot made to look up things on the wiki on the go: You can view anything available on the wiki without ever leaving Discord. This is mainly useful when you're talking with friends about Terraria and need to show them something. It's written in [`Python`](https://www.python.org/) using the [`discord.py`](https://github.com/Rapptz/discord.py) library.

# Installing & Running 🤖
I would prefer it if you don't run an instance of my bot. It can be invited using this [link](https://discord.com/api/oauth2/authorize?client_id=1069569059257077840&permissions=517543938112&scope=bot). If you still want to run an instance of my bot, however, here's how you can do it:
* Make a bot from the discord developer portal. Here's a [tutorial](https://discordpy.readthedocs.io/en/latest/discord.html) on setting up your bot.
* Give your bot all [intents](https://discordpy.readthedocs.io/en/latest/intents.html). Only the messages intents is required for it to function, but `/pop` checks if the user is on mobile or not which requires all intents.
* Make sure you have the latest stable version of [`Python`](https://www.python.org/) installed.
* Make a venv. In your root folder, run this command:
  ```py
  # Making a venv:
  python3 -m venv venv
  ```
* Installing the requirements. This is simply:
  ```py
  # Installing dependencies:
  pip install -U -r requirements.txt
  ```
* Enter your bot's token in the [`config.py`](https://github.com/its-truce/terrabase/blob/main/main/config.py) file.
