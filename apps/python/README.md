# Attentive Application Demo — Python Server

This demo uses a simple [Flask](https://flask.palletsprojects.com/en/2.0.x/) application as the server to demonstrate the
Attentive OAuth install flow.

For more detail on the Authorization code flow that Attentive uses, please checkout our documentation [here](https://docs.attentivemobile.com/pages/authentication/)

### You’ll need the following:

- [Python 3.7.8](https://www.python.org/downloads/release/python-378/)

### Getting Started

Before getting started, check to see that you have the right version of Python installed (3.7.8).
```bash
python3 --version
```

Once you have the correct Python setup, copy the example environment variables file .env.example from the root of the repo into your own environment file called .env:
```bash
cp .env.example .env
```

Update your .env file with your own Attentive  API keys and any other configuration details you might want to add. 
The env variables are managed via the python-dotenv package.

After, create a virtual environment to manage the packages and state our application needs:

```bash
cd apps/python
python3 -m venv env
source env/bin/activate
```

Run pip install to fetch the Python packages we use:
```bash
pip install -r requirements.txt
```

Export our Flask app and run!
```bash
export FLASK_APP=./src/app.py
python3 -m flask run
```

You should now see it running on `http://localhost:3000`
