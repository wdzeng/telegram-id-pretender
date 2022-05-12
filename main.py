import os
import asyncio
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.errors import FloodWaitError, UsernameOccupiedError, UsernameInvalidError, UsernameNotModifiedError

api_id = os.environ['TG_API_ID']
api_hash = os.environ['TG_API_HASH']
session_path = os.environ.get('TG_SESSION_PATH')
desired_username = os.environ['DESIRED_USERNAME']
send_message = 'SEND_TG_MESSAGE' in os.environ

# API ID should be number
try:
    api_id = int(api_id)
except ValueError:
    print('Invalid api id: ' + api_id)
    sys.exit(30)


def login():
    # Login if needed
    # https://docs.telethon.dev/en/stable/concepts/sessions.html#different-session-storage
    session_text = ''
    if session_path != None:
        print('Use session file: ' + session_path)
        try:
            with open(session_path, 'r') as session_file:
                session_text = session_file.read()
        except:
            print('Failed to read session. Try login.')
    else:
        print('No session file provided. Try login.')

    if session_text == '' and not os.isatty(sys.stdin.fileno()):
        # if no session is provided and this is not an interactive shell
        # let the login failed without asking user.
        print('Not interactive shell. Do not prompt login. Login failed.')
        sys.exit(30)

    try:
        client = TelegramClient(StringSession(session_text), api_id, api_hash)
    except ValueError as e:
        print('Login failed.')
        sys.exit(30)
    return client


async def task(client):
    # https://docs.telethon.dev/en/stable/examples/users.html?highlight=updateusername#updating-your-username
    try:
        await client(UpdateUsernameRequest(desired_username))
        print('Username updated: ' + desired_username)
        msg = '[Peeker] Successfully take the username: ' + desired_username
        exit_code = 0
    except UsernameOccupiedError:
        print('Username occupied: ' + desired_username)
        msg = '[Peeker] Username occupied: ' + desired_username
        exit_code = 20
    except UsernameInvalidError:
        print('Username invalid: ' + desired_username)
        msg = '[Peeker] Invalid username: ' + desired_username
        exit_code = 21
    except UsernameNotModifiedError:
        print('Username not modified: ' + desired_username)
        msg = '[Peeker] You already take the username: ' + desired_username
        exit_code = 22
    except FloodWaitError as e:
        # https://docs.telethon.dev/en/stable/quick-references/faq.html#how-can-i-except-floodwaiterror
        print('Flood. Remaning: ' + str(e.seconds))
        msg = '[Peeker] Flood. Remaining: ' + str(e.seconds)
        exit_code = 87

    if send_message is not None:
        await client.send_message('me', msg)
    return exit_code


def saveLogin(client):
    if session_path != None:
        print('Session path is set to save login: ' + session_path)
        session_text = client.session.save()
        with open(session_path, 'w') as session_file:
            session_file.write(session_text)
        print('Login saved.')


async def main():
    client = login()
    async with client:
        saveLogin(client)
        exit_code = await task(client)
        sys.exit(exit_code)

asyncio.run(main())
