import re
from parsel import Selector
from utils import clean_url
from playwright.sync_api import sync_playwright


class Post:
    def __init__(self, url, context):
        self.url = url
        self.context = context

        self.page = self.context.new_page()
        self.page.goto(self.url)
        self.page.set_default_timeout(2_000)
        self.unfold()

    def collect(self):
        collections = {}
        collections['comments'] = self.collect_comments()
        return collections

    def collect_comments(self):
        # comment:
        #   - id
        #   - message
        #   - photos 
        #   - reactions
        #   - replies

        comments = []
        content = Selector(text=self.page.content())
        comment_section = content.xpath('//div[@class="x1y1aw1k xn6708d xwib8y2 x1ye3gou"]')

        for comment in comment_section:
            # comment_id = comment.xpath('[@class="xt0psk2"]').attrib['href']
            username = comment.xpath('span[@class="x3nfvp2"]/span/text()').get()
            message = comment.xpath('div[@class="x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r"]/div/text()').get()
            cmt = {
                # 'id': comment_id,
                'username': username,
                'message': message,
                # 'photos' : photos,
                }
            comments.append(cmt)
        return comments

    def unfold(self):
        see_prev_selector = "div[@class='x78zum5 x1iyjqo2 x21xpn4 x1n2onr6']"

        content = Selector(text=self.page.content())
        content = content.xpath("//div[@class='x1jx94hy x12nagc']")
        for _ in range(3):
            if len(content.xpath(see_prev_selector)) == 0:
                break
            self.page.locator(see_prev_selector).click()
            content = Selector(text=self.page.content())
            content = content.xpath("//div[@class='x1jx94hy x12nagc']")

        replies_selector = "div[@class='x78zum5 x1iyjqo2 x21xpn4 x1n2onr6']"
        if len(content.xpath(replies_selector)) == 0:
            return

        # yes it is silly, but it's working
        while True:
            replies = self.page.locator(replies_selector).all()
            if len(replies) == 0:
                break
            replies[0].click()

    def close(self):
        self.page.close()
