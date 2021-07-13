import re
from collections import defaultdict
from datetime import datetime, timedelta

import folium
from flask import render_template, url_for, request

from app import app, db
from app.models import Estates, EstateImages


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    estates = (
        db
        .session
        .query(Estates)
        .filter(Estates.created_at > yesterday)
        .order_by(Estates.estate_id.desc())
        .paginate(page, app.config['ESTATES_PER_PAGE'], False)
    )
    next_url = url_for('index', page=estates.next_num) if estates.has_next else None
    prev_url = url_for('index', page=estates.prev_num) if estates.has_prev else None

    # Get images for queried estates
    images_table = defaultdict(list)
    estate_ids = [estate.estate_id for estate in estates.items]
    images = db.session.query(EstateImages).filter(EstateImages.estate_id.in_(estate_ids)).all()
    for image in images:
        images_table[image.estate_id].append(image.estate_images)

    return render_template(
        'index.html',
        estates=estates.items,
        images=images_table,
        next_url=next_url,
        prev_url=prev_url
    )


@app.route('/detail/<estate_id>')
def detail(estate_id):
    # Fetch estate details
    estate = (
        db
        .session
        .query(Estates)
        .filter(Estates.estate_id == estate_id)
        .first()
    )
    estate.seller_numbers = re.findall(r"\d{12}", estate.seller_numbers)

    # Fetch estate images
    images = db.session.query(EstateImages).filter(EstateImages.estate_id == estate_id).all()

    # Create map
    coordinates = (estate.estate_latitude, estate.estate_longitude)
    folium_map = folium.Map(location=coordinates, zoom_start=16)
    folium.Marker(location=coordinates, icon=folium.Icon(icon='home')).add_to(folium_map)

    return render_template(
        'detail.html',
        estate=estate,
        images=images,
        map=folium_map._repr_html_()
    )
