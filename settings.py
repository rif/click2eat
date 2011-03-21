# -*- coding: utf-8 -*-
import socket
if socket.gethostname() in ('grace', 'love', 'cocostar', 'joy', 'Virgils-Mac-Pro-4.local', 'kubu'):
    from settings_dev import *
else:
    from settings_prod import *

