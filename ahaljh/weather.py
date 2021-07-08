class Weather:
    """
    날씨 예보 모음
    """

    forecasts = []

    class Forecast:
        """
        시간대별 날씨 예보
        """

        def __init__(self, from_hour, to_hour, wf_kor, temperature, precipitation) -> None:
            self.from_hour = from_hour
            self.to_hour = to_hour
            self.wf_kor = wf_kor
            self.temperature = temperature
            self.precipitation = precipitation

        def __str__(self):
            return f'[{self.from_hour}시~{self.to_hour}시]온도:{self.temperature}, 날씨:{self.wf_kor}, 강수확률:{self.precipitation}%'

        def will_rain(self):
            return self.precipitation >= 50

    def add_forecast(self, from_hour, to_hour, wf_kor, temperature, precipitation) -> None:
        self.forecasts.append(self.Forecast(from_hour, to_hour, wf_kor, temperature, precipitation))

    def __init__(self, town) -> None:
        self.town = town

    def _make_forecast_str(self, forecasts: list):
        return '>\n>'.join(str(fc) for fc in forecasts)

    def __str__(self):
        return self._make_forecast_str(self.forecasts)

    def forecast(self):
        return f'>*[{self.town}] 일기예보* \n>\n>' + self._make_forecast_str(self.forecasts)

    def rain_forecasts(self):
        str_rain_forecasts = self._make_forecast_str(fc for fc in self.forecasts if fc.will_rain())
        return f'>*[{self.town}] 일기예보* \n>\n>' + str_rain_forecasts if str_rain_forecasts else ''
