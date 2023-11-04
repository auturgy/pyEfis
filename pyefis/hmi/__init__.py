#  Copyright (c) 2018 Phil Birkelbach
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import logging

from . import actionclass
from pyefis.hmi import functions
from . import keys
from . import data

actions = None
from . import menu
from . import buttonmenu

def initialize(config):
    global actions
    log = logging.getLogger(__name__)
    log.info("Initializing Actions")
    actions = actionclass.ActionClass()

    if "databindings" in config:
        data.initialize(config["databindings"])
