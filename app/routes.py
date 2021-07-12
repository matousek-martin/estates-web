from datetime import datetime, timedelta

from flask import render_template

from app import app, db
from app.models import Estates, EstateImages


@app.route('/')
@app.route('/index')
def index():
    month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    estates = db.session.query(Estates).filter(Estates.created_at > month_ago).all()
    return render_template('index.html', title='Home', estates=estates[:100])
