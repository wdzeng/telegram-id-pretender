# Telegram Peeker

![peek](res/peek.png)

Peek at other's Telegram username, taking it over once it is released.

## Install

The [telethon](https://docs.telethon.dev/en/stable/) library is used. Python 3.7 is required.

```bash
pip3 install telethon
```

Or use the image on [dockerhub](https://hub.docker.com/repository/docker/hyperbola/telegram-peeker).

```bash
docker pull hyperbola/telegram-peeker:1.0
```

## Usage

The script should be used with cron. A running is an attempt to take over the username.

You need an API key to use the script. You can generate one [here](https://my.telegram.org/apps).

Following command tries to update username to `fzhong`.

```bash
# cli
TG_API_ID=<api_id> TG_API_HASH=<api_hash> python3 main.py fzhong

# docker
docker run -e TG_API_ID=<api_id> -e TG_API_HASH=<api_hash> [-it] hyperbola/telegram-peeker:1.0 fzhong
```

The script should ask your login.

> You should answer your mobile phone number in international format. For Taiwanese, use `+8869xxxxxxxxx` instead of `09xxxxxxxx`.

### Login Automatically

The script asks your login interactively. To login automatically, you can `-s <file-to-save-session>` to save and restore the login session.

```bash
TG_API_ID=api_id TG_API_HASH=api_hash python3 main.py -s ~/session fzhong
```

If such file is specified, the script tries to read session token from the file and uses that token to login. If such file does not exist, or if the session token is invalid, the script prompts your login and then save the updated token to that file so that it can login automatically in the next run. Keep that file secret since it contains sensitive data.

If the script is not running interactively, the session file should be specified. Otherwise the script exits without asking your login.

Since telegram requires 2FA login and this action must be performed on the spot, there is no support for logging automatically by setting username and password.

### Options

- `--id` PATH: read telegram api id from this file
- `--hash` PATH: read telegram api hash from this file
- `-s`, `--session` PATH: read login token from this file
- `-v`, '--verbose': verbose; should be `0`, `1` or `2`; default to `1`
- `-D`, `--no-prompt`: do not ask login even in interactive shell

Following environment variables make effects. Noted that these variables refer to value directly, but not path to the value.

- `TG_API_ID`: telegram api id; overrides `--id` option
- `TG_API_HASH`: telegram api hash; overrides `--hash` option
- `TG_SESSION`: login session; overrides `--session` option

### Verbosity

Verbosity can be set to either 0, 1, or 2 by `-v` flag. Control which message should be sent to your `Saved Messages` channel in your telegram account.

- `0`: do not send any message to telegram
- `1`: send critical messages only
- `2`: send all messages

### Exit Code

- `0`: successfully take the desired username
- `20`: desired username is occupied
- `21`: desired username is invalid
- `22`: desired username already owned by you
- `30`: failed to login
- `87`: failed for flood
- `1`: failed for any other reason
