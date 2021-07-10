# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PostItem(scrapy.Item):
    link = scrapy.Field(serailizer=str)
    likes = scrapy.Field(serailizer=int)
    comments = scrapy.Field(serailizer=int)
    hashtags = scrapy.Field(serailizer=str)
    tags = scrapy.Field(serailizer=str)
    caption = scrapy.Field(serailizer=str)

class InfluencerItem(scrapy.Item):
    name = scrapy.Field(serializer=str)
    profile_pic = scrapy.Field(serializer=str)
    bio = scrapy.Field(serializer=str)
    location = scrapy.Field(serializer=str)
    followers = scrapy.Field(serailizer=int)
    total_posts = scrapy.Field(serailizer=int)
    email = scrapy.Field(serailizer=str)
    website = scrapy.Field(serailizer=str)
    posts = scrapy.Field(serailizer=list)
    account_type = scrapy.Field(serailizer=str)
    verified = scrapy.Field(serailizer=bool)

