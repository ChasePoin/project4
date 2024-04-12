from module_2 import ScrapersGettersSetters as SGS
from module_1 import GAI
import argparse as ap
from os.path import exists
import textwrap

### IMPORTANT: Make sure you are in the same current working directory as the folder containing the URLs and all of the downloaded files/folders. #######
## module 1 imports gemini related functionality. module 2 imports the scrapers, getters, writers ##
# run the file by typing python run.py x   x is your file containing the URLs you want to scrape + return a summary of; there is an example txt file included.
# if a RAW file is returned for your article but no processed file, there is potentially harmful content detected by the AI. There is an error testing line commented out in the sendAIprompt() function in GAI.py.


def argparser():
    parser=ap.ArgumentParser()
    parser.add_argument(help='Your file containing URLs', dest='file', type=str)
    arguments = parser.parse_args()
    file = arguments.file
    return file

def main():
    # URL getter gets all of the URLs from the file, passes in each individually to the scraper
    fileName = argparser()
    # make objects of scraper, writers, URL grabber, and make readable tool
    APscraper = SGS.APscraper()
    fileURLGetter = SGS.GetURLSTextFile()
    titleWriter = SGS.WriteTitle()
    articleWriter = SGS.WriteArticle()
    summaryWriter = SGS.WriteSummary()
    makeReadableForAI = GAI.MakeReadable()
    urls = fileURLGetter.getURLs(fileName)
    articleNumber = 1
    # this version now passes each URL individually instead of the whole file, so articleNumber is now passed in for error reporting
    for url in urls:
        APscraper.scrape(url, articleNumber)
        # RAW is original file format, with article title + article body
        # PROCESSED is new file format, with only the article body        
        rawFileName = APscraper.titleText + "_RAW.txt"
        rawFileName = rawFileName.replace(" ", "_")
        summaryFileName = APscraper.titleText + "_summary.txt"
        summaryFileName = summaryFileName.replace(" ", "_")

        # RAW:
        if (not exists("./Data/raw/" + rawFileName)):
            # handles writing raw data
            # RAW == ORIGINAL FORM OF WRITING
            rawFileToOutput = open("./Data/raw/" + rawFileName, "x")
            try:
                titleWriter.writeInfo(APscraper.titleText, rawFileToOutput, articleNumber)
                # writes the title to the file
            except:
                print(f"Failed to write title for article {articleNumber}.")
            
            try:
                articleWriter.writeInfo(APscraper.body, rawFileToOutput, articleNumber)
                # write article body to file
            except:
                print(f"Failed to write Article data for RAW, article {articleNumber}")

            print(f"RAW Article {articleNumber} file created successfully.")
        else:
            print(f"RAW Article {articleNumber} file already exists.")

        # SUMMARY:
        if (not exists("./Data/processed/" + summaryFileName)):
            # handles writing processed data
            ### PROCESSED IS NOW THE SUMMARIES ###
            fileToOutput = open("./Data/processed/" + summaryFileName, "x")

            try:
                model = GAI.configureAI()
                # sets up the AI, returns which model is being used
            except:
                print(f"Failed to set up the AI for article {articleNumber}")

            readableArticle = makeReadableForAI.makeArticleReadable(APscraper.body, articleNumber)
            # makes the article a giant string instead of an array; the AI does NOT like the array...
            readableTitle = makeReadableForAI.makeTitleReadable(APscraper.titleText, articleNumber)
            # makes the title properly formatted for the AI to read
            
            try:
                aiSummary = GAI.sendAIprompt(model, readableArticle, readableTitle)
                # sends the AI the prompt with the newly readable (converted to large strings) body and title and model of gemini being used
            except:
                print(f"Failed to send the AI the prompt for article {articleNumber}")

            try:
                summaryWriter.writeInfo(textwrap.fill(aiSummary.text, 100), fileToOutput, articleNumber)
                # writes gemini's returned summary text to file
            except:
                print(f"Failed to write the summary for article {articleNumber}")

            # the try except blocks do not fail the program but instead just fail on a per article basis
            print(f"PROCESSED Article {articleNumber} file created successfully.")
            fileToOutput.close()
        else:
            print(f"PROCESSED Article {articleNumber} file already exists.")

        articleNumber = articleNumber + 1

if __name__ == "__main__":
    main()
