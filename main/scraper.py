import requests                 #send req to download the website to download th esource code
from bs4 import BeautifulSoup   #parses the html and get readable text from it.

#the block takes URL and performs the actions inside
def get_webpage_text(url):
    #try habdles errors like unnecessary waiting time, not valid link etc.
    try:
        #setting user helps to bypass restrictions like automated bots
        headers = {"User-Agent": "Mozilla/5.0"} #behaves as normal user, so that the websites that blocks bot ot automated requests, without any name.

        #res is an responsive object, it tells url is live or not responding
        res = requests.get(url, headers=headers, timeout=10) #reponse wait time while the program asks for code of the url
        if res.status_code != 200:  #status of any url, if 200 it is ok, if 400 not found, if 403 forbidden
            return None
        soup = BeautifulSoup(res.text, "html.parser") #parses the html extracted via res
        # Extract all text content
        for script in soup(["script", "style"]):  #removing styles and script tags from the html for cleaner look
            script.extract()
        text = soup.get_text(separator=" ") #seprate the words by a space, if they start with new line a space adde to the word
        return " ".join(text.split()) #removes ectra space, newlines, ensure linear spacing.
    
    #tuning a base class for common errors like timeout error, connection error
    #show the error message
    except Exception as e:
        print(f"Error: {e}")
        return None
