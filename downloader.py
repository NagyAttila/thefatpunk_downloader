#!python3 -W ignore
from bs4 import BeautifulSoup
import urllib.request, re, wget
from os import mkdir, chdir

def conv_iri_to_url(iri):
    encoded = str(iri.encode('utf-8'))
    encoded = encoded.replace(' ','%20')
    return encoded[2:-1].replace('\\x','%')

def get_links(url):
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    return soup.find_all('a', href=True)

# Create output directory
output_dir = './albums'
mkdir(output_dir)
chdir(output_dir)

page_url = 'http://www.thefatpunk.dk/index.php?p=php/danish.php&name=Ads'
all_links = get_links(page_url)

letters = [x for x in all_links if re.search('letter=\w$', x['href']) != None]
for letter in letters:
    letter_url = u''.join(page_url + letter['href'])
    all_links = get_links(letter_url)
    bands = [x for x in all_links if re.search('letter=\w.*name=', x['href']) != None]
    for band in bands:
        band_url = conv_iri_to_url(u''.join((page_url, band['href'])))
        all_links = get_links(band_url)
        albums = [x for x in all_links if re.search('http', x['href']) != None]
        for album in albums:
            album_url = album['href']

            # Save album
            wget.download(album_url)

