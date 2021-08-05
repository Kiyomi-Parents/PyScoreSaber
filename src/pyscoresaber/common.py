import logging
import time

from .errors import RateLimitedException, NotFoundException, ServerErrorException

WAIT_RATE_LIMIT = 60
WAIT_SERVER_ERROR = 5


class Common:

    @staticmethod
    def request(method, *args, **kwargs):
        def attempt():
            response = method(*args, **kwargs)
            Common.verify_response(response)
            return response

        return Common.request_attempt(attempt)

    @staticmethod
    def verify_response(response):
        if response.status_code == 429:
            raise RateLimitedException(response)

        if 400 <= response.status_code < 500:
            raise NotFoundException(response)

        if 500 <= response.status_code < 600:
            raise ServerErrorException(response)

    @staticmethod
    def request_attempt(func):
        attempt = 0
        attempting = True
        last_exception = None

        while attempting and attempt < 6:
            try:
                result = func()

                attempting = False
                return result
            except ServerErrorException as error:
                attempt += 1
                logging.info(str(error))
                logging.info(f"Waiting {WAIT_SERVER_ERROR} seconds...")
                last_exception = error
                time.sleep(WAIT_SERVER_ERROR)
            except RateLimitedException as error:
                attempt += 1
                logging.info(str(error))
                logging.info(f"Waiting {WAIT_RATE_LIMIT} seconds...")
                last_exception = error
                time.sleep(WAIT_RATE_LIMIT)

        if last_exception is not None:
            raise last_exception
