import re
import unicodedata
import requests
import datetime
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def wordcloud(url):
    article = normalize_text(get_text_from_web(url))
    words_list = extract_words(article)
    generate_wordcloud(words_list)

def get_text_from_web(url):
    req = requests.get(url)
    # 日本語の文字化け防止
    req.encoding = req.apparent_encoding

    bs_obj = BeautifulSoup(req.text, "html.parser")
    content = bs_obj.find(id="main").get_text()
    return content

def normalize_text(content):
    text = re.sub('\u3000', '', content)
    text = re.sub('\n', ' ', text)
    text = re.sub('\\n', '', text)
    text = re.sub('\\n', ' ', text)

    norm_text = unicodedata.normalize('NFKC', text)
    return norm_text

def extract_words(text):
    t = Tokenizer()
    tokenized_text = t.tokenize(text)

    words_list = []
    for token in tokenized_text:
        tokenized_word = token.surface
        words_list.append(tokenized_word)

    return words_list

def generate_wordcloud(words_list):
    dir_path = 'out/wordcloud'
    font = 'fonts/ipaexg.ttf'
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    wordcloud = WordCloud(font_path=font, width=3000, height=1800, collocations=False, background_color='white').generate(''.join(words_list))

    plt.figure(figsize=(18, 12))
    plt.imshow(wordcloud)
    plt.tick_params(labelbottom=False, labelleft=False)
    plt.xticks([])
    plt.yticks([])
    plt.savefig("{0}/{1}_wordcloud.png".format(dir_path, now))