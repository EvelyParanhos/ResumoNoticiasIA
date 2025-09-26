import feedparser
from datetime import datetime


def pegar_noticias_do_dia(url):
    hoje = datetime.now().date()
    feed = feedparser.parse(url)
    noticias_do_dia = []
    for entry in feed.entries:
        if entry.published_parsed.tm_year == hoje.year and entry.published_parsed.tm_mon == hoje.month and entry.published_parsed.tm_mday == hoje.day:
            noticias_do_dia.append(entry)
    return noticias_do_dia