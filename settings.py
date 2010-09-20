# -*- coding: utf-8 -*-
import socket
if socket.gethostname() in ('grace', 'love', 'cocostar', 'old-mac', 'Virgils-Mac-Pro-4.local'):
    from settings_dev import *
else:
    from settings_prod import *

