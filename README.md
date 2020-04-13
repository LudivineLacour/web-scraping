# Doctolib web-scrapping
 
The objective of this project is to get a database of all existing doctors in France, for any kind of speciality to make analysis on Medicine in France.

Doctolib website gives access to doctors on the platform & those who are around a location but not subscribed.

Others information are available such as: availabilit, languages, prices, 
 
 ## Process
 
 [Flowchart to come]
 
 Tools and ways of working: I made several exploration on the data retrieved from the scrapping on a jupyter notebook (exploration.pynb). Then I created a python script with functions to run the scraping and automatically savong
 
 ## Python concepts used in the web-scrapping
 
 Librairies used:
 - pandas
 - re
 - time
 - datetime
 - requests
 - bs4 (BeautifulSoup)
 - pymysql
 - sqlalchemy
 
 Concepts used:
 - `.json_normalize()` to transform the json into a dataframe
 - html and css selection with `BeautifulSoup()`
 - `.to_sql()` with the `if_exists='append'` argument to save the data after each speciality was scraped

 
 ## Results
 
 #1 A database containing a `doctors` table with all doctors names, address, speciality, if they propose TeleHealth consultation
 
 #2 A dataframe with the next availability for a list of doctors based on location and speciality
 
 ## Challenges
 
 - Scraping taking too much time: I changed the way to save data to my database by sending data scraped after each speciality and append it in the database instead of saving the data at the end of the scraping
 - Can't know the number of results for a search based on a location and a speciality
 - Many cases to handle: Need to test on several random specialities to get has many use case as possible
 
 ## Lesson learned
 
 - How to deal with scalability: go step-by-step when scraping by making sure data is regularly saved and requests based on human volume
 
 ## Possible improvements
 
 - Enriched the database location using the Address API provided by the gouvernment (https://geo.api.gouv.fr/adresse)
 - Improve scraping time by doing scraping with search url based on region location


