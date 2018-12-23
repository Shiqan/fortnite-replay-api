#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import and_, func
from sqlalchemy.sql import exists

from project.api.logging import logger
from project.api.models import Replay
from project.app import db


class Storage:
    def insert_replay(replay):
        try:
            db.session.add(replay)
            db.session.commit()
            return True
        except Exception:
            logger.error('Exception inserting replay', exc_info=1)
            return False

    def player_exists(username):
        try:
            return db.session.query(exists().where(Replay.username == username)).scalar()
        except Exception:
            logger.error(
                'Exception while checking if player exists', exc_info=1)
            return False

    def get_all_replays():
        return Replay.query.order_by(Replay.created_at.desc()).limit(5)

    def get_number_of_replays_from(username):
        return db.session.query(func.count(Replay.username == username)).scalar()

    def get_number_of_wins_from(username):
        return db.session.query(func.count(and_(Replay.username == username, Replay.position == 1))).scalar()

    def get_all_replays_from(search_filter):
        filters = [
            Replay.username == search_filter.username,
            Replay.eliminations >= search_filter.min_kills, 
            Replay.eliminations <= search_filter.max_kills,
            Replay.position >= search_filter.min_position, 
            Replay.position <= search_filter.max_position
        ]

        if search_filter.search:
            filters.append(Replay.title.like(search_filter.search+'%'))

        if search_filter.win == 'true':
            filters.append(Replay.position == '1')

        if search_filter.startdate:
            filters.append(Replay.created_at >= search_filter.startdate)

        if search_filter.enddate:
            filters.append(Replay.created_at <= search_filter.enddate)

        return Replay.query.filter(*filters)\
            .order_by(Replay.created_at.desc())\
            .paginate(
                page=search_filter.start,
                per_page=search_filter.length
            )
