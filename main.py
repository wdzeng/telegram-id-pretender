import os
import asyncio
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest, CheckUsernameRequest
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


async def info(s, client = None):
    print(s)
    if client is not None and send_message is not None:
        await client.send_message('me', '[Peeker] ' + s)


async def task(client):
    # https://docs.telethon.dev/en/stable/examples/users.html?highlight=updateusername#updating-your-username
    try:
        result = await client(CheckUsernameRequest(desired_username))
        if result:
            await info('Username is not occupied, try to take it.')
            await client(UpdateUsernameRequest(desired_username))
            await info('Successfully take the username: ' + desired_username)
            return 0
        else:
            # username is occupied
            await info('Username occupied: ' + desired_username)
            return 20
    except UsernameOccupiedError:
        await info('Username occupied: ' + desired_username)
        return 20
    except UsernameInvalidError:
        await info('Username invalid: ' + desired_username)
        return 21
    except UsernameNotModifiedError:
        await info('Username not modified: ' + desired_username)
        return 22
    except FloodWaitError as e:
        # https://docs.telethon.dev/en/stable/quick-references/faq.html#how-can-i-except-floodwaiterror
        await info('Flood. Remaning: ' + str(e.seconds))
        return 87


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
