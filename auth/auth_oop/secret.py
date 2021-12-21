import os
import random
from datetime import datetime
from hashlib import sha256

def setup():
    random.seed(datetime.now().date().isoformat())
    os.environ['AuthCICE'] = sha256(str(random.random()).encode()).hexdigest()
