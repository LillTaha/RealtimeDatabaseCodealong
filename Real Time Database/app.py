from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Firebase configuration
firebaseConfig = {
  'apiKey': "AIzaSyAGB8GFQN4N4vI_pFsXDVDrHSdpLYYysvk",
  'authDomain': "meet-example2024.firebaseapp.com",
  'databaseURL': "https://meet-example2024-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "meet-example2024",
  'storageBucket': "meet-example2024.appspot.com",
  'messagingSenderId': "104511305959",
  'appId': "1:104511305959:web:583cc9dde2b008e9b94a42",
  'measurementId': "G-6JPQ4XNJTT"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def index():
    if 'user' in login_session:
        print(login_session['user'])
        user_id = login_session['user']['localId']
        user_data = db.child("users").child(user_id).get().val()
        all_users = db.child("users").get().val()
        return render_template('profile.html', user=user_data, all_users=all_users)
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        fav_movie = request.form['fav_movie']
        fav_song = request.form['fav_song']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            db.child("users").child(user_id).set({
                "name": name,
                "fav_movie": fav_movie,
                "fav_song": fav_song
            })
            login_session['user'] = user
            return redirect(url_for('index'))
        except:
            return "Failed to create account. Try again."
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            login_session['user'] = user
            return redirect(url_for('index'))
        except:
            return "Failed to login. Check your credentials."
    return render_template('login.html')

@app.route('/logout')
def logout():
    login_session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)