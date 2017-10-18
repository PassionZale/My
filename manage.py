#! env/bin/python
import os
from flask import url_for
from flask_script import Manager, Shell, commands
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import FlaskyConfigs, FlaskyArticles

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('showurls', commands.ShowUrls)


@app.context_processor
def override_processor():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['v'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    manager.run()