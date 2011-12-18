#!/usr/bin/python
#Copyright (C) 2009 Gabes Jean, naparuba@gmail.com
#
#This file is part of Shinken.
#
#Shinken is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Shinken is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Shinken.  If not, see <http://www.gnu.org/licenses/>.


properties = {
    'daemons' : ['broker'],
    'type' : 'webui',
    'phases' : ['running'],
    'external' : True,
    }


# called by the plugin manager to get an instance
def get_instance(plugin):
    print "Get a WebUI instancefor plugin %s" % plugin.get_name()

    #First try to import
    try:
        from webui_broker import Webui_broker
    except ImportError , exp:
        print "Warning : the plugin type %s is unavalable : %s" % ('webui', exp)
        return None

    instance = Webui_broker(plugin)
    return instance
