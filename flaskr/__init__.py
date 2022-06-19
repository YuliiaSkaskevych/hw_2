import os
from flask import Flask, render_template
from flaskr.db import get_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def home_page():
        return '<p>Welcome!</p>'

    @app.route('/names/')
    def names():
        db = get_db()
        artist = db.execute(
            'SELECT COUNT (DISTINCT id) AS "artist" FROM tracks'
        ).fetchall()
        return render_template('names.html', artist=artist)

    @app.route('/tracks/')
    def tracks():
        db = get_db()
        tracks = db.execute(
            'SELECT COUNT (id) FROM tracks'
        ).fetchone()
        return render_template('tracks_info.html', tracks=tracks)

    @app.route('/tracks/<genre>/')
    def genre(genre):
        db = get_db()
        if genre in db:
            genre_t = db.execute(
                'SELECT COUNT (id) FROM tracks WHERE genre=?'
            ).fetchone()
            return render_template('genre.html', genre=genre_t)
        else:
            return f'Tracks has not genre {genre}!'

    @app.route('/tracks-sec/')
    def tracks_sec():
        db = get_db()
        sec = db.execute(
            'SELECT title, length FROM tracks'
        ).fetchall()
        return render_template('tracks_sec.html', sec=sec)

    @app.route('/tracks-sec/statistics/')
    def statistics():
        db = get_db()
        avg = db.execute(
            'SELECT AVG(length) FROM tracks'
        ).fetchone()
        sum = db.execute(
            'SELECT SUM(length) FROM tracks'
        ).fetchone()
        return render_template('statistics.html', avg=avg, sum=sum)

    from . import db
    db.init_app(app)

    return app