from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, abort
from UptimeBot import UptimeBot

# Create a Flask app
app = Flask(__name__)

# Enable CORS for server
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Using RESTful API wrapper
api = Api(app)

# Initialize bot for real-time checking
bot = UptimeBot()


def abort_if_doesnt_exist(id):
    """This function will return a 404 when a server ID does not exist"""
    try:
        # If this raises an exception
        bot.get_server(id)
    except:
        # Return a 404 page
        abort(404, message="Server with ID {} does not exist".format(id))


class Server(Resource):
    # Server
    # Shows a single server
    def get(self, id):
        try:

            # Try to parse an ID from request input
            id = int(id)
        except:

            # If it can't be parsed, show a message telling that
            # IDs must be integers
            abort(400, message="Server IDs are integers.")

        # Checks if ID exists
        abort_if_doesnt_exist(id)

        # Return server status
        return bot.get_server(id)


class ServerList(Resource):
    # ServerList
    # Shows a list of all servers
    def get(self):
        # Get all servers status
        return bot.get_servers()


# Routing
# This will allow requests on path "/servers"
api.add_resource(ServerList, "/servers")
# This will allow requests on path "/servers/<id>", getting <id> as a parameter
api.add_resource(Server, "/servers/<id>")


if __name__ == "__main__":
    # Run the Flask app disabling debug mode
    app.run(debug=False)
