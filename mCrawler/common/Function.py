import os
import re
from bs4 import BeautifulSoup


class Function:
    def __init__(self, *args, **kwargs):
        super(Function, self).__init__(*args, **kwargs)

    @classmethod
    def remove_carriage_return(cls, text):
        text = text.strip().rstrip(os.linesep).replace("\n", " ").replace("\r", " ")
        return text

    @classmethod
    def replace_tab_to_space(cls, text):
        text = text.strip().replace("\t", " ")
        return text

    @classmethod
    def replace_duplicate_to_space(cls, text):
        text = re.sub(' +', ' ', text).strip()
        return text

    @classmethod
    def remove_tags(cls, text, tag):
        text = re.sub('<' + tag + '.*?>.*?</' + tag + '>', '', text, 0, re.I | re.S)
        return text

    @classmethod
    def get_body(cls, text):
        text = re.search('<body.*/body>', text, re.I | re.S)
        return text

    @classmethod
    def get_text(cls, text):
        text = Function.remove_carriage_return(text)
        text = Function.replace_tab_to_space(text)
        text = Function.remove_tags(text, 'script')
        text = Function.remove_tags(text, 'head')
        text = Function.remove_tags(text, 'footer')
        text = Function.remove_tags(text, 'style')
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.extract().get_text()
        text = Function.replace_duplicate_to_space(text)
        return text
