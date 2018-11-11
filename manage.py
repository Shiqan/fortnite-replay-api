from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from project.app import create_app, db
from project.api.models import Replay

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()