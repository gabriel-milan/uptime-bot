__all__ = ["UptimeBot"]

import json
from time import sleep
from threading import Thread
from utils import is_up


class UptimeBot:
    """Class for real-time checking servers
    on a thread.
    """

    def __init__(self, server_list_file="/app/server_list.json") -> None:
        """
        Provide a JSON file with the server list
        """

        # Tries to parse JSON file
        try:
            # Open provided file as read-only
            with open(server_list_file, "r") as f:
                # Parse text content into JSON dictionary
                servers = json.load(f)
                # Close file
                f.close()
        except:
            # File does not exist
            raise NameError(
                f"Failed to load server list from file {server_list_file}")

        # If attribute "servers" is not on JSON
        if "servers" not in servers:
            # JSON file is not properly written
            raise ValueError(
                "Key 'servers' not found in server list, please check your file")

        # If type of attribute "servers" is not a list
        elif type(servers["servers"]) != list:
            # JSON file is not properly written
            raise ValueError("'servers' attribute must be a list")

        # Get server list
        servers = servers["servers"]

        # Check each server for missing content
        for i, server in enumerate(servers):

            # If IP was not specified
            if not "ip" in server:
                # JSON file is not properly written
                raise ValueError(f"Server {server} must have attribute 'ip'!")

            # If port was not specified
            elif not "port" in server:
                # JSON file is not properly written
                raise ValueError(
                    f"Server {server} must have attribute 'port'!")

            # Provide an unique ID for this server
            server["id"] = i

            # Server initial state is "down"
            server["state"] = False

        # Store server list in an object attribute
        self._servers = servers

        # Create a thread list
        self._threads = []

        # Set myself as running
        self._running = True

        # For each server on the list
        for i in range(len(self._servers)):

            # Start a new thread running the function "update_server_loop"
            # on the background
            thread = Thread(target=self.update_server_loop,
                            args=(i,), daemon=True)
            thread.start()

            # Append this thread to the thread list
            self._threads.append(thread)

    @property
    def running(self):
        """Just a getter for the _running attribute"""
        return self._running

    def get_servers(self):
        """Get information for all servers"""
        return self._servers

    def get_server(self, id):
        """Get a single server information"""
        return self._servers[id]

    def get_custom_server(self, ip, port):
        """Get a custom server information"""
        # Create an empty dictionary
        info = {}
        # Add IP attribute
        info["ip"] = ip
        # Add port attribute
        info["port"] = port
        # Add status
        info["state"] = is_up(ip, port)
        # Return this information
        return info

    def update_server_loop(self, server_id):
        """Loop function for updating server status"""

        # This will stop running when main thread stops
        while self.running:

            # Try to update server information
            try:
                # Update server status using the "is_up" function
                self._servers[server_id]["state"] = is_up(
                    self._servers[server_id]["ip"], self._servers[server_id]["port"])

            # If it fails, for any reason
            except Exception as e:
                # Log it so we can check on later
                print(f"Failed to update server with ID {server_id}: {e}")

            # Sleep for 1 second (will update server status every second)
            sleep(1)
