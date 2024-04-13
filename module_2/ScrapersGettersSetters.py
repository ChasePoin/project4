from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

# The idea behind this module was to take the pre-existing scrape function and make it a subclass of a superclass named Scrapers(), making Scrapers() a template
# for future scrapers to be made, and for the APscraper to simply be one of many subclass scrapers if the functionality were ever to be needed.
# each scraper would have an __init__ function so when an object is created it creates objects of each getter from the imported module. There is no limit
# on the amount of getters and writers, you just simply have to implement the functionality of what you want to get and what you want to write

# each scraper's scrape() should only take a raw URL to scrape. scrape() returns nothing, but is responsible for making sure each file is output properly
# each info getter expects the soup (the beautifulsoup parsed html)

# In this version, the URLGrabber superclass and related subclass are moved to this module, as I felt they better suited this module than the other now. There is also now a WriteSummary() class to write the 
# AI generated summary to file.

class Scrapers(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def scrape(self, url: str, articleNum: int) -> None:
        pass

class InfoGetters(ABC):
    @abstractmethod
    def getInfo(self, soup) -> str:
        pass

class InfoWriters(ABC):
    @abstractmethod
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        pass

class URLGrabber(ABC):
    @abstractmethod
    def getURLs(self, source) -> str:
        pass

class APscraper(Scrapers):
    def __init__(self):
        self.titleGetter = GetTitle()
        self.articleGetter = GetArticle() 
   
    def scrape(self, url: str, articleNumber: int) -> None:
        "Pass the url wanted to be scraped."    
        # article number will be used for error reporting
        try:
            html = requests.get(url, headers={"Connection": "keep-alive", "User-agent": "Mozilla/5.0"})
        except:
            print("Failure to request web data for article " + str(articleNumber) + ".")
        
        soup = BeautifulSoup(html.content, "lxml")
        # requests sends a request for the data from the web server
        # BeautifulSoup parses and allows the particular data we want to be pulled easily

        try:
            self.titleText = self.titleGetter.getInfo(soup)
            # calls getTitle() to, well, get the title
        except:
            print(f"Failed to get title for article {articleNumber}.")

        try:
            self.body = self.articleGetter.getInfo(soup)
        except:
            print(f"Failed to get Article for RAW, article {articleNumber}")

class GetURLSTextFile(URLGrabber):
    # using a file
    def getURLs(self, source) -> str:
        # information is the file to open
        try:   
            urls = open(source, "r")
            return urls
        except:
            print("Failure to open file containing URLs.")
            exit()
        # open URL file

class GetTitle(InfoGetters):
    def getInfo(self, soup) -> str:
        # gets title from <h1> tags, makes it pretty, encoding it into ascii and decoding it back to a string in order to remove
        # unicode characters from appearing as "question marks," returns the title
        try:
            title = soup.find('h1', class_='Page-headline').text
            encodedTitle = title.encode('ascii', 'ignore')
            titleText = encodedTitle.decode()
        except:
            # sets title to an empty string and outputs warning
            titleText = ""
            print("Title text unable to be scraped.")
        return titleText

class WriteTitle(InfoWriters):
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        formattedTitle = "Title: " + information + "\n"
        # formats the title to write it using unformatted title text (information)
        try:
            fileToOutput.write(formattedTitle)
            # writes the beautiful title to the file
        except:
            print(f"Failed to write title for article {currentArticle}.")
    
class GetArticle(InfoGetters):
    def getInfo(self, soup) -> str:
        try:
            # gets actual article text from <p> tags, find_all() puts it into an array
            body = soup.find_all('p')
        except:
            # sets body content to empty string then outputs error message/warning
            body = ""
            print("Body unable to be scraped.")
        return body

class WriteArticle(InfoWriters):
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        # loops through newly created array, makes it pretty, encoding it into ascii and decoding it back to a string in order to remove unicode
        # does not return anything and instead writes each part of the array to the file
        count = 0
        try:
            fullText = ""
            for partsOfArticle in information:
            # "count" is present in order to not print out the copyright at the beginning 
                if count == 1:        
                    encodeParts = partsOfArticle.text.encode('ascii', 'ignore')
                    # this gets rid of the "question marks" by encoding the file in ascii characters
                    fullText = fullText + encodeParts.decode() + "\n"
                    # writes the article data to the file and decodes it in order to make it a string
                count = 1
            fileToOutput.write((fullText))
        except:
            print(f"Failed to write body information for article {currentArticle}")

class WriteSummary(InfoWriters):
    # used to write the AI's summary to file
    def writeInfo(self, information, fileToOutput, currentArticle) -> None:
        try:
            # AI summary is just one giant response.text, so you can write it in one go
            fileToOutput.write(information)
        except:
            print(f"Failed to write AI summary to file for article {currentArticle}")
