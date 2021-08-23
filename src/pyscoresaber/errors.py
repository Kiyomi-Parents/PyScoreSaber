class ScoreSaberException(Exception):
    def __init__(self, status: int, url: str) -> None:
        self.status = status
        self.url = url

        super().__init__(f"Score Saber returned {self.status} for {self.url}")


class NotFoundException(ScoreSaberException):
    pass


class ServerException(ScoreSaberException):
    pass
