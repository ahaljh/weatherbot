import requests

DEFAULT_SLACK_EMOJI = ':sunny:'
DEFAULT_SLACK_USERNAME = '날씨bot'


class Slack:
    """slack에 message를 보내기 위해 만든 Class"""
    def __init__(self, url, channel, emoji=DEFAULT_SLACK_EMOJI, username=DEFAULT_SLACK_USERNAME):
        self.url = url
        self.channel = channel
        self.emoji = emoji
        self.username = username

    def send_message(self, text, channel='', url='', emoji='', username=''):
        """Slack에 Webhook 방식으로 메시지를 전송합니다."""
        payload = {'text': text}

        payload['channel'] = self.channel if channel == '' else channel
        payload['icon_emoji'] = self.emoji if emoji == '' else emoji
        payload['username'] = self.username if username == '' else username

        requests.post(url if url != '' else self.url,
                      json=payload
                      )
