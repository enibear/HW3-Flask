import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def fill_db():
    db = get_db()
    cursor = db.cursor()

    tracks_data = [
        ('Track1', 'Artist1', 'Rock', 123),
        ('Track2', 'Artist2', 'Pop', 321),
        ('Track3', 'Artist3', 'Hip Hop', 456),
        ('Track4', 'Artist4', 'Electronic', 654),
        ('Track5', 'Artist5', 'Jazz', 789),
        ('Track6', 'Artist6', 'Bop-pop', 987),
        ('Track6', 'Artist6', 'Bop-pop', 123)
    ]

    for track in tracks_data:
        cursor.execute(
            'INSERT INTO tracks (title, artist, genre, length) VALUES (?, ?, ?, ?)', track
        )

    db.commit()
    db.close()


@click.command('fill-db')
def fill_db_command():
    fill_db()
    click.echo('Fill the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(fill_db_command)
