# Importing packages
from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import os
import markdown
import shelve

# Create an instance of app
app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    """Index will show the documentation"""
    with open(os.path.dirname(app.root_path) + "/README.md", 'r') as markdown_file:

        # Read the content of the documentation file
        content = markdown_file.read()

    # Converting to HTML
    return markdown.markdown(content)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, '_database'):
        g.sqlite_db = shelve.open("todolist.db")
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, '_database'):
        g.sqlite_db.close()


class TaskList(Resource):
    """Get all tasklists"""

    def get(self):
        db = get_db()
        keys = list(db.keys())

        tasks = []

        for key in keys:
            tasks.append(db[key])

        return {'message': 'Success', 'data': tasks}, 200

    def post(self):
        """Insert new tasks"""
        parser = reqparse.RequestParser()
        parser.add_argument('task_id', required=True)
        parser.add_argument('description', required=True)

        # Parse the arguments into a object

        args = parser.parse_args()
        db = get_db()
        db[args['task_id']] = args

        return {'message': 'Task created', 'data': args}, 201


class Task(Resource):
    def get(self, task_id):
        """Get a specific task"""
        db = get_db()
        return {'message': 'Task found', 'data': db[task_id]}, 200

    def delete(self, task_id):
        """Delete a specific task"""
        db = get_db()
        if (task_id not in db):
            return {'message': 'Not Found', 'data': {}}, 204
        del db[task_id]
        return {}, 204


api.add_resource(TaskList, '/tasklists')
api.add_resource(Task, '/task/<task_id>')
