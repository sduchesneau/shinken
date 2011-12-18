### Will be populated by the UI with it's own value
app = None

from shinken.webui.bottle import redirect
from shinken.modules.webui_broker.helper import hst_srv_sort
from shinken.util import safe_print
try:
    import json
except ImportError:
    # For old Python version, load
    # simple json (it can be hard json?! It's 2 functions guy!)
    try:
        import simplejson as json
    except ImportError:
        print "Error : you need the json or simplejson module"
        raise

# Get the div for each element
def get_div(elt):
    icon = app.helper.get_icon_state(elt)
    stars = ''
    for i in range(2, elt.business_impact):
        stars += '''<div class="criticity-inpb-icon-%d">
                  <img src="/static/images/star.png">
              </div>''' % (i-1)
    lnk = app.helper.get_link_dest(elt)
    button = app.helper.get_button('', img='/static/images/search.png')
    s = """
        %s
	<img style="width: 64px;height: 64px;" src="%s">
	<span class="state_%s">%s : %s</span>
	<div style="float:right;">
	<a href="%s">%s</a>
        """ % (stars, icon, elt.state.lower(), elt.state, elt.get_full_name(), lnk, button)
    s = s.encode('utf8', 'ignore')
    return s


# Our page
def get_page():
    # First we look for the user sid
    # so we bail out if it's a false one
    user = app.get_user_auth()

    if not user:
        redirect("/user/login")
    

    all_imp_impacts = app.datamgr.get_services()#important_elements()
    #all_imp_impacts.sort(hst_srv_sort)

    impacts = []
    for imp in all_imp_impacts:
        safe_print("FIND A BAD SERVICE IN IMPACTS", imp.get_dbg_name())
        d = {'name' : imp.get_full_name().encode('utf8', 'ignore'),
             "title": "My Image 3", "thumb": "/static/images/state_flapping.png", "zoom": "/static/images/state_flapping.png",
             "html" : get_div(imp)}
        impacts.append(d)
    
    # Got in json format
    #j_impacts = json.dumps(impacts)
#    print "Return impact in json", j_impacts

    return {'app' : app, 'user' : user, 'impacts' : impacts}


pages = {get_page : { 'routes' : ['/wall/'], 'view' : 'wall', 'static' : True}}

