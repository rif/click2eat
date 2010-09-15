# -*- coding: utf-8 -*-
import socket
if socket.gethostname() in ('grace', 'love', 'cocostar', 'old-mac'):
    from settings_dev import *
else:
    from settings_prod import *

