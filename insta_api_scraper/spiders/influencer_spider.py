import json
import scrapy
from scrapy.selector import Selector

from insta_api_scraper.items import InfluencerItem, PostItem
from insta_api_scraper.parser import ig_parser


class InfluencerSpider(scrapy.Spider):
    name = 'influencer'

    def start_requests(self):

        with open('username.json', 'r') as fd:
            print(fd)
            data = json.loads(fd.read())
            for obj in data:
                handle = obj['username']
                yield scrapy.Request(
                    f'https://www.instagram.com/{handle}/',
                    callback=self.parse_influencer
                )

    def parse_influencer(self, response, **kwargs):
        parser = ig_parser.Parser()
        parser.feed(response.text)

        json_data = parser.Data['entry_data']['ProfilePage'][0]['graphql']['user']
        influencer = InfluencerItem({
            'name': json_data['full_name'],
            'profile_pic': json_data['profile_pic_url'],
            'bio': json_data['biography'],
            'location': json_data['business_address_json'],
            'followers': json_data['edge_followed_by']['count'],
            'total_posts': json_data['edge_owner_to_timeline_media']['count'],
            'email': json_data['business_email'],
            'website': json_data['external_url'],
            'account_type': ig_parser.get_account_type(json_data),
            'verified': json_data['is_verified']
        })

        posts = []
        for obj in json_data['edge_owner_to_timeline_media']['edges']:
            if obj['node'].get('edge_media_to_caption'):
                caption = obj['node']['edge_media_to_caption']['edges'][0]['node']['text']
            else:
                caption = obj['node']['accessibility_caption']
            post = PostItem({
                'link': 'https://instagram.com/p/{}/'.format(obj['node']['shortcode']),
                'likes': obj['node']['edge_liked_by']['count'],
                'comments': obj['node']['edge_media_to_comment']['count'],
                'hashtags': ig_parser.get_hashtags(caption),
                'tags': ig_parser.get_tags(obj),
                'caption': caption
            })
            posts.append(dict(post))
        influencer['posts'] = posts

        return influencer
