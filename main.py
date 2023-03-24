import time
import lxml
import shutil
import logging

import playwright
from parsel import Selector
from playwright.sync_api import sync_playwright

from post import Post
from page import Page
from post import Post

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

    pages = Page('306516256927109', context)
    for permalinks in pages:
        for permalink in permalinks:
            url = 'https://m.facebook.com/groups/306516256927109/permalink/' + permalink
            post = Post(url, context)
            print(post.collect())
            post.close()
    browser.close()