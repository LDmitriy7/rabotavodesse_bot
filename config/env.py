import toml

_env = toml.load('env.toml')


class Bot:
    _data = _env['Bot']

    token: str = _data['token']
    id = int(token.split(':')[0])
    skip_updates = _data.get('skip_updates', False)


class Database:
    _data = _env['Database']

    name = _data['name']
    username = _data.get('username')
    password = _data.get('password')
    host = _data.get('host', 'localhost')
    port = _data.get('port', 27017)
    auth_source = _data.get('auth_source', 'admin')


class Users:
    _data = _env['Users']

    admins_ids = _data['admins_ids']


class Log:
    _data = _env['Log']

    file = _data.get('file')
    level = _data.get('level')


_misc = _env['Misc']

TECH_SUPPORT_CHAT_ID = _misc['TECH_SUPPORT_CHAT_ID']
MAIN_GROUP_ID = _misc['MAIN_GROUP_ID']
RESTRICT_TIME = _misc['RESTRICT_TIME']
USERS_TO_INVITE_COUNT = _misc['USERS_TO_INVITE_COUNT']

WHITELIST_CHATS_IDS = [TECH_SUPPORT_CHAT_ID, MAIN_GROUP_ID]
