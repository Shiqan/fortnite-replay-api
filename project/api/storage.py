#!/usr/bin/python
# -*- coding: utf-8 -*-

from project.app import db
from project.api.models import Replay

class Storage:
    def insert_replay(replay):
        try:
            db.session.add(replay)
            db.session.commit()
            return True
        except Exception:
            return False

    def get_all_replays():
        return Replay.query.order_by(Replay.created_at.desc()).all()

    def get_all_replays_from(username):
        return Replay.query.filter_by(username=username).order_by(Replay.created_at.desc()).all()
