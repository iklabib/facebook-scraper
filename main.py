from playwright.sync_api import sync_playwright
import time

from post import Post
from walker import GroupWalker
import LoginPage
import config

conf = config.load()
browser_conf: dict = conf['browser']['chromium']
browser_args = {'viewport': browser_conf.pop('viewport', {})}

with sync_playwright() as pw:
    browser = pw.chromium.launch(**browser_conf)
    context = browser.new_context(**browser_args)

    LoginPage.login(context)
    time.sleep(5) # TODO: better waiting

    group = GroupWalker('306516256927109', context)
    for permalinks in group:
        print(permalinks)
        for permalink in permalinks:
            url = 'https://m.facebook.com/groups/306516256927109/permalink/' + permalink
            post = Post(url, context)
            post.close()
    browser.close()
