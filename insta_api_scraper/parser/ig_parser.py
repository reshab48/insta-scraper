import re
import json
from html.parser import HTMLParser


class Parser(HTMLParser):

    Data = {}

    def handle_data(self, data):
        if data.startswith("window._sharedData"):
            self.Data = json.loads(data[data.find('{"config"'): -1])
        else:
            pass


def get_account_type(data):
    if data['is_business_account']:
        return 'Business'
    elif data['is_professional_account']:
        return 'Professional'
    else:
        return 'Individual'


def get_tags(data):
    tags = []
    for obj in data['node']['edge_media_to_tagged_user']['edges']:
        tags.append('@{}'.format(obj['node']['user']['username']))
    return ','.join(tags)


def get_hashtags(caption):
    hashtags = []
    for obj in re.findall(r'#(\w+)', caption):
        hashtags.append('#{}'.format(obj))
    return ','.join(hashtags)
