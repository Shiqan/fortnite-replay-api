from sqlalchemy import and_, func
from sqlalchemy.sql import exists

from project.api.logging import logger
from project.api.models import Elimination, Replay, ReplayStats
from project.app import db


class StorageProvider:
    def insert_replay(self, username, replay):
        if (self.replay_exists(str(replay.header.guid))):
            logger.info('Replay already exists')
            return False

        try:
            model = Replay(guid=str(replay.header.guid),
                           version=replay.header.fortnite_version,
                           release=replay.header.release,
                           total_players=replay.team_stats['total_players'])
            db.session.add(model)
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.error('Exception inserting replay', exc_info=1)
            return False

        try:
            db.session.add(ReplayStats(replay_id=model.id, username=username,
                                stats=replay.stats, team_stats=replay.team_stats))
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.error(
                f'Exception inserting replay stats for {username}', exc_info=1)
            return False

        try:
            for elim in replay.eliminations:
                db.session.add(Elimination(replayId=model.id, replay_id=model.id, eliminator=elim.eliminator,
                                           eliminated=elim.eliminated, weapon_type=elim.gun_type, knocked=elim.knocked, time=elim.time))
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.error('Exception inserting replay', exc_info=1)
            return False
        return True

    def replay_exists(self, guid):
        try:
            return db.session.query(exists().where(Replay.guid == guid)).scalar()
        except Exception:
            logger.error(
                'Exception while checking if replays exists', exc_info=1)
            return False

    def player_exists(self, username):
        try:
            return db.session.query(exists().where(ReplayStats.username == username)).scalar()
        except Exception:
            logger.error(
                'Exception while checking if player exists', exc_info=1)
            return False

    def get_replay(self, replay_id):
        return db.session.query(Replay).get(replay_id)

    def get_number_of_replays_from(self, username):
        return db.session.query(func.count(ReplayStats.username == username)).scalar()

    def get_number_of_wins_from(self, username):
        return db.session.query(func.count(and_(ReplayStats.username == username, ReplayStats.winner == True))).scalar()

    def get_all_replays_from(self, search_filter):
        filters = [
            ReplayStats.username == search_filter.username,
            ReplayStats.eliminations >= search_filter.min_kills,
            ReplayStats.eliminations <= search_filter.max_kills,
            ReplayStats.position >= search_filter.min_position,
            ReplayStats.position <= search_filter.max_position
        ]

        if search_filter.search:
            pass
            # filters.append(Replay.title.like(search_filter.search+'%'))

        if search_filter.win == 'true':
            filters.append(ReplayStats.winner == True)

        if search_filter.startdate:
            filters.append(ReplayStats.created_at >= search_filter.startdate)

        if search_filter.enddate:
            filters.append(ReplayStats.created_at <= search_filter.enddate)

        return ReplayStats.query.filter(*filters)\
            .order_by(ReplayStats.created_at.desc())\
            .paginate(
                page=search_filter.start,
                per_page=search_filter.length
        )
