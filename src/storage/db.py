from pathlib import Path

from loguru import logger

from src.config.config import Config


class DB:
    def __init__(self):
        config = Config()
        config.load()
        self.file_name = Path(__file__).parent / config.database.file_name
        self.refresh_token = ''

        self.load()

    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token

    def get_refresh_token(self):
        return self.refresh_token

    def save(self):
        with open(self.file_name, 'w') as file:
            file.write(self.refresh_token)
            logger.info('Refresh token saved to file.')

    def load(self):
        try:
            with open(self.file_name, 'r') as file:
                self.refresh_token = file.read()
                logger.info('Refresh token loaded from file.')
        except FileNotFoundError:
            # If the file doesn't exist, create an empty one.
            with open(self.file_name, 'w'):
                pass
            logger.warning('File not found. A new file has been created.')
        except Exception as e:
            logger.warning(f"An error occurred while loading the file: {e}")


if __name__ == '__main__':
    db = DB()
    # db.set_refresh_token('refresh_token')
    logger.warning(f'Токен прочитан: {db.get_refresh_token()}')
    db.save()
