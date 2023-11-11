import json

import requests as requests
from loguru import logger

from src.config.config import Config
from src.storage.db import DB

CONFIG: Config = Config()
CONFIG.load()

headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept': 'application/json, text/*'}


def get_refresh_token():
    """ Функция получения refresh токена """
    data = {
        'client_id': CONFIG.amo.integration_id,
        'client_secret': CONFIG.amo.secret_key,
        'grant_type': "authorization_code",
        'code': CONFIG.amo.authorization_code,
        'redirect_uri': CONFIG.amo.base_url
    }
    json_data = json.dumps(data)
    response = requests.post(url=f'{CONFIG.amo.base_url}/oauth2/access_token', data=json_data, headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()

        # Extract access_token and refresh_token from the parsed JSON
        refresh_token = result.get("refresh_token", "")
        db = DB()
        db.load()
        db.set_refresh_token(refresh_token)
        db.save()
        logger.info('Refresh token получен и сохранен')
    else:
        logger.warning(f"Error: Невозможно получить refresh токен. Status code: {response.status_code}")
        logger.warning(f"Error: {response.text}")


def get_access_token() -> str:
    """ Функция получения access_token'а для доступа к AmoCrm;
    По пути сохраняет refresh токен при каждом вызове"""
    db = DB()
    refresh_token = db.get_refresh_token()
    data = {
        "client_id": CONFIG.amo.integration_id,
        "client_secret": CONFIG.amo.secret_key,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": CONFIG.amo.base_url
    }
    response = requests.post(url=f'{CONFIG.amo.base_url}/oauth2/access_token', data=json.dumps(data), headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()

        # Extract access_token and refresh_token from the parsed JSON
        access_token = result.get("access_token", "")
        refresh_token = result.get("refresh_token", "")

        # Save the refresh token to the database
        db.set_refresh_token(refresh_token)

        # Return the obtained access token
        logger.info('Access token получен')
        db.save()
        return access_token
    else:
        # If the request was not successful, print an error message
        logger.warning(f"Error: Unable to obtain access token. Status code: {response.status_code}")
        logger.warning(f"Error: {response.text}")
        return ""


if __name__ == '__main__':
    get_refresh_token()
    logger.warning('Пробуем получить новый токен')
    logger.warning(get_access_token())
