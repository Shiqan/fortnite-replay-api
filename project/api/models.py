import datetime
from collections import Counter

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

from dataclasses import dataclass
from project.app import db


@dataclass
class Filter:
    username: str
    start: int
    length: int
    search: str
    startdate: datetime
    enddate: datetime
    min_position: int
    max_position: int
    min_kills: int
    max_kills: int
    win: bool


class Elimination(db.Model):
    __tablename__ = 'elimination'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    replay_id = db.Column(db.Integer, db.ForeignKey(
        'replay.id', ondelete='CASCADE'))

    eliminator = db.Column(db.String(255), nullable=False)
    eliminated = db.Column(db.String(255), nullable=False)
    knocked = db.Column(db.Boolean)
    weapon_type = db.Column(db.Integer, default=False, nullable=False)
    time = db.Column(db.DateTime, default=False, nullable=False)

    def __init__(self, replayId, **kwargs):
        super(Elimination, self).__init__(**kwargs)

    def __json__(self):
        return ['eliminator', 'eliminated', 'knocked', 'weapon_type', 'time']


class Replay(db.Model):
    __tablename__ = 'replay'

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

    elimination_events = db.relationship("Elimination", backref="Replay")

    @hybrid_property
    def knocks(self):
        return len([i for i in self.elimination_events if i.eliminator == self.username and i.knocked])

    @hybrid_property
    def knocked(self):
        return len([i for i in self.elimination_events if i.eliminated == self.username and i.knocked])

    @hybrid_property
    def weapon_usage(self):
        return Counter(i.weapon_type for i in self.elimination_events)

    def __init__(self, title, username, stats, team_stats):
        self.title = title
        self.username = username

        self.eliminations = stats['eliminations']
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

        self.position = team_stats['position']
        self.total_players = team_stats['total_players']

    def __json__(self):
        return ['id', 'created_at', 'title', 'username', 'accuracy', 'assists', 'weapon_damage', 'other_damage', 'revives', 'damage_taken',
                'damage_structures', 'materials_gathered', 'materials_used', 'total_traveled', 'eliminations', 'position', 'total_players', 'knocks', 'knocked', 'weapon_usage']
