import urllib.request
import urllib
import socket
import datetime
from re import findall

now = datetime.datetime.now()
f = open('sitemap.txt', 'r')
failed_pages = []
startSourcePath = '<loc>'
endSourcePath = '</loc>'


def find_links(text):

    urls = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))?[^(<)|(\n)]+'
    site_pages = [url for url in findall(urls, text) if url.strip()]
    return site_pages


def check_pages(pages):
    for page_url in pages:
        try:

            code = urllib.request.urlopen(page_url).getcode()
            print("{0} - {1}".format(page_url, code))

        except socket.error as e:
            print(page_url, "Ping Error: ", e)
            failed_pages.append(str(page_url + " - " + str(e)))


def http_from_https(pages_list):
    new_links = []
    for pages_list in pages_list:
        link = pages_list.replace("https", "http")
        new_links.append(link)
    return new_links


def generate_message():
    n = len(failed_pages)
    list = ""
    if (n > 0):
        list = "404 errors: \r\n"
        for failed_link in failed_pages:
            list = "\r\n".join((list, failed_link))
    else:
        list = "All links are correct\r\n\r\n"
    return list


def write_result(text):
    results = open('results.txt', 'a')
    results.write(now.strftime("\r\n%d-%m-%Y %H:%M"))
    results.write('\r\n')
    results.write(text)
    results.close()


a = find_links(f.read())
real_links = http_from_https(a)
check_pages(real_links)
write_result(generate_message())


