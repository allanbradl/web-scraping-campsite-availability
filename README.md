# web-scraping-campsite-avialability
This python program runs every 30 mins (user input) to check for the availability of campsites at a particular campground (under heavy demand) and emails the user the availability within a specific duration. It uses Python's selenium module to scrape the recreation.gov website and uses a .bat file to schedule the repeated run for the python code in windows.

try1_log.txt contains the log of the availability of the campsites, if any, during each run of the code. 

Selenium module and the chrome driver extension are required to run the program without opening an on-screen window on the google chrome browser.

Note: The campsite link on recreation.gov, dates of interest, and the target campsite numbers (#) may be modified according to the location.
