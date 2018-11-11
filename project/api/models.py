#!/usr/bin/python
# -*- coding: utf-8 -*-

from project import db
from sqlalchemy.sql import func


class Replay(db.Model):
    __tablename__ = 'replays'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,  server_default=func.now())

    accuracy = db.Column(db.Integer, default=False, nullable=False)
    assists = db.Column(db.Integer, default=False, nullable=False)
    eliminations = db.Column(db.Integer, default=False, nullable=False)
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
     

    def __init__(self, title, username, stats, team_stats):
        self.title = title
        self.username = username

        self.accuracy = stats.accuracy
        self.assists = stats.assists
        self.eliminations = stats.eliminations
        self.weapon_damage = stats.weapon_damage
        self.other_damage = stats.other_damage
        self.revives = stats.revives
        self.damage_taken = stats.damage_taken
        self.damage_structures = stats.damage_structures
        self.materials_gathered = stats.materials_gathered
        self.materials_used = stats.materials_used
        self.total_traveled = stats.total_traveled

        self.position = team_stats.position
        self.total_players = team_stats.total_players

    def to_json(self):
        return self.__dict__()