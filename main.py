import os
import asyncio
import sys
import argparse
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateUsernameRequest, CheckUsernameRequest
from telethon.errors import FloodWaitError, UsernameOccupiedError, UsernameInvalidError, UsernameNotModifiedError


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super().__init__(prog, max_help_position=40, width=80)

    # https://stackoverflow.com/a/31124505/8386446
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string


def fmt(prog): return CustomHelpFormatter(prog)


# Parse argument
parser = argparse.ArgumentParser(formatter_class=fmt)
parser.add_argument(
    '--id', type=str, help='path to file containing telegram api id', metavar='')
parser.add_argument('--hash', type=str,
                    help='path to file containing telegram api hash', metavar='')
parser.add_argument('-s', '--session', dest='session', type=str,
                    help='path to session file', metavar='')
parser.add_argument('-v', '--verbose', dest='verbose', type=int, default=1,
                    help='verbose', choices=[0, 1, 2], metavar='')
parser.add_argument('-D', '--no-prompt', dest='no_prompt', default=False, action='store_true',
                    help='force use session and don\'t prompt login')
parser.add_argument('username', type=str, help='desired username')
args = parser.parse_args()

verbose = args.verbose
no_prompt = args.no_prompt


async def info(s, level, client=None):
    print(s)
    if client is not None and verbose >= level:
        await client.send_message('me', '[Telegram ID Pretender] ' + s)


def read_text(path):
    if path is None:
        return None
    with open(path, 'r') as f:
        text = f.read()
        return text


def get_api_id(id_path):
    api_id = os.environ.get('TG_API_ID')
    if api_id is not None:
        print('Use api id specified in environment variable.')

        try:
            api_id = int(api_id)
        except ValueError:
            print('Invalid api id. Must be number.')
            sys.exit(1)

        return api_id

    try:
        api_id = read_text(id_path)
    except:
        print('Cannot read telegram api id from file: ' + id_path)

    if api_id is None:
        print('Please give telegram api id.')
        sys.exit(1)

    return api_id


def get_api_hash(hash_path):
    api_hash = os.environ.get('TG_API_HASH')
    if api_hash is not None:
        print('Use api hash specified in environment variable.')
        return api_hash

    try:
        api_hash = read_text(hash_path)
    except:
        print('Cannot read telegram api hash from file: ' + hash_path)
    if api_hash is None:
        print('Please give telegram api hash.')
        sys.exit(1)

    return api_hash


def get_session(session_path):
    session_code = os.environ.get('TG_SESSION')
    if session_code is not None:
        print('Use session code specified in environment variable.')
        return session_code

    try:
        session_code = read_text(session_path)
    except:
        session_code = None

    return session_code


def login(api_id, api_hash, session_code):
    # Login if needed
    # https://docs.telethon.dev/en/stable/concepts/sessions.html#different-session-storage

    if (session_code is None or session_code == '') and (no_prompt or not os.isatty(sys.stdin.fileno())):
        print('Login failed.')
        sys.exit(30)

    try:
        client = TelegramClient(StringSession(session_code), api_id, api_hash)
    except ValueError:
        print('Login failed.')
        sys.exit(30)

    return client


async def take_username(client, desired_username):
    # https://docs.telethon.dev/en/stable/examples/users.html?highlight=updateusername#updating-your-username
    try:
        # Check if the username is already owned by the client
        me = await client.get_me()
        if me.username == desired_username:
            await info('Username not modified: ' + desired_username, 1, client)
            return 22

        # Check if the username is available
        username_available = await client(CheckUsernameRequest(desired_username))

        if not username_available:
            await info('Username occupied: ' + desired_username, 2, client)
            return 20

        await info('Username is not occupied, try to take it.', 1, client)
        await client(UpdateUsernameRequest(desired_username))
        await info('Successfully take the username: ' + desired_username, 1, client)
        return 0

    except UsernameOccupiedError:
        await info('Username occupied: ' + desired_username, 2, client)
        return 20

    except UsernameInvalidError:
        await info('Username invalid: ' + desired_username, 1, client)
        return 21

    except UsernameNotModifiedError:
        await info('Username not modified: ' + desired_username, 1, client)
        return 22

    except FloodWaitError as e:
        # https://docs.telethon.dev/en/stable/quick-references/faq.html#how-can-i-except-floodwaiterror
        await info('Flood. Remaning: ' + str(e.seconds), 2, client)
        return 87


def save_login(client, session_path):
    if session_path is not None:
        print('Save login token at: ' + session_path)
        session_code = client.session.save()
        with open(session_path, 'w') as session_file:
            session_file.write(session_code)
        print('Login saved.')


async def main():
    api_id = get_api_id(args.id)
    api_hash = get_api_hash(args.hash)
    session_code = get_session(args.session)
    desired_username = args.username

    # Login
    client = login(api_id, api_hash, session_code)

    async with client:
        save_login(client, args.session)
        exit_code = await take_username(client, desired_username)
        sys.exit(exit_code)


asyncio.run(main())
