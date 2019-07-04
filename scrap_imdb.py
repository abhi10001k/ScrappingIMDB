# -*- coding: utf-8 -*-
"""Scrap_IMDB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u8VMD8-0ba1jfWexdDG7oYA3GyBkkQTG
"""

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
# print(len(castlist))
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
print(moviesList[0])