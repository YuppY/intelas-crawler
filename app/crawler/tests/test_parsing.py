import io

import pytest

from crawler.parsing import list_links


@pytest.mark.parametrize(
    "source_str, expected",
    (
            (
                    """\
        <html><head><title>The Dormouse's story</title></head>
        <body>
        <p class="title"><b>The Dormouse's story</b></p>
        
        <p class="story">Once upon a time there were three little sisters; and their names were
        <a href="http://example.org/elsie" class="sister" id="link1">Elsie</a>,
        <a href="http://example.org/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://example.org/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>
        
        <p class="story">...</p>""",
                    [
                        "http://example.org/elsie",
                        "http://example.org/lacie",
                        "http://example.org/tillie",
                    ],
            ),
            (
                    """\
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        Invalid links are filtered: doctype and without href.
        <a href="http://example.org/">valid link</a>
        <a name="invalid">invalid link</a>
        """,
                    ["http://example.org/"],
            ),
    ),
)
def test_list_links(source_str, expected):
    assert list_links(io.StringIO(source_str)) == expected
