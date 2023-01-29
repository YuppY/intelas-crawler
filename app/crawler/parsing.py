import typing as t

import bs4
from bs4 import BeautifulSoup, SoupStrainer


def list_links(source: t.TextIO) -> list[str]:
    tree = BeautifulSoup(source, "lxml", parse_only=SoupStrainer("a"))
    return list(
        filter(
            None, (child.get("href") for child in tree if isinstance(child, bs4.Tag))
        )
    )
