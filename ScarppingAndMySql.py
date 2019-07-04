import requests
from bs4 import BeautifulSoup

page_link = "https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc"
page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")

"""**Fecting Movies Name**"""

l = page_content.find_all("h3")
movies = []
for i in range(50):
  movies.append(l[i].find_all("a")[0].text)

"""**Fetching Movies Year**"""

year = []
for i in range(50):
  year.append(l[i].find_all("span",{"class","lister-item-year"})[0].text[1:-1])
year = [int(each) for each in year]

"""**Fetching Movies Ratings**"""

lrating = page_content.find_all("div",{"class":"ratings-imdb-rating"})
ratings = []
for i in range(50):
  ratings.append(lrating[i].text[2:-1])

"""**Fetching Movies Cast**"""

castlist = page_content.find_all("div",{"class":"lister-item-content"})
cast = []
for i in range(50):
  l = castlist[i].find_all("p",{"class":""})[0].text.split("\n")
  l = [each.strip() for each in l]
  member = []
  for x in reversed(l):
    if(x == "Stars:"):
      break
    member.append(x)
  member = member[1:]
  member = [each.strip(",") for each in member]
  cast.append(member)
# cast

"""**Fetching Movies Directors**"""

castlist = page_content.find_all("div",{"class":"lister-item-content"})
directors = []
for i in range(50):
  directors.append(castlist[i].find_all("p",{"class":""})[0].a.text)
# directors

"""**Final List of Movies**"""

moviesList = []
for i in range(50):
    moviesList.append({"Id":i+1,"Name":movies[i],"Year":year[i],"Rating":ratings[i],"Director":directors[i],"Stars":cast[i]})
# moviesList

import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "abhi10001k",
	auth_plugin = "mysql_native_password",
	database="IMDB"
)

# print(mydb)

mycursor = mydb.cursor()

# Created Movies Table 
sql_cmd = "CREATE TABLE Movies_Data(MovieId int NOT NULL,MoviesName varchar(255) NOT NULL,Rating float,Year int,PRIMARY KEY(MovieId))"
mycursor.execute(sql_cmd)

# Created Table for Directors
sql_cmd = "CREATE TABLE Directors(MovieId int NOT NULL,FirstName varchar(255),LastName varchar(255),PRIMARY KEY(MovieId))"
mycursor.execute(sql_cmd)

# Created Table for Cast/Stars
sql_cmd = "CREATE TABLE Stars(MovieId int NOT NULL,FirstName varchar(255),LastName varchar(255))"
mycursor.execute(sql_cmd)

mydb.commit()


# filling Movies_Data Table
placeholders = ', '.join(['%s'] * 4)
columns = ', '.join(["MovieId","MoviesName","Rating","Year"])
sql_cmd = "INSERT INTO Movies_Data(%s) VALUES( %s )" %(columns,placeholders)
for i in range(50):
	mycursor.execute(sql_cmd,[moviesList[i]["Id"],moviesList[i]["Name"],moviesList[i]["Rating"],moviesList[i]["Year"]])

# filling Director Table
placeholders = ', '.join(['%s'] *3)
columns = ', '.join(["MovieId","FirstName","LastName"])
sql_cmd = "INSERT INTO Directors(%s) VALUES( %s )" %(columns,placeholders)
for i in range(50):
	splitName = moviesList[i]["Director"].split()
	mycursor.execute(sql_cmd,[moviesList[i]["Id"],splitName[0],splitName[-1]])

# filling Stars Table
placeholders = ', '.join(['%s'] *3)
columns = ', '.join(["MovieId","FirstName","LastName"])
sql_cmd = "INSERT INTO Stars(%s) VALUES( %s )" %(columns,placeholders)
for i in range(50):
	for x in moviesList[i]["Stars"]:
		splitName = x.split()
		mycursor.execute(sql_cmd,[moviesList[i]["Id"],splitName[0],splitName[-1]])
		
mydb.commit()

