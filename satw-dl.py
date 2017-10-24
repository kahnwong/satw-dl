import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from time import sleep
from fake_useragent import UserAgent

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

class Scraper(object):
    def __init__(self, name, url, pages, start):
        self.name = name
        self.url = url
        self.pages = pages
        self.start = start-1

    def make_request(self, url):
        response = requests.get(url, allow_redirects=True, headers=header).content
        soup = BeautifulSoup(response, 'html.parser')
        sleep(0.2)
        return soup

    def get_images(self):
        raise NotImplementedError

    def download(self):
        images = self.get_images()

        try:
            os.mkdir(self.name)
        except FileExistsError:
            pass
        print('======', self.name, '======')

        for index, image in enumerate(images):
            parsed = urlparse(image)
            filename = parsed.path.split('/')[-1]

            full_path = self.name + '/' + str(index), filename

            r = requests.get(image)
            with open(full_path, 'wb') as img_obj:
                img_obj.write(r.content)
                print(filename)

        sleep(2)

class SATW(Scraper):
    def get_thumbnail(self):
        thumbnails = []
        start = self.start

        for i in range(1, self.pages+1)[::-1]: # debug
            page = self.url + 'page' + str(i)
            print(page)

            soup = self.make_request(page)

            page_thumbnails = []
            for scrape in soup.find_all("div", class_="col-xs-6 col-sm-2"):
                thumbnail = [x.get("href") for x in scrape.find_all('a')]
                page_thumbnails.extend(thumbnail)

            page_thumbnails = page_thumbnails[::-1]
            # print(page_thumbnails)
            thumbnails.extend(page_thumbnails)

        return thumbnails[start:] # debug for range

    def get_images(self): # plus description
        thumbnails = self.get_thumbnail()

        images = []
        descriptions = []

        for i in thumbnails: # debug
            soup = self.make_request(i)

            # get comic url
            comic = [i.get('src') for i in soup.select('center > a > img')][1]
            print(comic)
            images.append(comic)

            # dump description to html
            description = [i for i in soup.find_all('div', class_='col-md-9')][0]
            descriptions.append(description)

        return images, descriptions

    def download(self):
        images, descriptions = self.get_images()

        try:
            os.mkdir(self.name)
        except FileExistsError:
            pass
        print('======', self.name, '======')

        for index, (image, description) in enumerate(zip(images, descriptions), self.start):
            parsed = urlparse(image)
            filename = parsed.path.split('/')[-1]

            full_path = self.name + '/' + str(index+1) + ' ' + filename

            r = requests.get(image)
            with open(full_path, 'wb') as img_obj:
                img_obj.write(r.content)
                print(index+1, filename)

            description_filename = full_path + '.html'
            with open(description_filename, 'w') as f:
                f.write(description.prettify())

        sleep(2)


def main(site):
    if site == 'satw':
        i = SATW('SATW', 'https://satwcomic.com/the-world/', 12, 1)
        i.download()


main('satw')
