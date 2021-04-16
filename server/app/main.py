from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, abort
from UptimeBot import UptimeBot

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
bot = UptimeBot()


def abort_if_doesnt_exist(id):
    try:
        bot.get_server(id)
    except:
        abort(404, message="Server with ID {} does not exist".format(id))


class Server(Resource):
    # Server
    # Shows a single server
    def get(self, id):
        try:
            id = int(id)
        except:
            abort(400, message="Server IDs are integers.")
        abort_if_doesnt_exist(id)
        return bot.get_server(id)


class ServerList(Resource):
    # ServerList
    # Shows a list of all servers
    def get(self):
        return bot.get_servers()


# Routing
api.add_resource(ServerList, "/servers")
api.add_resource(Server, "/servers/<id>")


if __name__ == "__main__":
    app.run(debug=False)
