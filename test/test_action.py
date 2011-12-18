#!/usr/bin/env python
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

#It's ugly I know....
from shinken_test import *
from shinken.action import Action

time.time = original_time_time
time.sleep = original_time_sleep

class TestAction(ShinkenTest):
    #setUp is in shinken_test

    def wait_finished(self, a):
        for i in xrange(1, 100000):
            if a.status == 'launched':
                a.check_finished(8012)
                time.sleep(0.01)

    #Change ME :)
    def test_action(self):
        a = Action()
        a.timeout = 10
        a.env = {}

        if os.name == 'nt':
            a.command = r'libexec\\dummy_command.cmd'
        else:
            a.command = "libexec/dummy_command.sh"
        self.assert_(a.got_shell_characters() == False)
        a.execute()
        self.assert_(a.status == 'launched')
        #Give also the max output we want for the command
        self.wait_finished(a)
        self.assert_(a.exit_status == 0)
        self.assert_(a.status == 'done')
        self.assert_(a.output == "Hi, I'm for testing only. Please do not use me directly, really")
        self.assert_(a.perf_data == "Hip=99% Bob=34mm")


    def test_environnement_variables(self):
        a = Action()
        a.timeout = 10
        if os.name == 'nt':
            return
        else:
            a.command = "/usr/bin/env"
        a.env = {'TITI' : 'est en vacance'}

        self.assert_(a.got_shell_characters() == False)

        a.execute()

        self.assert_(a.status == 'launched')
        #Give also the max output we want for the command
        self.wait_finished(a)
        print "Output", a.long_output, a.output
        titi_found = False
        for l in a.long_output.splitlines():
            if l == 'TITI=est en vacance':
                titi_found = True

        self.assert_(titi_found == True)
        

    #Some commands are shell without bangs! (like in Centreon...)
    #We can show it in the launch, and it should be managed
    def test_noshell_bang_command(self):
        a = Action()
        a.timeout = 10
        a.command = "libexec/dummy_command_nobang.sh"
        a.env = {}
        if os.name == 'nt':
            return
        self.assert_(a.got_shell_characters() == False)
        a.execute()

        self.assert_(a.status == 'launched')
        self.wait_finished(a)
        print "FUck", a.status, a.output
        self.assert_(a.exit_status == 0)
        self.assert_(a.status == 'done')


    def test_got_shell_characters(self):
        a = Action()
        a.timeout = 10
        a.command = "libexec/dummy_command_nobang.sh && echo finished ok"
        a.env = {}
        if os.name == 'nt':
            return
        self.assert_(a.got_shell_characters() == True)
        a.execute()

        self.assert_(a.status == 'launched')
        self.wait_finished(a)
        print "FUck", a.status, a.output
        self.assert_(a.exit_status == 0)
        self.assert_(a.status == 'done')


    def test_got_pipe_shell_characters(self):
        a = Action()
        a.timeout = 10
        a.command = "libexec/dummy_command_nobang.sh | grep 'Please do not use me directly'"
        a.env = {}
        if os.name == 'nt':
            return
        self.assert_(a.got_shell_characters() == True)
        a.execute()

        self.assert_(a.status == 'launched')
        self.wait_finished(a)
        print "FUck", a.status, a.output
        self.assert_(a.exit_status == 0)
        self.assert_(a.status == 'done')


if __name__ == '__main__':
    import sys
   
#    os.chdir(os.path.dirname(sys.argv[0]))
    unittest.main()

