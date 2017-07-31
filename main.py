#Code Written by @Cosm00_
#Stay Based Youngins....
#@COPTHATCREP TOLD ME TO DO IT FOR THE CULTURE. NOT REALLY BUT BITCH IM BASED GOD I WRITE WHAT I WANT. FUCK BITCHES GET KAIOKEN X10.

from classes.logger import logger
from bs4 import BeautifulSoup as bs
import requests, time

log = logger().log

class alldayidreamaboutsleeping:
    def __init__(self, region, sleeptime):
        self.s = requests.Session()
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        self.baseurl = 'http://www.adidas.com/static/on/demandware.static/-/Sites-CustomerFileStore/default/adidas-REGIONUPPER/en_REGIONUPPER/sitemaps/product/adidas-REGIONUPPER-en-REGIONLOWER-product.xml'
        self.region = region.upper()
        self.sleeptime = float(sleeptime)
        self.foundlist = []
        self.sitekey = ''

    def sitemap(self):
        url = self.baseurl
        url = url.replace('REGIONUPPER', self.region)
        url = url.replace('REGIONLOWER', self.region.lower())

        if self.region == 'US':
            url = 'http://www.adidas.com/on/demandware.static/-/Sites-CustomerFileStore/default/adidas-US/en_US/sitemaps/product/adidas-US-en-us-product.xml'
        elif self.region == 'GB':
            url = url.replace('.com', '.co.uk')
        elif self.region == 'AU':
            url = url.replace('.com', '.com.au')
        else:
            url = url.replace('.com', '.' + region.lower())
            url = url.replace('en-' + region.lower(), region.lower() + '-' + region.lower())
            url = url.replace('en_' + region, region.lower() + '_' + region)
            log(url, 'cyan')

        while True:
            res = self.s.get(url)
            if 'UNFORTUNATELY WE ARE UNABLE TO GIVE YOU ACCESS TO OUR SITE AT THIS TIME' not in res.text.upper():
                break
            else:
                log('BANNED, WAITING 5 MINUTES', 'red')
                time.sleep(300)

        soup = bs(res.text, 'lxml')

        length = len(soup.find_all('xhtml:link'))
        count = 1

        for item in soup.find_all('xhtml:link'):
            log('Searching Item : {}/{}'.format(str(count), str(length)), 'cyan')
            crawlurl = item['href'].replace('m.adidas','www.adidas')
            time.sleep(self.sleeptime)

            while True:
                try:
                    res = self.s.get(crawlurl, timeout = 5)
                    if 'UNFORTUNATELY WE ARE UNABLE TO GIVE YOU ACCESS TO OUR SITE AT THIS TIME' not in res.text.upper():
                        break
                    else:
                        log('BANNED, WAITING 5 MINUTES', 'red')
                        time.sleep(300)
                except:
                    pass

            try:
                new = bs(res.text, 'lxml')
            except:
                log('TIMED-OUT OF LINK : {}'.format(item['href']), 'red')
                pass

            try:
                sitekey = new.find('div', {'class':'g-recaptcha'})['data-sitekey']
                self.sitekey = str(sitekey)
                self.foundlist.append(str(crawlurl))
                log('Sitekey Found', 'green')
                log('URL : ' + crawlurl, 'green')
                log('Sitekey : ' + sitekey, 'green')
            except:
                pass

            count = count + 1
            
    def done(self):
        log('Sitekey = {}'.format(self.sitekey), 'rain')
        log('Found Key on Sites : ', 'green')
        for item in self.foundlist:
            log(item, 'green')


delay = log('Enter Delay Between Crawls (Typically 5) : ', 'input')
region = log('Enter Region to Search (EG: US, AU, GB) : ', 'input')

s = alldayidreamaboutsleeping(region, delay)
s.sitemap()
s.done()
