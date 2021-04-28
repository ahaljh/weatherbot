import requests
import sys
import xml.etree.ElementTree as elemTree
from datetime import datetime, timezone, timedelta
from weather import Weather
from slack import Slack


def parse_kma_url(name, zone_id):
    BASE_URL = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone='
    req = requests.get(BASE_URL + zone_id)

    for _ in range(0, 2):  # 실패 시 1회 재시도
        if req.ok:
            tree = elemTree.fromstring(req.text)

            weather = Weather(name)

            for data in tree.findall('./channel/item/description/body/data'):
                day = int(data.find('day').text)

                if day == 0:
                    hour = int(data.find('hour').text)
                    temperature = float(data.find('temp').text)
                    wf_kor = data.find('wfKor').text
                    precipitation = int(data.find('pop').text)

                    from_hour = hour - 3
                    to_hour = hour

                    weather.add_forecast(from_hour, to_hour, wf_kor, temperature, precipitation)

            return weather
    else:
        print('Status code is NOT 200')
        return Weather(name)


if __name__ == '__main__':
    # https://www.weather.go.kr/weather/lifenindustry/sevice_rss.jsp # 동네 ID는 여기 참고

    town_info = {'덕풍1동': "4145054000", "정자1동": "4113555000"}

    towns = {'덕풍1동': 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4145054000',
             '정자1동': 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4113555000',
             }  # 이건 그냥 하드코딩으로 두자.

    print(sys.argv)
    print(len(sys.argv))
    for a in sys.argv:
        print(a)

    utc_now = datetime.now(timezone.utc)
    print(f'UTC: {utc_now}')

    KST = timezone(timedelta(hours=9))
    kst_now = utc_now.replace(tzinfo=KST)
    print(f'KST: {kst_now}')

    slack_webhook_url = sys.argv[1]
    slack_rainy_channel_name = sys.argv[2]
    slack_sunny_channel_name = sys.argv[3]

    # print('--------------------------------------')
    # print(slack_webhook_url, slack_channel_name)
    # print('--------------------------------------')

    rain_forecast = ''
    for town_name, zone_id in town_info.items():
        weather = parse_kma_url(town_name, zone_id)
        rain_forecast += weather.rain_forecasts()

    rain_forecasts = [parse_kma_url(town_name, zone_id).rain_forecasts() for town_name, zone_id in town_info.items()]
    rain_forecasts_str = '\n\n'.join(rf for rf in rain_forecasts if rf)

    slack = Slack(url=slack_webhook_url, channel=slack_sunny_channel_name, emoji=':sunny:', username='날씨 bot')
    if rain_forecasts_str:
        print(rain_forecasts_str)
        slack.send_message(f'*비 예보가 있습니다.* :umbrella: \n\n{rain_forecasts_str}', channel=slack_rainy_channel_name)
    else:
        print('비 예보가 없음')
        slack.send_message('비 예보가 없음 :sunny: ')
