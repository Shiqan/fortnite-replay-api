from flask import Blueprint, jsonify, request
from ray import Reader

from project.api.logging import logger
from project.api.models import Filter, Replay
from project.api.storage_service import StorageService
from project.api.storage_provider import StorageProvider

replay_blueprint = Blueprint('replay', __name__)
db = StorageService(StorageProvider())

@replay_blueprint.route('/replays/upload/', methods=['POST'])
def parse_replay():
    logger.info('parse_replay()')
    response_object = {
        'status': 'success'
    }

    username = request.form.get('username', None)
    files = request.files.getlist('data_file')

    if not files or not username:
        response_object['message'] = 'Invalid request!'
        response_object['status'] = 'failed'
    else:
        for f in files:
            f.stream.seek(0)
            with Reader(f.stream.read()) as replay:
                if replay.header.guid:
                    if db.insert_replay(username, replay):
                        response_object['message'] = 'Successfully uploaded replays!'
                        response_object['uploaded'] = len(files)
                    else:
                        response_object['message'] = 'This replay couldnt be uploaded!'
                        response_object['status'] = 'failed'
                else:
                    response_object['message'] = 'This replay is too old!'
                    response_object['status'] = 'failed'

    return jsonify(response_object)


@replay_blueprint.route('/player/<username>/', methods=['GET'])
def player_exists(username):
    logger.info(f'player_exists({username})')
    response_object = {
        'status': 'success'
    }

    if not username:
        response_object['message'] = 'No username provided!'
        response_object['status'] = 'failed'
        response_object['exists'] = False
    else:
        response_object['exists'] = db.player_exists(username)

    return jsonify(response_object)


@replay_blueprint.route('/replay/', methods=['POST'])
def all_replays_from():
    response_object = {
        'status': 'success'
    }

    username = request.form.get('username', None)
    start = request.form.get('start', 1)
    length = request.form.get('length', 10)
    search = request.form.get('search', '')
    startdate = request.form.get('startdate', None)
    enddate = request.form.get('enddate', None)
    min_position, max_position = request.form.get(
        'position', '0,100').split(',')
    min_kills, max_kills = request.form.get('kills', '0,100').split(',')
    win = request.form.get('win', False)

    if not username:
        response_object['message'] = 'No username provided!'
        response_object['status'] = 'failed'
    else:
        search_filter = Filter(username=username, search=search, start=int(start), length=int(length), win=win,
                               startdate=startdate, enddate=enddate, min_position=int(float(min_position)), max_position=int(float(max_position)),
                               min_kills=int(float(min_kills)), max_kills=int(float(max_kills)))

        logger.info(f'all_replays_from() - {username}')

        result = db.get_all_replays_from(search_filter)
        response_object['total'] = result.total
        response_object['pages'] = result.pages
        response_object['next'] = result.has_next
        response_object['prev'] = result.has_prev
        response_object['replays'] = result.items
    return jsonify(response_object)


@replay_blueprint.route('/replay/<replay_id>/', methods=['GET'])
def get_replay(replay_id):
    response_object = {
        'status': 'success'
    }

    if not replay_id:
        response_object['message'] = 'No id provided!'
        response_object['status'] = 'failed'
    else:
        logger.info(f'get_replay() - {replay_id}')

        result = db.get_replay(replay_id)
        response_object['replay'] = result
    return jsonify(response_object)


@replay_blueprint.route('/replays/ping/', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
