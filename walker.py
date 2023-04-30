import json
from typing import List
from parsel import Selector

class GroupWalker:
    def __init__(self, group_id, context):
        self.base_url = 'https://mbasic.facebook.com'
        self.url = f'{self.base_url}/groups/{group_id}'
        print(self.url)
        self.context = context

        self.page = self.context.new_page()
        # self.page.set_default_timeout(2_000)
        self.next_page = self.url
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.next_page is None:
            raise StopIteration()

        self.page.goto(self.next_page)
        content = Selector(text=self.page.content())
        url = content.xpath('//*[@id="m_group_stories_container"]/div/a').xpath('@href').get()

        if url is None: 
            self.next_page = None
        else:
            self.next_page = self.base_url + url
        return self.collect_permalinks()

    def collect_permalinks(self) -> List[str]:
        content = Selector(text=self.page.content())
        elements = content.xpath("//article[@class='dk dm dx']").xpath("@data-ft").getall()
        permalinks = [json.loads(element)['mf_story_key'] for element in elements]
        return permalinks
