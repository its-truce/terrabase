import aiohttp
import asyncio
import bs4
import string
from colorthief import ColorThief
from io import BytesIO
from urllib.request import urlopen
import urllib.request
from datetime import datetime

def markdown_links(tag: bs4.Tag):
    for img in tag.find_all('img'):
        img.decompose()
    for link in tag.find_all('a'):
        href = link.get('href')
        link_text = link.text
        link.replace_with(f'[{link_text}](https://terraria.wiki.gg{href})')
    for a in tag.find_all('a'):
        a.unwrap()
    return tag.text

async def scrape(search):
    caps = string.capwords(search, sep=None)
    page = caps.replace(" ", "_")
    URL = "https://terraria.wiki.gg/wiki"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}/{page}", allow_redirects=True) as response:
            redirect = response.url
            async with session.get(redirect) as redirect_response:
                body = await redirect_response.text()
    soup = bs4.BeautifulSoup(body, "html.parser")
    title = soup.find(id="firstHeading")
    print(title.string)
    pre = soup.find(id="mw-content-text").find("p")
    desc = markdown_links(pre)
    print(desc)
    img = soup.find(id="mw-content-text").find("img").get("src")
    now = datetime.now()
    url = f"https://terraria.wiki.gg{img}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    respi = urllib.request.urlopen(req)
    f = BytesIO(respi.read())
    done = datetime.now()
    print(done - now)

# asyncio.run(scrape(str(input("Page to search for: "))))
