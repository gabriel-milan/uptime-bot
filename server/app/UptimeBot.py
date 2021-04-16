__all__ = ["UptimeBot"]

import json
from time import sleep
from threading import Thread
from utils import is_up


class UptimeBot:
    def __init__(self, server_list_file="/app/server_list.json") -> None:
        try:
            with open(server_list_file, "r") as f:
                servers = json.load(f)
                f.close()
        except:
            raise NameError(
                f"Failed to load server list from file {server_list_file}")
        if "servers" not in servers:
            raise ValueError(
                "Key 'servers' not found in server list, please check your file")
        elif type(servers["servers"]) != list:
            raise ValueError("'servers' attribute must be a list")
        servers = servers["servers"]
        for i, server in enumerate(servers):
            if not "ip" in server:
                raise ValueError(f"Server {server} must have attribute 'ip'!")
            elif not "port" in server:
                raise ValueError(
                    f"Server {server} must have attribute 'port'!")
            server["id"] = i
            server["state"] = False
        self._servers = servers
        self._threads = []
        self._running = True
        for i in range(len(self._servers)):
            thread = Thread(target=self.update_server_loop,
                            args=(i,), daemon=True)
            thread.start()
            self._threads.append(thread)

    @property
    def running(self):
        return self._running

    def get_servers(self):
        return self._servers

    def get_server(self, id):
        return self._servers[id]

    def update_server_loop(self, server_id):
        while self.running:
            try:
                self._servers[server_id]["state"] = is_up(
                    self._servers[server_id]["ip"], self._servers[server_id]["port"])
            except Exception as e:
                print(f"Failed to update server with ID {server_id}: {e}")
            sleep(1)
