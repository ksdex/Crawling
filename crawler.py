import logging
import re
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus):
        self.frontier = frontier
        self.corpus = corpus

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        count_dic = {}
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched,
                        len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    #baseURL = url_data['url']
                    #parse = urlparse(baseURL)
                    #if parse.netloc.lower() in count_dic:
                        #count_dic[parse.netloc.lower()] += 1
                    #else:
                        #count_dic[parse.netloc.lower()] = 1
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.add_url(next_link)
        # print('max subdomain is', max(count_dic, key=count_dic.get))

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        '''
        outputLinks = []
        # if url_data["content_type"].find("text") <= -1:
        # 'only calculate but no add into list'
        print(url_data['is_redirected'])
        print(url_data['final_url'])
        print(url_data['http_code'])
        if not url_data['is_redirected']:
            soup = BeautifulSoup(url_data['content'], "lxml")
            baseURL = url_data['url']
            if len(baseURL) < 500:
                print('baseURL:', baseURL)
                for link in soup.findAll('a'):
                    url = link.get('href')
                    print("----%s" % url)
                    if None != url:
                        url = urljoin(baseURL, url)
                        url = urldefrag(url)[0]
                    outputLinks.append(url)
        else:
            url = url_data['final_url']
            url = urldefrag(url)[0]
            outputLinks.append(url)
        return outputLinks

        '''
        outputLinks = []
        print(url_data['is_redirected'])
        print(url_data['final_url'])
        print(url_data['http_code'])
        soup = BeautifulSoup(url_data['content'], "lxml")
        baseURL = url_data['url']
        if len(baseURL) < 500:
            print('baseURL:', baseURL)

            parsed = urlparse(baseURL)
            log_dict = {"url": baseURL.strip().replace("'", "\'"), "subdomain": parsed.netloc.lower(),
                        "status": url_data['http_code'], "content_type": url_data['content_type'],
                        "meet_time": 0, "is_return": 0}

            for link in soup.findAll('a'):
                url = link.get('href')
                print("----%s" % url)
                if url is not None:
                    url = urljoin(baseURL, url)
                    url = urldefrag(url)[0]
                    outputLinks.append(url)
                    print('addurl', url)

        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """

        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        '''
        Sam: what I changed from here
             I think I have already excluded the calender from the crawling but need more test
             to see if it is all right
        '''
        archive_pat = "archive.ics.uci.edu"
        if re.match(archive_pat, parsed.netloc.lower()):
            return False
        if len(url) > 500:
            return False
        today = r"^today\.uci\.edu$"
        calender = r"^\/department\/information_computer_sciences\/calendar(\/|\?)?((.)+)?$"
        if re.match(today, parsed.netloc.lower()):
            if re.match(calender, parsed.path.lower()):
                return False

        '''
        Sam: what I changed end here
        '''

        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print("TypeError for ", parsed)
            return False
