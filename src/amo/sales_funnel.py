import requests
from loguru import logger

from src.amo.auth import get_access_token
from src.config.config import Config


class SalesFunnel:
    def __init__(self):
        self.header = {
            'Content-Type': 'application/json; charset=UTF-8',
            # 'Accept': 'application/json, text/*',
        }
        self.upd_access()
        config: Config = Config()
        config.load()
        self.base_url = config.amo.base_url

    def upd_access(self):
        access_token = get_access_token()
        self.header['Authorization'] = f'Bearer {access_token}'
        logger.info('Access token updated.')

    def get_pipelines(self):
        url = f'{self.base_url}/api/v4/leads/pipelines'
        response = requests.get(url=url, headers=self.header)
        if response.status_code == 401:
            logger.warning('Access token expired. Updating...')
            self.upd_access()
            response = requests.get(url=url, headers=self.header)
        if response.status_code != 200:
            logger.warning(f'Error: {response.status_code}')
            # logger.warning(f'Error: {response.text}')

        return response.json()

    def get_events(self):
        url = f'{self.base_url}/api/v4/events'
        params = {'filter[type]': 'lead_status_changed'}
        # request with param filer
        # url = f'{self.base_url}/api/v4/events?filter[entity][type]=leads&filter[entity][id]=1'
        response = requests.get(url=url, headers=self.header, params=params)
        if response.status_code == 401:
            logger.warning('Access token expired. Updating...')
            self.upd_access()
            response = requests.get(url=url, headers=self.header)
        if response.status_code != 200:
            logger.warning(f'Error: {response.status_code}')
            # logger.warning(f'Error: {response.text}')
        return response.json()


if __name__ == '__main__':
    sf = SalesFunnel()
    # print(sf.get_pipelines())
    print(sf.get_events())
