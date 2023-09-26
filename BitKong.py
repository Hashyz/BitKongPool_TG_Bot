import datetime
import requests
from prettytable import PrettyTable
import re


class BitKongAPI:

  def __init__(self) -> None:
    pass

  # @staticmethod
  def req(self,
          current_time=datetime.datetime.utcnow().isoformat() + 'Z',
          take=1,
          index=2):

    url = "https://api.playhub.io:443/graphql"
    headers = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Sec-Ch-Ua":
        "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Authorization": "Bearer null",
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "X-Client-Id": "KgtAfV",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Origin": "https://bitkong.com",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://bitkong.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,my;q=0.8,id;q=0.7"
    }

    json = {
        "operationName": "getLeaderboardData",
        "query":
        "query getLeaderboardData($kind: LeaderboardKind, $id: ID, $take: Int, $locale: String! = \"en\", $date: DateTimeOffset, $index: Int) {\n  viewer {\n    ...LeaderboardSpotUser\n    __typename\n  }\n  leaderboard(kind: $kind, id: $id, date: $date, index: $index) {\n    next {\n      id\n      __typename\n    }\n    previous {\n      id\n      __typename\n    }\n    amount\n    lockedAmount\n    currency {\n      id\n      __typename\n    }\n    isCurrent\n    startedAt\n    endAt\n    kind\n    viewerSpot {\n      ...LeaderboardSpot\n      __typename\n    }\n    spots(take: $take) {\n      ...LeaderboardSpot\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment LeaderboardSpot on LeaderboardSpot {\n  spot\n  points\n  bonus\n  lockedBonus\n  currency {\n    id\n    __typename\n  }\n  wagered\n  wageredCurrency {\n    id\n    __typename\n  }\n  user {\n    ...LeaderboardSpotUser\n    __typename\n  }\n  __typename\n}\n\nfragment LeaderboardSpotUser on User {\n  id\n  login\n  badge\n  profile {\n    avatarId\n    __typename\n  }\n  betting {\n    level {\n      id\n      rank {\n        id\n        nameId\n        name(locale: $locale)\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n",
        "variables": {
            "date": current_time,  #"2023-09-14T06:35:09.839Z",
            "index": index,
            "kind": "HOURLY",
            "locale": "en",
            "take": take
        }
    }  #take maean position
    try:
      res1 = requests.post(url, headers=headers, json=json, timeout=5)
    except:
      return self.req(take=1, index=2)
    return res1

  # @staticmethod
  def timeLeft(self):
    # Define the starting time
    # startedAt = "2023-09-26T05:00:00+00:00"
    res1 = self.req()
    # print(res1)
    startedAt = res1.json()['data']['leaderboard']['startedAt']

    # Extract the ISO datetime without the timezone information
    iso_pattern = re.compile(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})")
    start_datetime_str = iso_pattern.search(startedAt).group(0)

    # Calculate the time difference
    time_difference = datetime.datetime.utcnow(
    ) - datetime.datetime.fromisoformat(start_datetime_str)

    # Calculate the time left out of 60 minutes
    time_left = max(60 - (time_difference.total_seconds() / 60), 0)

    return f"💸 {int(time_left)} minutes left out of 60 minutes."

  def getData(self, request, need, take=1, index=2):
    #get current pool start time
    res1 = self.req()
    startedAt = res1.json()['data']['leaderboard']['startedAt']
    # print(startedAt)
    # timeLef = BitKongAPI.timeLeft(startedAt)

    result_datetime = datetime.datetime.fromisoformat(startedAt) - (
        datetime.timedelta(hours=1) * need)

    result_datetime_str = result_datetime.isoformat()

    res2 = BitKongAPI().req(current_time=result_datetime_str,
                            take=take,
                            index=index)
    respondInjsn = res2.json()['data']['leaderboard']
    # print(res2.json())
    return {"respondInjsn": respondInjsn, "need": need, "respond": res2}

  @staticmethod
  def TourTable(res1, need=10):
    data = []
    total = len(res1.json()['data']['leaderboard']['spots'])

    for i in range(need if total > need else total):
      wagered = res1.json()['data']['leaderboard']['spots'][i]['wagered']
      name = res1.json()['data']['leaderboard']['spots'][i]['user']['login']
      data.append([name, wagered])

    table = PrettyTable()
    table.field_names = ["Pos", "Name", "Wager"]
    for e, (element, count) in enumerate(data, start=1):
      table.add_row([e, element, count])
    return table
