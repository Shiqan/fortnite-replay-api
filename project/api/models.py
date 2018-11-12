#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy.sql import func

from project import db


class Replay(db.Model):
    __tablename__ = 'replays'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now())

    eliminations = db.Column(db.Integer, default=False, nullable=False)
    accuracy = db.Column(db.Float, default=False, nullable=False)
    assists = db.Column(db.Integer, default=False, nullable=False)
    weapon_damage = db.Column(db.Integer, default=False, nullable=False)
    other_damage = db.Column(db.Integer, default=False, nullable=False)
    revives = db.Column(db.Integer, default=False, nullable=False)
    damage_taken = db.Column(db.Integer, default=False, nullable=False)
    damage_structures = db.Column(db.Integer, default=False, nullable=False)
    materials_gathered = db.Column(db.Integer, default=False, nullable=False)
    materials_used = db.Column(db.Integer, default=False, nullable=False)
    total_traveled = db.Column(db.Integer, default=False, nullable=False)

    position = db.Column(db.Integer, default=False, nullable=False)
    total_players = db.Column(db.Integer, default=False, nullable=False)

    def __init__(self, title, username, stats, team_stats, eliminations):
        self.title = title
        self.username = username

        self.accuracy = stats['accuracy']
        self.assists = stats['assists']
        self.weapon_damage = stats['weapon_damage']
        self.other_damage = stats['other_damage']
        self.revives = stats['revives']
        self.damage_taken = stats['damage_taken']
        self.damage_structures = stats['damage_structures']
        self.materials_gathered = stats['materials_gathered']
        self.materials_used = stats['materials_used']
        self.total_traveled = stats['total_traveled']
        self.eliminations = len(eliminations)

        self.position = team_stats['position']
        self.total_players = team_stats['total_players']

    def __json__(self):
        return ['created_at', 'title', 'username', 'accuracy', 'assists', 'weapon_damage', 'other_damage', 'revives', 'damage_taken',
                'damage_structures', 'materials_gathered', 'materials_used', 'total_traveled', 'eliminations', 'position', 'total_players']
