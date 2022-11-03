import datetime
import requests
from bs4 import BeautifulSoup

# cookie、X-CSRF-TOKEN 必要時，自行更動
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "78",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_gcl_au=1.1.571205612.1667446544; _gaexp=GAX1.2.VVimaachSRmZP5jWfNP7ug.19375.0; _gid=GA1.2.1356438039.1667446544; _gat_UA-52977744-1=1; __lt__cid=f57c6065-48c8-48bd-b96d-a5d2a7fcdcfa; __lt__sid=50ba2e90-b9110992; _gat_gtag_UA_132963325_17=1; gaconnector_GA_Client_ID=120203662.1667446544; gaconnector_pages_visited_list=/locations-schedule/taipei-station; _fbp=fb.1.1667446544902.477217732; gaconnector_gclid=; gaconnector_fc_source=(direct); gaconnector_lc_source=(direct); gaconnector_fc_medium=(none); gaconnector_lc_medium=(none); gaconnector_fc_campaign=(direct); gaconnector_lc_campaign=(direct); gaconnector_fc_term=(not set); gaconnector_lc_term=(not set); gaconnector_fc_content=(not set); gaconnector_lc_content=(not set); gaconnector_fc_landing=https://www.worldgymtaiwan.com/locations-schedule/taipei-station; gaconnector_lc_landing=https://www.worldgymtaiwan.com/locations-schedule/taipei-station; gaconnector_fc_referrer=(not set); gaconnector_lc_referrer=(not set); gaconnector_fc_channel=Direct; gaconnector_lc_channel=Direct; gaconnector_ip_address=-; gaconnector_OS=Linux x86_64; gaconnector_device=desktop; gaconnector_browser=Chrome 106.0.0.0; gaconnector_city=New Taipei; gaconnector_country=Taiwan; gaconnector_country_code=TW; gaconnector_region=New Taipei; gaconnector_time_zone=Asia/Taipei; gaconnector_latitude=25.0504; gaconnector_longitude=121.5324; _ga=GA1.1.120203662.1667446544; gaconnector_page_visits=2; gaconnector_all_traffic_sources=(direct)/(none), (direct)/(none); __atuvc=2|44; __atuvs=636337103fa26ec0001; gaconnector_time_passed=38004; _ga_JYDVKLW8PC=GS1.1.1667446544.1.1.1667446584.20.0.0; _ga_2E6H95K0WT=GS1.1.1667446544.1.1.1667446584.0.0.0; XSRF-TOKEN=eyJpdiI6InBBaE1YRHdtdnlJWEF0U20rZUNWYkE9PSIsInZhbHVlIjoiTnlyak5lOFkzam94cHJFcG4wSE80UHAzMEZBWUxHK2NjV05qWVhadktsdkEzUkZubitFOWN4eDN2cERpYlcxYiIsIm1hYyI6Ijk5YzMzMzFjNWQ1NTBmMzFkOWM3NTgwMWVmZTM0NDZhYzMzNjk5MWNhZmY1Y2IwM2YwZDY2NzE2ZThjMTJkY2EifQ==; laravel_session=eyJpdiI6ImtVWm1XdldzMjJTd280TUZzaUdnQWc9PSIsInZhbHVlIjoiT2ZseUo2eDhrYmprMHREMFwvbUhXUW5PVjBVeTl0Kzl1dnBYNGdNNUFDWEhya2VZWGIxNTN4Rk9zUUZYRlhTMEIiLCJtYWMiOiI4OTBiZWFmMzEzMzNmNjFiZWI4NzkzNDhhYTQ2YjcxNzEwMzc4NTk3YmZmYzc1OGI4NTVmMTQxYTg1M2Q4OTYwIn0=",
    "Host": "www.worldgymtaiwan.com",
    "Origin": "https://www.worldgymtaiwan.com",
    "Referer": "https://www.worldgymtaiwan.com/locations-schedule/taipei-station",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "X-CSRF-TOKEN": "MHQqUj5RovzUsVwMAKosknuqDytZlr7cvprn8epw",
}

data = {
    "vType": "Store",
    "vCategory": "",
    "vClass": "",
    "vTeacher": "",
    "vKeyword": "",
    "vSID": "taipei-station",
    "vWeek": "0",  # 0 for this week, 1 for next week, -1 for last week, 依此類推
}

url = "https://www.worldgymtaiwan.com/getStoreClass"

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

week_dates = [datetime.date.today() + datetime.timedelta(days=i) for i in
              range(int(data.get("vWeek")) * 7 - datetime.date.today().weekday(), 7 - datetime.date.today().weekday())]
week_dates_str = [date.strftime("%Y-%m-%d") for date in week_dates][:7]


def get_week_class_table():
    # Get the data from the website
    print(week_dates_str)
    html = requests.post(url, headers=headers, data=data).content
    soup = BeautifulSoup(html, "lxml")
    for day in days:
        table = soup.find(attrs={"data-weekday": day})
        class_times = table.find_all("div", class_="class-time")
        class_names = table.find_all("div", class_="class-name")
        class_instructor = table.find_all("div", class_="class-instructor")
        print("-" * 50 + day + "-" * 50)
        for class_time, class_name, class_instructor in zip(
                class_times, class_names, class_instructor
        ):
            print(
                f"課程名稱:{class_time.text}, 時間:{class_time.text}, 教練:{class_instructor.text}"
            )
            print("-" * 50)


if __name__ == "__main__":
    get_week_class_table()
