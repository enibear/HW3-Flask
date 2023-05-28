import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def main():
    return render_template('index.html')


@bp.route('/names/', methods=('GET', 'POST'))
def names():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(DISTINCT artist) FROM tracks")
        count = cursor.fetchone()[0]

        return render_template('names.html', content=count)
    return render_template('names.html')

@bp.route('/tracks/', methods=('GET', 'POST'))
def tracks():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(title) FROM tracks")
    count = cursor.fetchone()[0]

    cursor.execute("SELECT genre FROM tracks")
    rows = cursor.fetchall()
    tracks = [row[0] for row in rows]

    if request.method == 'POST':
        genre = request.form['genre']
        cursor.execute("SELECT COUNT(*) FROM tracks WHERE genre = ?", (genre,))
        count_genre = cursor.fetchone()[0]

        return render_template('tracks.html', count=count_genre, content=count, tracks=tracks)

    return render_template('tracks.html', content=count, tracks=tracks)


@bp.route('/tracks-sec/')
def title():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT title, length FROM tracks")
    rows = cursor.fetchall()
    tracks = [(row['title'], row['length']) for row in rows]

    return render_template('title.html', content=tracks)


@bp.route('/tracks-sec/statistics/')
def statistics():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT length FROM tracks")
    rows = cursor.fetchall()
    tracks = [row['length'] for row in rows]
    total_sum = sum(tracks)
    average_sum = sum(tracks) / len(tracks)

    return render_template('statistics.html', total_sum=total_sum, average_sum=average_sum)
