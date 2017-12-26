import json
import os

root = os.path.dirname(__file__)
config_file = os.environ.get('CONFIG_FILE', '/'.join([root, 'default_config.json']))


def load_from_file():
    return json.load(open(config_file))


#
config = load_from_file()

# todo: старая схема конфигов. предложение все конфигурировать через файл
config.update({
    'TOKEN': config.get('TOKEN') or os.environ.get('TOKEN'),
    'PORT': config.get('PORT') or int(os.environ.get('PORT', '8443')),
    'URL': os.environ.get('URL'),
    'POLL': int(os.environ.get('POLL', 0)),
    'LOG_LEVEL': config.get('LOG_LEVEL') or os.environ.get('LOG_LEVEL', 'CRITICAL'),
})
