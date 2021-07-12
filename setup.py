"""Get the site emails from URL."""
#THIS IS SPAGHETTI CODE. THE SOURCE BELOW MEANS NOTHING, I INCLUDED IT CAUSE I DID NOT WRITE THIS. I NEEDED CODE TO POPULATE THINGS. 
# ALL COMMENTS ARE MINE. PLEASE DON'T LOOK IN TO THIS THAT DEEP LOL
#Source:https://www.w3resource.com/projects/python/web-programming/python-web-programming-8.php

import re
from html.parser import HTMLParser
from urllib import parse

import requests
class Parser(HTMLParser):
    def __init__(self, domain: str):
        HTMLParser.__init__(self)
        self.data = []
        self.domain = domain

    def handle_starttag(self, tag: str, attrs: str) -> None:
        """
        This function parse html to take takes url from tags
        """
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value != "#" and value != "":
                    if value not in self.data:
                        url = parse.urljoin(self.domain, value)
                        self.data.append(url)



def get_domain_name(url: str) -> str:
    ## internal_AD_domain = leftoverlunch.local
    ## internal_AD_SAPdomain = LLsap.com
    """
    This function get the main domain name
    >>> get_domain_name("https://a.b.c.d/e/f?g=h,i=j#k")
    'c.d'
    >>> get_domain_name("Not a URL!")
    ''
    """
    return ".".join(get_sub_domain_name(url).split(".")[-2:])
def get_sub_domain_name(url: str) -> str:
    """
    >>> get_sub_domain_name("https://a.b.c.d/e/f?g=h,i=j#k")
    'a.b.c.d'
    >>> get_sub_domain_name("Not a URL!")
    ''
    """
    return parse.urlparse(url).netloc
def emails_from_url(url: str = "https://github.com") -> list:
    """
    This function takes url and return all valid urls
    """

    domain = get_domain_name(url)

    parser = Parser(domain)

    try:

        r = requests.get(url)


        parser.feed(r.text)


        valid_emails = set()
        for link in parser.data:

            try:
                read = requests.get(link)

                emails = re.findall("[a-zA-Z0-9]+@" + domain, read.text)

                for email in emails:
                    valid_emails.add(email)
            except ValueError:
                pass
    except ValueError:
        exit(-1)

    return sorted(valid_emails)
if __name__ == "__main__":
    emails = emails_from_url("https://github.com")
    print(f"{len(emails)} emails found:")
    print("\n".join(sorted(emails)))
