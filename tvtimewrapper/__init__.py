import requests
import json
import re
from bs4 import BeautifulSoup

class TVTimeWrapper:
  """
  TO-DO
  - fetch series info by ID
  - fix language
  """
  def __init__(self,username,password,lang="en"):
    self.session = requests.Session()
    self.lang = lang
    self.h = {
      "Referer": f"https://www.tvtime.com/{lang}",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }
    self.session.post(f"https://www.tvtime.com/signin?username={username}&password={password}",
      data={"username": username,
            "password": password,
            "redirect_path": f"https://www.tvtime.com/{self.lang}/to-watch"},
      headers=self.h)
  def _getSeriesEpisodeID(self,data):
    data = data.split("/")
    for index,d in enumerate(data):
      if d == "show":
        show = data[index+1]
      elif d == "episode":
        episode = data[index+1]
    return {"show":show,"episode":episode}
  def _getRemainingEp(self,data):
    try:
      remaining = data.find("h2").find("span", class_="nb-remainging-episodes").text
      return re.sub("[^0-9]", "", remaining)
    except:
      return 0
  def toWatch(self):
    toScrape = self.session.get(f"https://www.tvtime.com/{self.lang}/to-watch",headers=self.h)
    soup = BeautifulSoup(toScrape.text, 'html.parser')
    sections = soup.find_all(id="to-watch")
    dataToReturn = []
    for s in sections:
      sectionTitle = s.find("h1")
      if "Watch next" in sectionTitle.text:
        seriesList = s.find_all("li")
        for series in seriesList:
          if series.text != "": # Ignore empty <li> tags, could do a lambda on find_all <li>
            poster = series.find("img")
            details = series.find("div",class_="episode-details")
            episode = details.find("h2").find("a")
            name = details.find("a",class_="nb-reviews-link secondary-link").text
            dataToAppend = {
              'name' : name,
              'poster' : poster['src'],
              'episode_link' : episode['href'],
              'season' : episode.text.split("E")[0].replace("S",""),
              'episode' : episode.text.split("E")[-1],
              'series_id' :  self._getSeriesEpisodeID(episode['href'])['show'],
              'episode_id' : self._getSeriesEpisodeID(episode['href'])['episode'],
              'remaining' : self._getRemainingEp(details)
            }
            dataToReturn.append(dataToAppend)
    return dataToReturn
  def notWatchedForAWhile(self):
    toScrape = self.session.get(f"https://www.tvtime.com/{self.lang}/to-watch",headers=self.h)
    soup = BeautifulSoup(toScrape.text, 'html.parser')
    sections = soup.find_all(id="to-watch")
    dataToReturn = []
    for s in sections:
      sectionTitle = s.find("h1")
      if "Not watched for a while" in sectionTitle.text:
        seriesList = s.find_all("li")
        for series in seriesList:
          if series.text != "": # Ignore empty <li> tags, could do a lambda on find_all <li>
            poster = series.find("img")
            details = series.find("div",class_="episode-details")
            episode = details.find("h2").find("a")
            name = details.find("a",class_="nb-reviews-link secondary-link").text
            dataToAppend = {
              'name' : name,
              'poster' : poster['src'],
              'episode_link' : episode['href'],
              'season' : episode.text.split("E")[0].replace("S",""),
              'episode' : episode.text.split("E")[-1],
              'series_id' :  self._getSeriesEpisodeID(episode['href'])['show'],
              'episode_id' : self._getSeriesEpisodeID(episode['href'])['episode'],
              'remaining' : self._getRemainingEp(details)
            }
            dataToReturn.append(dataToAppend)
    return dataToReturn
  def notStartedYet(self):
    toScrape = self.session.get(f"https://www.tvtime.com/{self.lang}/to-watch",headers=self.h)
    soup = BeautifulSoup(toScrape.text, 'html.parser')
    sections = soup.find_all(id="to-watch")
    dataToReturn = []
    for s in sections:
      sectionTitle = s.find("h1")
      if "Not started yet" in sectionTitle.text:
        seriesList = s.find_all("li")
        for series in seriesList:
          if series.text != "": # Ignore empty <li> tags, could do a lambda on find_all <li>
            poster = series.find("img")
            details = series.find("div",class_="episode-details")
            episode = details.find("h2").find("a")
            name = details.find("a",class_="nb-reviews-link secondary-link").text
            dataToAppend = {
              'name' : name,
              'poster' : poster['src'],
              'episode_link' : episode['href'],
              'season' : episode.text.split("E")[0].replace("S",""),
              'episode' : episode.text.split("E")[-1],
              'series_id' :  self._getSeriesEpisodeID(episode['href'])['show'],
              'episode_id' : self._getSeriesEpisodeID(episode['href'])['episode'],
              'remaining' : self._getRemainingEp(details)
            }
            dataToReturn.append(dataToAppend)
    return dataToReturn
  def markWatched(self,episode_id):
    r = self.session.put("https://www.tvtime.com/watched_episodes",data={"episode_id": episode_id},headers=self.h).json()
    if ("result" in r) and (r['result'] == "OK"):
      return r
    else:
      return {"result" : "error"}
  def react(self,episode_id,reaction):
    reactions = {
      "good" : 1,
      "fun" : 2,
      "wow" : 3,
      "sad" : 4,
      "so-so" : 6,
      "bad" : 7
    }
    try:
      emotion_id = reactions[reaction.lower()]
    except:
      return {"result" : "error","error" : "Reaction requested not available"}
    r = self.session.post("https://www.tvtime.com/emotions",data={"episode_id": episode_id, "emotion_id": emotion_id},headers=self.h).json()
    if ("result" in r) and (r['result'] == "OK"):
      return r
    else:
      return {"result" : "error"}
  def comment(self,episode_id,comment):
    data = {
      "comment": comment,
      "shareOnFacebook": 0,
      "shareOnTwitter": 0,
      "episode_id": episode_id
    }
    r = self.session.post("https://www.tvtime.com/comments",data=data,headers=self.h).json()
    if ("result" in r) and (r['result'] == "OK"):
      return r
    else:
      return {"result" : "error"}
  def voteActor(self,episode_id,actor_id):
    r = self.session.post("https://www.tvtime.com/vote_for_actor",data={"episode_id": episode_id, "actor_id": actor_id},headers=self.h).json()
    if ("result" in r) and (r['result'] == "OK"):
      return r
    else:
      return {"result" : "error"}