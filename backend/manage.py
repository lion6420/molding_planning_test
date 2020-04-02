from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from app import app

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
  return dict(app=app)

if __name__ == '__main__':
  manager.run()