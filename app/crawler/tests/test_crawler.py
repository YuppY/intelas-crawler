from unittest import mock

import yarl

from crawler.crawler import CrawlerResult, crawl_url


def test_crawl_url(requests_mock):
    requests_mock.get(
        "http://example.org/parent",
        text="""\
<a href="http://example.org/son">son</a>
<a href="http://example.org/daughter">daughter</a>
<a href="http://example.org/exception">exception</a>
<a href="#self-reference">self reference</a>
""",
    )
    requests_mock.get(
        "http://example.org/son",
        text="""\
<a href="http://example.org/granddaughter">granddaughter</a>
""",
    )
    requests_mock.get(
        "http://example.org/daughter",
        text="""\
<a href="http://example.org/grandson">grandson</a>
""",
    )
    requests_mock.get(
        "http://example.org/granddaughter",
        text="""\
<a href="http://example.org/grandgranddaughter">grandgranddaughter</a>
""",
    )
    requests_mock.get("http://example.org/exception", status_code=500)

    assert crawl_url(yarl.URL("http://example.org/parent"), depth=3) == CrawlerResult(
        url=yarl.URL("http://example.org/parent"),
        children=(
            CrawlerResult(
                url=yarl.URL("http://example.org/son"),
                children=(
                    CrawlerResult(url=yarl.URL("http://example.org/granddaughter"),),
                ),
            ),
            CrawlerResult(
                url=yarl.URL("http://example.org/daughter"),
                children=(CrawlerResult(url=yarl.URL("http://example.org/grandson"),),),
            ),
            CrawlerResult(
                url=yarl.URL("http://example.org/exception"), exception=mock.ANY
            ),
            CrawlerResult(url=yarl.URL("http://example.org/parent#self-reference"),),
        ),
    )


class TestCrawlerResult:
    def test_has_exception(self):
        assert not CrawlerResult(url=yarl.URL("foo")).has_exception()
        assert CrawlerResult(url=yarl.URL("foo"), exception=Exception()).has_exception()

    def test_format_exception(self):
        assert CrawlerResult(url=yarl.URL("foo")).format_exception() is None
        assert (
            CrawlerResult(url=yarl.URL("foo"), exception=Exception()).format_exception()
            == "Exception\n"
        )
