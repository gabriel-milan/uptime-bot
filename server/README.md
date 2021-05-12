# UptimeBot server

## First steps

- Copy the `example_server_list.json` file in the root of this repository into `server_list.json` and adapt it to fit your needs.
- Run `docker-compose build server` in order to build the Docker image for server only
- Run `docker-compose up server` in order to run the server
- Server will be available at `http://localhost:8001/`

## Endpoints

- `GET http://<your-server>:8001/servers`: returns the list of servers in `server_list.json` with current status. Ouput format is as follows:
```json
[
  {
    "ip": "google.com",
    "port": 80,
    "id": 0,
    "state": true
  },
  {
    "ip": "www.lps.ufrj.br",
    "port": 443,
    "id": 1,
    "state": true
  }
]
```

- `GET http://<your-server>:8001/servers/<id>`: returns the server in `server_list.json` at index `<id>`. Ouput format is as follows:
```json
{
  "ip": "google.com",
  "port": 80,
  "id": 0,
  "state": true
}
```

- `POST http://<your-server>:8001/servers`: expects input with `ip` and `port`, the format (JSON, form, etc.) doesn't really matter

Example input:
```json
{
	"ip": "google.com",
	"port": 443
}
```

Output for this:
```json
{
  "ip": "google.com",
  "port": 443,
  "state": true
}
```

## Rate limits

Currently values are:

- For all endpoints: maximum 1000 requests per day, maximum 100 requests per hour
- For the `http://<your-server>:8001/servers` endpoint: (all endpoints rules) + maximum 2 requests per minute