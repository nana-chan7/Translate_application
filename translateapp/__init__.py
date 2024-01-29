from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rgsVBrhbhantjukdlldeer1230fnxgnz'
app.config.from_object('translateapp.config')

import translateapp.views
