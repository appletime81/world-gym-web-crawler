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
    "Cookie": "_gcl_au=1.1.1250621335.1667355528; _gaexp=GAX1.2.VVimaachSRmZP5jWfNP7ug.19375.1; _gid=GA1.2.243658949.1667355528; __lt__cid=74b9a463-b6b1-49b6-9c3c-27491f7cbd58; __lt__sid=87c38079-3ce59805; _fbp=fb.1.1667355528677.2011227152; gaconnector_GA_Client_ID=1741022972.1667355528; gaconnector_pages_visited_list=/locations-schedule/taipei-station; gaconnector_gclid=; gaconnector_fc_source=(direct); gaconnector_lc_source=(direct); gaconnector_fc_medium=(none); gaconnector_lc_medium=(none); gaconnector_fc_campaign=(direct); gaconnector_lc_campaign=(direct); gaconnector_fc_term=(not set); gaconnector_lc_term=(not set); gaconnector_fc_content=(not set); gaconnector_lc_content=(not set); gaconnector_fc_landing=https://www.worldgymtaiwan.com/locations-schedule/taipei-station; gaconnector_lc_landing=https://www.worldgymtaiwan.com/locations-schedule/taipei-station; gaconnector_fc_referrer=(not set); gaconnector_lc_referrer=(not set); gaconnector_fc_channel=Direct; gaconnector_lc_channel=Direct; gaconnector_ip_address=-; gaconnector_OS=Windows 10; gaconnector_device=desktop; gaconnector_browser=Chrome 106.0.0.0; gaconnector_city=New Taipei; gaconnector_country=Taiwan; gaconnector_country_code=TW; gaconnector_region=New Taipei; gaconnector_time_zone=Asia/Taipei; gaconnector_latitude=25.0504; gaconnector_longitude=121.5324; _ga=GA1.1.1741022972.1667355528; gaconnector_page_visits=10; gaconnector_all_traffic_sources=(direct)/(none), (direct)/(none), (direct)/(none), (direct)/(none), (direct)/(none), (direct)/(none), (direct)/(none), (direct)/(none), (direct)/(none), (direct)/(none); __atuvc=10|44; __atuvs=6361d388ba2668c0009; gaconnector_time_passed=2846373; _ga_JYDVKLW8PC=GS1.1.1667355528.1.1.1667359020.60.0.0; _ga_2E6H95K0WT=GS1.1.1667355528.1.1.1667359020.0.0.0; XSRF-TOKEN=eyJpdiI6ImphdjVQSktGR0h2U3BocTJOQ3NcL25RPT0iLCJ2YWx1ZSI6InhzbmZmUkJ4WXBxR2trMDl1UHc2VmVvZkgyWG9sT1o2cTN1WVZ2V3lVeXE3bGVSajNYRWR2bnV0TWJvXC9peU5vIiwibWFjIjoiMDNmYWEwZjgzMjg3ZGExNjQxOThjMmZkZDg1MDk5ZGExNmUwZjc4ZTJhY2FlY2RiMjc0ZTM0NGRmZWE5ZTk0NiJ9; laravel_session=eyJpdiI6IjBmQjRVYzdObFdwQ2VhRGlOWDFmTVE9PSIsInZhbHVlIjoiNFc1SjRVWFBWNldYZksyOTVvUEhHRWxcL1FmRTZmeVhvbGIwMThoTEo4UGtld0RiWDA3dHdRMlJlaiswYXBaU1EiLCJtYWMiOiIwNTFiZDg3NzE0ZjFhY2NkYWU2OTM1ZWI0NjZjM2Y1MjI3NzkxMzIzYWFiOGNkNTRmZWFkNTc1Y2I4ZDdhOTI1In0=",
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
    "X-CSRF-TOKEN": "OMKzxyFwxgHuueM9DEwXvVp1uGyTivEQwr3eZrdw",
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
        print("-" * 30 + day + "-" * 300)
        for class_time, class_name, class_instructor in zip(
                class_times, class_names, class_instructor
        ):
            print(
                f"課程名稱:{class_time.text}, 時間:{class_time.text}, 教練:{class_instructor.text}"
            )
            print("-" * 50)


if __name__ == "__main__":
    get_week_class_table()
