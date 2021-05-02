from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, abort, reqparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from UptimeBot import UptimeBot

# Create a Flask app
app = Flask(__name__)

# Enable CORS for server
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Using RESTful API wrapper
api = Api(app)

# Initialize bot for real-time checking
bot = UptimeBot()

# Initialize a request parser (for POST request)
parser = reqparse.RequestParser()

# Adds required arguments
parser.add_argument("ip")
parser.add_argument("port")

# Adding rate limits for requests
# so we won't get spammed and suffer
# from DDoS
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)


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
    # [GET] => Shows a single server
    def get(self, id):
        # Try to parse an ID from request input
        try:
            id = int(id)
        # If it can't be parsed, show a message telling that
        # IDs must be integers
        except:
            abort(400, message="Server IDs are integers.")

        # Checks if ID exists
        abort_if_doesnt_exist(id)

        # Return server status
        return bot.get_server(id)


class ServerList(Resource):
    # ServerList

    decorators = [limiter.limit("2/minute")]

    # [GET] => Shows a list of all servers
    def get(self):
        # Get all servers status
        return bot.get_servers()

    # [POST] => Returns status of an arbitrary server
    def post(self):
        # Parse arguments
        args = parser.parse_args()
        # Try to parse an integer port from request input
        try:
            port = int(args["port"])
        # If it can't be parsed, show a message telling that
        # port must be integer
        except:
            abort(400, message="Port must be integer.")
        ip = args["ip"]
        return bot.get_custom_server(ip, port)


# Routing
# This will allow requests on path "/servers"
api.add_resource(ServerList, "/servers")
# This will allow requests on path "/servers/<id>", getting <id> as a parameter
api.add_resource(Server, "/servers/<id>")


if __name__ == "__main__":
    # Run the Flask app disabling debug mode
    app.run(debug=False)
