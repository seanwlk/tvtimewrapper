# TVTime Wrapper

Simple class that allows the usage of TVTime via script with "API like" data returns. Note that this is not an official library and it works by webscraping the site.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install tvtimewrapper
```

## Usage

```python
from tvtimewrapper import TVTimeWrapper

tvtime = TVTimeWrapper("username","password")
```
### Methods

- toWatch()

```python
tvtime.toWatch() # Returns "Watch next" part of the website as list of dicts
# Example output:
[
  {
    "name":"Last Week Tonight with John Oliver",
    "poster":"https://dg31sz3gwrwan.cloudfront.net/poster/278518/1012307-4-optimized.jpg",
    "episode_link":"/en/show/278518/episode/7694963",
    "season":"07",
    "episode":"13",
    "series_id":"278518",
    "episode_id":"7694963",
    "remaining":0
  }
]
```
- notWatchedForAWhile()
```python
tvtime.notWatchedForAWhile() # Returns "Not watched for a while" part of the website as list of dicts
# Example output:
[
  {
    "name":"Big Little Lies",
    "poster":"https://dg31sz3gwrwan.cloudfront.net/poster/305719/1179542-4-optimized.jpg",
    "episode_link":"/en/show/305719/episode/7219153",
    "season":"02",
    "episode":"02",
    "series_id":"305719",
    "episode_id":"7219153",
    "remaining":"5"
  },
  {
    "name":"Elite",
    "poster":"https://dg31sz3gwrwan.cloudfront.net/poster/346328/1312784-4-optimized.jpg",
    "episode_link":"/en/show/346328/episode/7268881",
    "season":"02",
    "episode":"01",
    "series_id":"346328",
    "episode_id":"7268881",
    "remaining":"15"
  },
  {
    "name":"Altered Carbon",
    "poster":"https://dg31sz3gwrwan.cloudfront.net/poster/332331/1262768-4-optimized.jpg",
    "episode_link":"/en/show/332331/episode/7550513",
    "season":"02",
    "episode":"01",
    "series_id":"332331",
    "episode_id":"7550513",
    "remaining":"7"
  }
]
```
- notStartedYet()
```python
tvtime.notStartedYet() # Returns "Not started yet" part of the website as list of dicts
# Example output:
[
  {
    "name":"Lost in Space (2018)",
    "poster":"https://dg31sz3gwrwan.cloudfront.net/poster/343253/62105950-4-optimized.jpg",
    "episode_link":"/en/show/343253/episode/6564318",
    "season":"01",
    "episode":"01",
    "series_id":"343253",
    "episode_id":"6564318",
    "remaining":"19"
  }
]
```
- markWatched(episode_id)

With this method you can set an episode as watched. The episode ID is available from toWatch() method. Note that TVTime uses the IDs from TVDB.
```python
tvtime.markWatched(7694963) # Returns actual http response from server
```
- react(episode_id,reaction)

With this method you can react to an episode given the ID and the reaction type from the ones available from the site. (good,fun,wow,sad,so-so,bad)
```python
tvtime.react(7694963,"good") # Returns actual http response from server
```
- comment(episode_id,comment)

With this method you can comment on an episode given the ID.
```python
tvtime.comment(7694963,"Interesting episode") # Returns actual http response from server
```
- voteActor(episode_id,actor_id)

With this method you can vote an actor from the episode watched.
```python
tvtime.voteActor(7694963,64832777) # Returns actual http response from server
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv2](https://choosealicense.com/licenses/gpl-2.0/)