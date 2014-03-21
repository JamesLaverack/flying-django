from google.appengine.api import users

def user_data(request):
    u = users.get_current_user()
    if u:
        return {'logged_in': True, 'username': u.nickname(), 'url': users.create_logout_url("/"), 'user_id': u.user_id()}
    else:
        return {'logged_in': False, 'url': users.create_login_url("/")}
