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

    from . import db
    db.init_app(app)

    @app.route('/')
    def home_page():
        return '<p>Welcome!</p>'

    @app.route('/names/')
    def names():
        db = get_db()
        artist = db.execute(
            'SELECT COUNT (DISTINCT artist) FROM tracks'
        ).fetchone()
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
        g = db.execute(
            'SELECT COUNT (id) FROM tracks WHERE genre = ?', (genre,)
        ).fetchone()
        return render_template('genre.html', g=g, genre=genre)


    @app.route('/tracks-sec/')
    def tracks_sec():
        db = get_db()
        sec = db.execute(
            'SELECT title,running FROM tracks'
        ).fetchall()
        return render_template('tracks_sec.html', sec=sec)

    @app.route('/tracks-sec/statistics/')
    def statistics():
        db = get_db()
        count = db.execute(
            'SELECT AVG(running), SUM(running) FROM tracks'
        ).fetchall()
        return render_template('statistics.html', count=count)

    return app