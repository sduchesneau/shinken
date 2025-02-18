#!/usr/bin/env python
#Copyright (C) 2009-2010 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
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


#DBMysql is a MySQL access database class
from shinken.db import DB

import MySQLdb
from MySQLdb import IntegrityError
from MySQLdb import ProgrammingError


class DBMysql(DB):
    def __init__(self, host, user, password, database, character_set, table_prefix = ''):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.character_set = character_set
        self.table_prefix = table_prefix


    #Create the database connection
    #TODO : finish (begin :) ) error catch and conf parameters...
    def connect_database(self):
        #self.db = MySQLdb.connect (host = "localhost", user = "root", passwd = "root", db = "merlin")
        self.db = MySQLdb.connect (host = self.host, user = self.user, \
                                       passwd = self.password, db = self.database)
        self.db.set_character_set(self.character_set)
        self.db_cursor = self.db.cursor ()
        self.db_cursor.execute('SET NAMES %s;' % self.character_set)
        self.db_cursor.execute('SET CHARACTER SET %s;' % self.character_set)
        self.db_cursor.execute('SET character_set_connection=%s;' % self.character_set)
        #Thanks http://www.dasprids.de/blog/2007/12/17/python-mysqldb-and-utf-8 for utf8 code :)


    #Just run the query
    #TODO: finish catch
    def execute_query(self, query):
        #print "[MysqlDB]I run query", query, "\n"
        try:
            self.db_cursor.execute(query)
            self.db.commit()
        except IntegrityError , exp:
            print "[MysqlDB] Warning : a query raise an integrity error : %s, %s" % (query, exp)
        except ProgrammingError , exp:
            print "[MysqlDB] Warning : a query raise a programming error : %s, %s" % (query, exp)
