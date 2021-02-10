import requests
import sys
import xml.etree.ElementTree as elemTree
from weather import Weather
from slack import Slack


def parse_kma_url(name, url):
    req = requests.get(url)

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
    towns = {'덕풍1동': 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4145054000',
             '정자1동': 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=4113555000',
             }  # 이건 그냥 하드코딩으로 두자.

    print(sys.argv)
    print(len(sys.argv))
    for a in sys.argv:
        print(a)

    slack_webhook_url = sys.argv[1]
    slack_channel_name = sys.argv[2]

    # print('--------------------------------------')
    # print(slack_webhook_url, slack_channel_name)
    # print('--------------------------------------')

    for town_name, town_url in towns.items():
        weather = parse_kma_url(town_name, town_url)

        slack = Slack(url=slack_webhook_url, channel=slack_channel_name, emoji=':sunny:', username='날씨 bot')

        rain_forecast = weather.rain_forecasts()
        if (rain_forecast != ''):
            print(rain_forecast)
            slack.send_message(f'*비 예보가 있습니다.* :umbrella: \n\n{rain_forecast}')
        else:
            print('비 예보가 없음')
            slack.send_message('비 예보가 없음 :sunny: ')
