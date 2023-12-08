from flask import Blueprint, flash, redirect, render_template, url_for
import requests

from webapp.weather.forms import CheckWeatherForm

from ..config import WEATHER_KEY


blueprint = Blueprint('weather', __name__, url_prefix='/weather')


def get_weather_by_city(city_name: str):
    """
    Функция получения погодных условий по API

    :param city_name: наименование города
    """
    weather_url = 'http://api.weatherstack.com/current'
    params = {
        'access_key': WEATHER_KEY,
        'query': city_name
    }
    try:
        api_result = requests.get(weather_url, params)
        api_result.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.Timeout:
        print(f"Timeout occurred for URL {weather_url}")
    except requests.ConnectionError:
        print(f"Connection error occurred for URL {weather_url}")
    except requests.TooManyRedirects:
        print(f"Too many redirects for URL {weather_url}")
    except requests.RequestException as error:
        print(f"An error occurred while fetching {weather_url}: {error}")

    try:
        api_response = api_result.json()
        location = api_response['request']['query']
        current_temp = api_response['current']['temperature']
        weather_descriptions = api_response['current']['weather_descriptions'][0]
        feelslike_temp = api_response['current']['feelslike']
    except (KeyError, AttributeError):
        location = 'Город указан неверно! Укажите другой.'
        current_temp = '-'
        weather_descriptions = '-'
        feelslike_temp = '-'

    return location, current_temp, weather_descriptions, feelslike_temp


@blueprint.route('/', methods=['GET'], defaults={'city_name': 'Москва'})
@blueprint.route('/<string:city_name>', methods=['GET'])
def show_weather(city_name: str):
    """
    Страница отображения погоды для города, указанного пользователем

    :param city_name: наименование города
    """
    title = 'Прогноз погоды'
    check_weather_form = CheckWeatherForm()
    weather_location = get_weather_by_city(city_name)

    return render_template(
        'weather/show_weather.html',
        page_title=title,
        check_weather_form=check_weather_form,
        city_name=city_name,
        location=weather_location[0],
        current_temp=weather_location[1],
        weather_descriptions=weather_location[2],
        feelslike_temp=weather_location[3]
    )


@blueprint.route('/search-weather', methods=['POST'])
def search_weather():
    """
    Процесс поиска погоды для города
    """
    check_weather_form = CheckWeatherForm()
    if check_weather_form.validate_on_submit():
        city_name = str(check_weather_form.city_name.data)
        print(city_name)
        if city_name != '':
            return redirect(url_for('weather.show_weather',
                                    city_name=city_name))

    return redirect(url_for('weather.show_weather'))
