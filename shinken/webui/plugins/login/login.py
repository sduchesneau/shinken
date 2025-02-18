#!/usr/bin/env python
#Copyright (C) 2009-2011 :
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
#    Andreas Karfusehr, andreas@karfusehr.de
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

from shinken.webui.bottle import redirect

### Will be populated by the UI with it's own value
app = None

# Our page
def get_page():
    return user_login()


def user_login():
    user = app.get_user_auth()
    if user:
        redirect("/problems")

    err = app.request.GET.get('error', None)
    login_text = app.login_text

    return {'error': err, 'login_text' : login_text}


def user_login_redirect():
    redirect("/user/login")
    return {}


def user_logout():
    # To delete it, send the same, with different date
    user_name = app.request.get_cookie("user", secret=app.auth_secret)
    if user_name:
        app.response.set_cookie('user', False, secret=app.auth_secret, path='/')
    else:
        app.response.set_cookie('user', '', secret=app.auth_secret, path='/')
    redirect("/user/login")
    return {}


def user_auth():
    print "Got forms"
    login = app.request.forms.get('login', '')
    password = app.request.forms.get('password', '')
    is_auth = app.check_auth(login, password)

    if is_auth:
        app.response.set_cookie('user', login, secret=app.auth_secret, path='/')
        redirect("/problems")
    else:
        redirect("/user/login?error=Invalid user or Password")

    return {'app' : app, 'is_auth' : is_auth}


# manage the /. If the user is known, go to problems page.
# Should be /dashboad in the future. If not, go login :)
def get_root():
    user = app.request.get_cookie("user", secret=app.auth_secret)
    if user:
        redirect("/problems")
    else:
        redirect("/user/login")
        

pages = { user_login : { 'routes' : ['/user/login', '/user/login/'], 
                         'view' : 'login'},
          user_login_redirect : { 'routes' : ['/login'] },
          user_auth : { 'routes' : ['/user/auth'], 
                        'view' : 'auth', 
                        'method' : 'POST'},
          user_logout : { 'routes' : ['/user/logout', '/logout'] },
          get_root : {'routes' : ['/']},
          }

