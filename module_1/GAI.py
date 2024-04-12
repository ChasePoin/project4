from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import google.generativeai as gemai
import os


### IMPORTANT: Make sure you are in the same working directory as your file containing the URLs you want to scrape.

# This file is now responsible for functionality regarding sending a prompt to Gemini. class MakeReadable() has two functions related to making the article readable for the prompt, while configureAI()
# sets up the AI and sendAIprompt(model, articleText, articleTitle) sends the AI the prompt with the properly formatted article text and title so that it is readable.
            
def configureAI():
    # uses key from environment variable labeled "GOOGLE_API_KEY"
    # configures the gemini api
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    gemai.configure(api_key=GOOGLE_API_KEY)
    # modelToUse = 'gemini-pro'
    model = gemai.GenerativeModel('gemini-pro')
    return model

def sendAIprompt(model, articleText, articleTitle):
    # passes in the articleText, then sends the prompt to the AI, returning the AI's response
    prompt = "Please create a 50 word or less summary of this article. The title of the article is " + articleTitle + ". Please put the title above the article summary, labeling it as the title. Here is the article text to summarize: "
    response = model.generate_content(prompt + articleText) 
    # print(response.prompt_feedback) # potential error reporting; USE THIS IF YOUR ARTICLE RETURNS SOMETHING FOR RAW BUT NOT FOR SUMMARY/PROCESSED
    # IF THE PROBABILITY FOR ANY CATEGORY OF HARM IS MEDIUM OR ABOVE, THE AI WILL NOT CREATE A SUMMARY FOR YOUR ARTICLE
    return response

class MakeReadable():
    def makeArticleReadable(self, articleText, currentArticle):
        # new to this version of the project, makes the article readable by gemini by putting it into a large string instead of an array
        count = 0
        try:
            fullText = ""
            for partsOfArticle in articleText:
            # "count" is present in order to not print out the copyright at the beginning 
                if count == 1:        
                    encodeParts = partsOfArticle.text.encode('ascii', 'ignore')
                    # this gets rid of the "question marks" by encoding the file in ascii characters
                    fullText = fullText + encodeParts.decode() + "\n"
                    # writes the article data to the file and decodes it in order to make it a string
                count = 1
        except:
                print(f"Failed to condense body information for article {currentArticle}")

        return str(fullText)
    
    def makeTitleReadable(self, articleTitle, currentArticle):
        try:
            # encodes, decodes, then makes it a string
            readableTitle = articleTitle.encode('ascii', 'ignore')
            readableTitle = readableTitle.decode() + "\n"
            readableTitle = str(readableTitle)
        except:
            print(f"Failed to make title readable for article {currentArticle}")     

        return readableTitle
