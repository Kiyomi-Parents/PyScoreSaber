import logging

from .scoresaber import ScoreSaber
from .errors import *
from .models import *

handler = logging.StreamHandler()
logging.getLogger("PyScoreSaber").addHandler(handler)
