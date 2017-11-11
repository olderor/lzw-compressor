import re


class Parser:
    @staticmethod
    def find_urls(text):
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    @staticmethod
    def find_hrefs(content):
        return re.findall(r'href=[\'"]?([^\'" >]+)', content, re.IGNORECASE)
