from flask import Flask

app = Flask(__name__)
app.secret_key = 'iwakikan'


from app import routes