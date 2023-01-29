from __future__ import annotations

import logging
import traceback
import typing as t
from dataclasses import dataclass

import requests
import yarl

from .parsing import list_links

TIMEOUT = 1


@dataclass
class CrawlerResult:
    url: yarl.URL
    children: t.Tuple[CrawlerResult] = ()
    exception: t.Optional[Exception] = None

    def has_exception(self) -> bool:
        return self.exception is not None

    def format_exception(self) -> t.Optional[str]:
        return self.exception and "".join(traceback.format_exception(self.exception))


def _crawl_children(
    session: requests.Session, base_url: yarl.URL, links: list[str], *, depth: int
) -> t.Iterable[CrawlerResult]:
    for link in links:
        link_url = base_url.join(yarl.URL(link))

        if depth == 1 or link_url.with_fragment(None) == base_url.with_fragment(None):
            yield CrawlerResult(url=link_url)
        else:
            yield _crawl_url(session, link_url, depth=depth)


def _crawl_url(
    session: requests.Session, url: yarl.URL, *, depth: int
) -> CrawlerResult:
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        links = list_links(response.content)
    except Exception as exception:
        return CrawlerResult(url=url, exception=exception)

    logging.debug("url %s, %s links", url, len(links))
    return CrawlerResult(
        url=url, children=tuple(_crawl_children(session, url, links, depth=depth - 1))
    )


def crawl_url(url: yarl.URL, *, depth: int) -> CrawlerResult:
    with requests.session() as session:
        return _crawl_url(session, url, depth=depth)
