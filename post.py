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
        comment_section = content.xpath('//div[@class="_2b06"]')
        for comment in comment_section:
            comment_id = comment.xpath('div[2]').attrib['data-commentid']
            username = comment.xpath('div[1]/text()').get()
            message = comment.xpath('div[2]/text()').get()
            cmt = {
                'id': comment_id,
                'username': username,
                'message': message,
                # 'photos' : photos,
                }

            comments.append(cmt)
        return comments
        

    def unfold(self):
        content = Selector(text=self.page.content())
        see_prev_selector = "//div[@class='async_elem']"
        for _ in range(3):
            if len(content.xpath(see_prev_selector)) == 0:
                break
            self.page.locator(see_prev_selector).click()
            content = Selector(text=self.page.content())

        replies_selector = "//div[@class='_2b1h async_elem']"
        if len(content.xpath(replies_selector)) == 0:
            return

        # yes it is silly, but it's work
        while True:
            replies = self.page.locator(replies_selector).all()
            if len(replies) == 0:
                break
            replies[0].click()
            

    def close(self):
        self.page.close()

if __name__ == "__main__":
    url = 'https://m.facebook.com/groups/306516256927109/permalink/1193266828252043'

    browser_args = {
        'headless': False, # set as True to hide browser
        'channel': 'chromium', # chrome or msedge
        # 'executable_path': "/path/to/browser"
    }

    with sync_playwright() as pw:
        browser = pw.chromium.launch(**browser_args)
        context = browser.new_context(
            viewport= {
                "width": 1920, 
                "height": 1080,
            }
        )

        post = Post(url, context)
        post.collect()
        post.close()