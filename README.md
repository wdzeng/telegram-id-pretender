# Telegram Peeker

![peek](res/peek.png)

Peek at other's Telegram username, taking it over once it is released.

## Install

The [telethon](https://docs.telethon.dev/en/stable/) library is used. Python 3.7 is required.

```python
pip3 install telethon argparse
```

## Usage

The script should be used with cron. A running is an attempt to change the username.

### CLI

Following command tries to update username to `fzhong`.

```py
TG_API_ID=<api_id> TG_API_HASH=<api_hash> python3 main.py fzhong
```

If you do not own an API key, generate one [here](https://my.telegram.org/apps).

### Docker

```bash
docker run -e TG_API_ID=api_id -e TG_API_HASH=api_hash [-it] hyperbola/telegram-peeker fzhong
```

The script should ask your login.

> You should answer your mobile phone number in international format. For Taiwanese, use `+8869xxxxxxxxx` instead of `09xxxxxxxx`.

### Login Automatically

The script asks your login interactively. To login automatically, you can `-s <file-to-save-session>` to save and restore the login session.

```py
TG_API_ID=api_id TG_API_HASH=api_hash python3 main.py -s ~/session fzhong
```

If such file is specified, the script tries to read session token from the file and uses that token to login. If such file does not exist, or if the session token is invalid, the script prompts your login and then save the updated token to that file so that it can login automatically in the next run. Keep that file secret since it contains sensitive data.

If the script is not running interactively, the session file should be specified. Otherwise the script exits without asking your login.

Since telegram requires 2FA login and this action must be performed on the spot, there is no support for logging automatically by setting username and password.

### Options

- `--id` PATH: read telegram api id from this file
- `--hash` PATH: read telegram api hash from this file
- `-s`, `--session` PATH: read login token from this file
- `-v`: verbose; should be `0`, `1` or `2`; default to `1`
- `--no-prompt`: do not ask login even in interactive shell

Following environment variables make effects. Noted that these variables refer to value directly, but not path to the value.

- `TG_API_ID`: telegram api id; overrides `--id` option
- `TG_API_HASH`: telegram api hash; overrides `--hash` option
- `TG_SESSION_PATH`: login session; overrides `--session` option

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
