from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import subprocess
import os


def space():
    print("""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
""")


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def getlink(request):
    request = request + "lyrics"
    print("getting url")
    raw_html = simple_get('https://www.youtube.com/search?q={0}'.format(request.lower().replace(" ", "+")))
    print("10%")
    html = BeautifulSoup(raw_html, 'html.parser')
    print("20%")
    links = str(html.select("a"))
    links = links.split("""
    """)
    print("30%")
    for i in links:
        i = str(i)
        watchurl = "/watch?" in i.lower()
        if watchurl == True:
            i = i.split(" ")
            print("50%")
            for j in i:
                watchurl = "/watch?" in j
                if watchurl == True:
                    j = j.split('"')
                    urlend = j[1]
            print("70%")
            break
    print("100%")
    return "https://www.youtube.com{0}".format(urlend)


def main():
    space()
    request = input("enter a song: ")
    link = getlink(request)
    print(link)
    output = os.system(
        """youtube-dl -f bestaudio -x --audio-format mp3 --output "{0}.%(ext)s" {1}""".format(request.replace(" ", "+"),
                                                                                              link))
    print("playing")
    subprocess.call(["AFPLAY", "{0}.mp3".format(request.replace(" ", "+"))])


while True:
    main()
