# Attentive Application Demo — Python Server

This demo uses a simple [Flask](https://flask.palletsprojects.com/en/2.0.x/) application as the server to demonstrate the
Attentive OAuth install flow.


### You’ll need the following:

- [Docker](https://docs.docker.com/get-docker/)

### Getting Started

Once you have Docker setup, copy the example environment variables file .env.example from the root of the repo into your own environment file called .env:
```bash
cp .env.example .env
```

Update your .env file with your own Attentive  API keys and any other configuration details you might want to add. 
The env variables are managed via the python-dotenv package.

To start the service, run
```bash
docker-compose up
```
You should now see it running on `http://localhost:3000`

### Testing Webhooks

TODO

## Tests

TODO
