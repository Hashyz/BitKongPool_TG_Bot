import datetime
import requests
from prettytable import PrettyTable
import re
from PIL import Image, ImageDraw, ImageFont
import io
# import matplotlib.pyplot as plt


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

    return f"Time Left : {int(time_left)} minutes"

  def getData(self, request, need, take=1, index=2):
    #get current pool start time
    res1 = self.req()
    try:
      startedAt = res1.json()['data']['leaderboard']['startedAt']
    except:
      startedAt = datetime.datetime.utcnow().isoformat()
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
  def SimpleTourTable(res1, need=10):
    data = []
    total = len(res1.json()['data']['leaderboard']['spots'])

    for i in range(need if total > need else total):
      wagered = res1.json()['data']['leaderboard']['spots'][i]['wagered']
      name = res1.json()['data']['leaderboard']['spots'][i]['user']['login']
      bonus = res1.json()['data']['leaderboard']['spots'][i]['bonus']
      data.append([name, wagered, bonus])

    table = PrettyTable()
    table.field_names = ["Name", "Wager", "Prize(Kong)"]
    for e, (nam, wgr, bns) in enumerate(data, start=1):
      table.add_row([nam, int(wgr), bns])
    return table
    # Create an image from the table
    # table_text = table.get_string()
    # table_image = Image.new("RGB", (800, 600), (255, 255, 255))
    # d = ImageDraw.Draw(table_image)
    # fnt = ImageFont.load_default()

    # d.text((10, 10), table_text, fill=(0, 0, 0), font=fnt)

    # # Save the image to a byte stream
    # img_byte_array = io.BytesIO()
    # table_image.save(img_byte_array, format='PNG')
    # img_byte_array.seek(0)

    # return img_byte_array
  @staticmethod
  def TourTable(res1, need=10):
    data = []
    total = len(res1.json()['data']['leaderboard']['spots'])

    for i in range(need if total > need else total):
      wagered = res1.json()['data']['leaderboard']['spots'][i]['wagered']
      name = res1.json()['data']['leaderboard']['spots'][i]['user']['login']
      bonus = res1.json()['data']['leaderboard']['spots'][i]['bonus']
      data.append([name, wagered, bonus])

    table = PrettyTable()
    table.field_names = ["No", "Name", "Wager", "Prize(Kong)"]
    for e, (nam, wgr, bns) in enumerate(data, start=1):
      table.add_row([e, nam, int(wgr), bns])
    # return table

    # font_path = "Roboto-Light.ttf"
    # # font_size = 16  # Adjust the font size as needed
    # font = ImageFont.truetype(font_path)

    # table_text = str(table)
    # text_width =  len(table_text.split("\n")[0])
    # text_height =  len(table_text.split("\n"))
    # # print(text_width,text_height)

    # # Create an image with a white background
    # im = Image.new("RGB", (text_width * 7, text_height * 15), "white")
    # draw = ImageDraw.Draw(im)
    # # font = ImageFont.truetype("FreeMono.ttf", 15)
    # # font = ImageFont.truetype("fonts/FreeMono.ttf", 15)

    # # Draw the table text on the image
    # draw.text((22, 1), table_text,font=font, fill="black")

    # # Save the image to a byte stream in PNG format
    # img_byte_array = io.BytesIO()
    # im.save(img_byte_array, format='PNG')
    # img_byte_array.seek(0)

    # return img_byte_array

    # Custom font and size
    # font_path = "Roboto-Light.ttf"
    font_size = 15
    # font = ImageFont.truetype(font_path, font_size)

    table_text = str(table)
    text_width = len(table_text.split("\n")[0])
    text_height = len(table_text.split("\n"))

    # Create an image with a white background
    im = Image.new("RGB", (text_width * 7, text_height * 15), "white")
    draw = ImageDraw.Draw(im)
    # Define the position for the table
    x, y = 21, 1
    # draw.text((22, 1), table_text,font=font, fill="black")

    # Split the table string into lines and draw each line with the custom font
    for line in table.get_formatted_string().splitlines():
      # print(line.split("|"))
      draw.text((x, y), line, fill="black", antialias=True)

      y += font_size  # Adjust for the font size

    # Save the image to a byte stream in PNG format
    img_byte_array = io.BytesIO()
    im.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    # Return the image
    return img_byte_array
