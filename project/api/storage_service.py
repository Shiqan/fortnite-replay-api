class StorageService:
    def __init__(self, provider):
        self.provider = provider

    def insert_replay(self, username, replay):
        return self.provider.insert_replay(username, replay)

    def replay_exists(self, guid):
        return self.provider.replay_exists(guid)

    def player_exists(self, username):
        return self.provider.player_exists(username)

    def get_replay(self, replay_id):
        return self.provider.get_replay(replay_id)

    def get_number_of_replays_from(self, username):
        return self.provider.get_number_of_replays_from(username)

    def get_number_of_wins_from(self, username):
        return self.provider.get_number_of_wins_from(username)

    def get_all_replays_from(self, search_filter):
        return self.provider.get_all_replays_from(search_filter)
