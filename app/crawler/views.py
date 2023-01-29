import yarl
from django.shortcuts import render

from .crawler import crawl_url

DEPTH = 3


def index(request):
    context = {}
    if request.method == "POST":
        url = yarl.URL(request.POST["url"])
        context.update({"url": url, "result": crawl_url(url, depth=DEPTH)})
    return render(request, "index.html", context)
