# AP News Web Scraper
This is a demonstration of the usage of an LLM API, Gemini API, using the web scraper that this is branched off of.
There are two modules that feed into run.py; GAI contains gemini AI related functions, such as sending the prompt and making the article readable by the AI.
This version now has more detailed test cases.

This branch also contains an updated version of the python environment used, as the LLM API requires a package to be imported. Be sure to use this version of the environment (the requirements.yml file in this branch).
## Information:

-Module 1 contains a file named GAI.py. This file contains two functions and a class with two methods. The two functions are configureAI() and sendAIprompt(). The first of these two sets up the gemini API with the gemini-pro model, while sendAIprompt() is responsible for taking the article text and article title and sending the summary prompt to gemini.

-Module 2 contains four superclasses: Scrapers(), InfoWriters(), InfoGetters(), URLGrabbers(). These were made with the intention of it being very easy to add new information writers and getters, scrapers, and new ways to get URLs while leaving the past ones alone. These are utilized within main() in run.py; the getters are used within the APscraper() function in module 2, while the writers are used within the run.py. This was set up this way with the idea that the scraper would get whatever getters are put inside the function and store it within the object, while it is up to the user to write what they want using the run.py main().

-run.py is responsible for looping and writing now, freeing up the rest of the classes to fulfill a single responsibility. Having run.py handle the writing makes it so you can write whatever you want instead of the scrape() function being overloaded with too much.

-run.py uses an argparser. To run the program simply type python run.py x with x being the name of the file containing your URLs. There is an example URL file titled "news_urls.txt." Feel free to use this as an example of how each processed and raw file turns out (under data) compared to their actual article. You can also just delete the URLs contained in this file and place your own, it works the exact same as creating your own. Just make sure you type the name properly when running the program.

-Data contains two different folders: raw and processed. Raw is the original version of the data format, with there being a title and the article body. Processed contains the gemini-generated summary of each of the articles.

-Test cases and their implementation can be found in the "Issues" tab above. Specifically, they're all listed in the "TEST CASES IMPLEMENTATION" thread. 

## API Key
An extremely important "key" to this project is the necessity of an API key to use this program. The API key is an access token to access their API. It is relatively simply to do this.

1. Go to https://ai.google.dev/tutorials/python_quickstart. If you do not have a google account, create one now.

2. Scroll to the "Setup your API key" section. Click on "Get an API key."

3. Generate your API key and copy it to clipboard. You will then need to store the API key into an environment variable. Open your CMD and type set GOOGLE_API_KEY=ctrl+v. It is important the name is GOOGLE_API_KEY, as this is what the AI setup function uses to find your API Key environment variable; if you want to use a different name for this environment variable, change the name in the configureAI() function's os.getenv() function call. 

4. To make sure it properly set, type echo %GOOGLE_API_KEY%. It should return your API key.

5. Type this same command in the CMD in visual studio code, just to make sure. If for some reason it doesn't echo the key back, just type set GOOGLE_API_KEY=ctr+v (as long as the key is still copied) in the cmd in vsc as well.

## To use this version of the scraper:
This assumes you have an python environment management system such as conda (recommended, as this is what was used to test) and visual studio code installed. There are plenty of guides on the internet on how to install these.

1. Download the zip from this repo by pressing the green code button and then "Download zip." Unpack this zip to your folder of choice.

2. Open your cmd and navigate the working directory to the folder you unpacked the zip to. (Example: cd .. takes you back a directory and cd "folder" will take you to the folder directory. Just look at your file explorer and move your cmd directory in accordance with each folder you see.)

3. This is where you will create your python environment; you will create this new environment based off the requirements.yml file. To do this in conda, type "conda env create -f requirements.yml." By default the name of this environment will be project1. If you want the environment to be a different name edit the "name" (first line) of the requirements.yml file. If you are using a different environment manager find the command to make a new environment based off a yml/yaml file.

4. Open the folder you extracted your zip file to in visual studio code.

5. Now press ctrl + shift + p to open the command palette and type in "python: select interpreter." Select the option with the corresponding name; a list will appear. Choose the option with the name of the environment you just created.

6. Take the URLs you want to scrape and either make a new text file and order the URLs as you want (look at news_urls.txt for formatting) or just replace the URLs in news_urls.txt with the ones you want to scrape.

7. Make sure your terminal in VSC is in the folder with your text file. Also make sure none of the files were split up.

8. Be sure to have read the above guide on how to setup your API Key. Type echo %GOOGLE_API_KEY% to make sure the key is configured properly. The key is CRUCIAL for this program to run properly.

9. The way to run the program has changed. It now uses an argparser. Repeating this because it is super important: to run the program, make sure your CWD is in the folder downloaded from this; all of the folder accesses are relative, so you need to be in the folder downloladed. Then type in the CMD/terminal "python run.py x" with x being the name of the file containing your URLs to be scraped.

10. Check the data folders for the raw and processed files; the raw folder will contain the old format, with the title and article body. The processed folder will contain the files with the gemini generated summary.
