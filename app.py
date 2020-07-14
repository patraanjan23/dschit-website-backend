import json
import os

from firebase_admin import auth, credentials, firestore, initialize_app
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)
CORS(app)
api = Api(app)
cred = credentials.Certificate(json.loads(os.environ['FIREBASE_CERT']))
fireapp = initialize_app(cred)
firedb = firestore.client()

colnames = {"team", "events", "projects", "resources"}
cols = {src: firedb.collection(src) for src in colnames}


@app.route('/', methods=['GET'])
def index():
    return '<H1>welcome to dschit backend</H1>'


class RouteResource(Resource):
    def aget(self, filename):
        """Abstract GET method for all routes"""
        try:
            data = []
            docs = cols[filename].stream()
            for doc in docs:
                data.append(doc.to_dict())
            return jsonify(data)
        except Exception as e:
            return f'ErrorGET: {e}', 404

    def apost(self, colname):
        """Abstract POST method for all routes"""
        idToken = request.headers['Authorization'].split(' ').pop()
        user = auth.verify_id_token(idToken)
        if not user:
            return 'Unauthorized', 401
        else:
            try:
                response = request.get_json()
                # TODO add json validation using schema later
                if 'id' in response.keys():
                    doc_id = str(response.pop('id'))
                    doc = cols[colname].document(doc_id).get()
                    if 'modify' in response.keys() and response['modify'] or not doc.exists:
                        if 'modify' in response.keys():
                            response.pop('modify')
                        cols[colname].document(doc_id).set(response)
                        return jsonify({'msg': 'Record Successfully Added'})
                    else:
                        return f'ItemExists: id = {doc_id}', 404
                else:
                    return 'IDError', 404
            except Exception as e:
                return f'ErrorPOST: {e}', 404

    def validate(self, data, valid_keys_for_post: set):
        result = False
        try:
            result = set(data.keys()) == valid_keys_for_post
        except:
            pass
        return result


class Events(RouteResource):
    def get(self):
        return self.aget("events")

    def post(self):
        return self.apost("events")


class Team(RouteResource):
    def get(self):
        return self.aget("team")

    def post(self):
        return self.apost("team")


class Projects(RouteResource):
    def get(self):
        return self.aget("projects")

    def post(self):
        return self.apost("projects")


class Resources(RouteResource):
    def get(self):
        return self.aget("resources")

    def post(self):
        return self.apost("resources")


api.add_resource(Events, '/events')
api.add_resource(Team, '/team')
api.add_resource(Projects, '/projects')
api.add_resource(Resources, '/resources')

if __name__ == "__main__":
    app.run(debug=True)
