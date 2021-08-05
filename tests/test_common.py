import unittest

from src.pyscoresaber import common, NotFoundException, RateLimitedException, ServerErrorException
from src.pyscoresaber.common import Common


class TestCommon(unittest.TestCase):
    class FakeResponse:
        def __init__(self, url, status_code):
            self.url = url
            self.status_code = status_code

    @staticmethod
    def fake_request(url, status_code):
        return TestCommon.FakeResponse(url, status_code)

    def setUp(self):
        common.WAIT_RATE_LIMIT = 0
        common.WAIT_SERVER_ERROR = 0

    def test_request_200(self):
        url = "https://httpstat.us/200"
        status_code = 200

        response = common.Common.request(self.fake_request, url, status_code)

        assert response.url == url
        assert response.status_code == status_code

    def test_request_404(self):
        with self.assertRaises(NotFoundException):
            Common.request(self.fake_request, "https://httpstat.us/404", 404)

    def test_request_429(self):
        with self.assertRaises(RateLimitedException):
            Common.request(self.fake_request, "https://httpstat.us/429", 429)

    def test_request_500(self):
        with self.assertRaises(ServerErrorException):
            Common.request(self.fake_request, "https://httpstat.us/500", 500)
