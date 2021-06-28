#!/usr/bin/env python3

import json
import ssl
from bs4 import BeautifulSoup
from urllib import request, parse


def google_search(keyword, start=1):
    url = "https://www.google.com/search?{}".format(parse.urlencode({"q": keyword, "start": start}))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    }
    req = request.Request(url, headers=headers, method="GET")
    context = ssl._create_unverified_context()
    html = request.urlopen(req, context=context)
    # print(html.read())

    # Parse search results: .rso, #hlcw0c, #g, #tF2Cxc, #yuRUbf, a
    parsed_html = BeautifulSoup(html, "html.parser")

    results = []
    for container in parsed_html.findAll("div", class_="tF2Cxc"):
        heading = container.find("h3", class_="LC20lb DKV0Md")

        if heading:
            heading = heading.text

        summary1 = container.find("span", class_="aCOpRe")
        if summary1:
            summary1 = summary1.text

        summary2 = container.find("div", class_="IsZvec")
        if summary2:
            summary2 = summary2.text

        link = container.find("div", class_="yuRUbf")
        if link:
            link = link.a["href"]

        results.append({
            "Heading": heading,
            "Summary1": summary1,
            "Summary2": summary2,
            "Link": link,
        })

    # print(json.dumps(results, indent=4, ensure_ascii=False))
    return results


if __name__ == "__main__":
    keyword = "debug"
    num = 20
    results = []
    while len(results) < num:
        t = google_search(keyword, start=len(results) + 1)
        results += t
    print(json.dumps(results, indent=4, ensure_ascii=False))

