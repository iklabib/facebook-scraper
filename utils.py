import re

def clean_url(url: str) -> str:
    return re.sub(r'(#.*|\?.*)', '', url)