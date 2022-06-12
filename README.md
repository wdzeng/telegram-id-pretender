# Telegram ID Pretender

[![release](https://badgen.net/github/release/wdzeng/telegram-id-pretender/stable?color=red)](https://github.com/wdzeng/telegram-id-pretender/releases/latest)
[![github](https://badgen.net/badge/icon/github/black?icon=github&label=)](https://github.com/wdzeng/telegram-id-pretender)
[![docker](https://badgen.net/badge/icon/docker?icon=docker&label=)](https://hub.docker.com/repository/docker/hyperbola/telegram-id-pretender)

![peek](res/peek.png)

Peek at other's Telegram username, taking it over once it is released.

## Install

### Python

Python 3.7 or up is required.

The [telethon](https://docs.telethon.dev/en/stable/) library is used.

```bash
pip3 install telethon
```

### Docker

Use the image on [dockerhub](https://hub.docker.com/repository/docker/hyperbola/telegram-id-pretender).

```bash
docker pull hyperbola/telegram-id-pretender:1
```

#### Supported tags

- `1`, `1.0`

## Usage

A running is an attempt to take over the username; therefore the script should be used with cron.

Following command tries to update username to `fzhong`. You need an API key to use the script. You can generate one [here](https://my.telegram.org/apps).

```bash
# python
TG_API_ID=<api_id> TG_API_HASH=<api_hash> python3 main.py fzhong

# docker
docker run [-it]\
    -e TG_API_ID=<api_id> \
    -e TG_API_HASH=<api_hash> 
    hyperbola/telegram-id-pretender:1 fzhong
```

The script should ask your login.

> **Warning**
> You should answer your mobile phone number in international format. For Taiwanese, use `+8869xxxxxxxxx` instead of `09xxxxxxxx`.

## Automatic Login

The script asks your login interactively. To do automatic login, you can `-s <session-file>` to save and restore the login session.

```bash
# python
TG_API_ID=<api_id> TG_API_HASH=<api_hash> python3 main.py -s /path/to/session/file fzhong

# docker
docker run [-it] \
    -v /path/to/session:/session \
    -e TG_API_ID=<api_id> \
    -e TG_API_HASH=<api_hash> \
    hyperbola/telegram-id-pretender:1 -s /session fzhong
```

If session file is specified, the script tries to read session token from the file and uses it to login; otherwise if session file does not exist, or if session token is invalid, the script prompts your login and then saves the updated token to session file so that it can perform automatic login in the next run. Keep session file secret since it contains sensitive data.

If the script is not running interactively, the session file must be specified. Otherwise the script fails without asking your login.

Since telegram requires 2FA login and this action must be performed on the spot, there is no support automatic login by setting username and password.

## Options

- `--id` PATH: read telegram api id from this file
- `--hash` PATH: read telegram api hash from this file
- `-s`, `--session` PATH: read login token from this file
- `-v`, `--verbose`: verbosity level; should be `0`, `1` or `2`; default to `1`
- `-D`, `--no-prompt`: do not ask login even in interactive shell

Following environment variables make effects. Noted that these variables refer to value directly, but not path to the value.

- `TG_API_ID`: telegram api id; overrides `--id` option
- `TG_API_HASH`: telegram api hash; overrides `--hash` option
- `TG_SESSION`: login session; overrides `--session` option

## Verbosity

Verbosity can be set to either 0, 1, or 2 by `-v` flag. Control which message should be sent to your `Saved Messages` channel in your telegram account.

- `0`: do not send any message
- `1`: send critical messages only
- `2`: send all messages

## Exit Code

- `0`: successfully took the desired username
- `20`: desired username is occupied
- `21`: desired username is invalid
- `22`: desired username is already owned by you
- `30`: failed to login
- `87`: failed for flood
- `1`: failed for any other reason

## Sister Bots

- [Shopee Coins Bot](https://github.com/wdzeng/shopee-coins-bot/)
- [Pinkoi Coins Bot](https://github.com/wdzeng/pinkoi-coins-bot/)
- [PTT Login Bot](https://github.com/wdzeng/ptt-login-bot/)
