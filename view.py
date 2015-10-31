from flask import Flask, render_template, request, redirect
from vkappauth.vk_app_auth import VKAppAuth
from settings_local import CLIENT_SECRET
import urllib2
import urllib
import json
import vk
app = Flask(__name__)

REDIRECT_URI = 'http://127.0.0.1:5000/redirect_from_vk'
CLIENT_ID = '5128481'
ACCESS_TOKEN = None
USER_ID = None


@app.route('/')
def home_handler():
    if not ACCESS_TOKEN:
        return redirect('/auth/')
    return render_template("Home.html")

# @app.route('/auth_old/', methods=['POST'])
# def vk_auth_old():
#     email = request.form['email']
#     password = request.form['password']
#     if not (email or password):
#         return render_template("Home.html", error='Enter email and password!')
#     vk_auth = VKAppAuth()
#     try:
#         token = vk_auth.auth(email, password, app_id=1, scope=['online'])
#     except RuntimeError:
#         return render_template("Home.html", error='Enter valid email and password!')
#     return render_template("Auth.html", token=token)


@app.route('/auth/')
def vk_auth():
    request_params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': ','.join(['audio', 'wall'])
    }
    url = "https://oauth.vk.com/authorize?" + urllib.urlencode(request_params)
    return redirect(url)


@app.route('/redirect_from_vk/')
def get_access_token():
    code = request.args.get('code')
    request_params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }
    url = 'https://oauth.vk.com/access_token?' + urllib.urlencode(request_params)
    response = json.loads(urllib2.urlopen(url).read())
    global USER_ID
    USER_ID = response['user_id']
    global ACCESS_TOKEN
    ACCESS_TOKEN = response['access_token']
    return redirect('/')


# @app.route('/post/')
# def get_info():
#     if not ACCESS_TOKEN:
#         return redirect('/auth/')
#     session = vk.Session(access_token=ACCESS_TOKEN)
#     api = vk.API(session)
#     info = api.audio.get(owner_id=USER_ID)
#     return 'ok'


if __name__ == '__main__':
    app.run()
