import os
import time
from hashlib import sha256

def setup():
    t = time.localtime()
    s = f'{t.tm_year}{t.tm_mon}{t.tm_mday}{t.tm_hour}{t.tm_min}'
    os.environ['AuthCICE'] = sha256(s.encode()).hexdigest()
