#!/usr/bin/env python2.6
#Copyright (C) 2009-2010 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
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


#
# This file is used to test reading and processing of config files
#

import os

from shinken_test import unittest, ShinkenTest

from shinken.log import logger
from shinken.objects.module import Module
from shinken.modules import ip_tag_arbiter
from shinken.modules.ip_tag_arbiter import get_instance 



class TestIpTag(ShinkenTest):
    #setUp is in shinken_test
    def setUp(self):
        self.setup_with_file('etc/nagios_module_ip_tag.cfg')


    #Change ME :)
    def test_hack_cmd_poller_tag(self):
        modconf = self.conf.modules.find_by_name('IpTag')

        # look for a objects that use it
        h1 = self.sched.hosts.find_by_name("test_host_0")
        h2 = self.sched.hosts.find_by_name("test_router_0")

        #get our modules
        mod = get_instance(modconf)
        # Look if we really change our commands

        # Ok we lie a bit, in the early phase, we should NOT
        # already got poller_tag properties. Must lie here
        # and find a better way to manage this in tests
        del h2.poller_tag
        
        # Calls the mod with our config
        mod.hook_early_configuration(self)
        

        print "H1", h1.poller_tag
        self.assert_(h1.poller_tag == 'None')

        print"H2", h2.poller_tag
        self.assert_(h2.poller_tag == 'DMZ')
        self.assert_(h2.check_command.poller_tag == 'DMZ')


    #Change ME :)
    def test_hack_cmd_poller_tag(self):
        modconf = self.conf.modules.find_by_name('IpTagAppend')

        # look for a objects that use it
        h1 = self.sched.hosts.find_by_name("test_host_0")
        h2 = self.sched.hosts.find_by_name("test_router_0")

        #get our modules
        mod = get_instance(modconf)
        # Look if we really change our commands

        # Ok we lie a bit, in the early phase, we should NOT
        # already got poller_tag properties. Must lie here
        # and find a better way to manage this in tests
        h1.hostgroups = 'linux,windows'
        h2.hostgroups = 'linux,windows'
        
        # Calls the mod with our config
        mod.hook_early_configuration(self)
        

        print "H1", h1.hostgroups
        self.assert_('newgroup' not in h1.hostgroups)

        print"H2", h2.hostgroups
        self.assert_('newgroup' in h2.hostgroups)
        

if __name__ == '__main__':
    unittest.main()

