import logging

from .scoresaber import ScoreSaber
from .scoresaber_provider import ScoreSaberProvider
from .errors import *
from .models import *

handler = logging.StreamHandler()
logging.getLogger("PyScoreSaber").addHandler(handler)
