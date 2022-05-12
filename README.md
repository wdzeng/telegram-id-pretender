# Telegram Peeker

![peek](res/peek.png)

Peek at other's Telegram username, taking it over once it is released.

## Install

The [telethon](https://docs.telethon.dev/en/stable/) library is used. Python 3 is required.

```python
pip3 install telethon
```

## Usage

The script should be used with cron. A running is an attempt to change the username.

Following command tries to update username to `fzhong`.

```py
TG_API_ID=<api_id> TG_API_HASH=<api_hash> DESIRED_USERNAME=fzhong python3 main.py
```

Or run the script using docker.

```bash
docker -e TG_API_ID=<api_id> \
       -e TG_API_HASH=<api_hash> \
       -e DESIRED_USERNAME=fzhong \
       [-it] \
       hyperbola/telegram-peeker:v1
```

### Login Automatically

The script asks your login interactively. To login automatically, you can provided a file to save and restore the session:

```py
TG_API_ID=<api_id> TG_API_HASH=<api_hash> DESIRED_USERNAME=fzhong TG_SESSION_PATH=~/session python3 main.py
```

If such file is specified, the script tries to read session token from the file and uses that token to login. If such file does not exist, or if the session token is invalid, the script prompts your login and then save the updated token to that file. Keep that file secret since it contains sensitive data.

If the script is not running non-interactively, the session file should be specified. Otherwise the script exits without asking your login.

Since telegram requires 2FA login and must be performed on the spot, there is no support for logging automatically given username and password.

### Options

Following environment variables make effects:

- `TG_API_ID`: Required. The telegram API ID.
- `TG_API_HASH`: Required. The telegram API hash.
- `TG_SESSION_PATH`: Optional. The path where telegram session token is saved.
- `DESIRED_USERNAME`: Required. The telegram username you want to take.
- `SEND_TG_MESSAGE`: Optional. If set, the script sends a message to your "Saved Messages" to inform the result.

If you do not own the API key, generate one [here](https://my.telegram.org/apps).

### Exit Code

- `0`: Successfully take the desired username.
- `20`: Desired username is occupied.
- `21`: Desired username is invalid.
- `22`: Desired username already owned by you.
- `30`: Failed to login.
- `40`: Failed for flood.
- `1`: Failed for any other reason.

## Caution

To avoid flood, run this script every 15 minutes would be good.
