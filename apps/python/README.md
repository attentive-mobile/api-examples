# Attentive Application Demo — Python Server

This demo uses a simple [Flask](https://flask.palletsprojects.com/en/2.0.x/) application as the server to demonstrate the
Attentive OAuth install flow.

View [Authentication](https://docs.attentivemobile.com/pages/authentication/) for more details on Attentive's Authorization
flow.

### Prerequistes:

- [Python 3.7.8](https://www.python.org/downloads/release/python-378/)
 
Before getting started, check to see that you have the right version of Python installed (3.7.8).
```bash
python3 --version
```
<i>If your machine is running Python 2 as the default then you can follow these great guides on installing Python 3 for
[macOS](https://docs.python-guide.org/starting/install3/osx/), [Windows](https://docs.python-guide.org/starting/install3/win/),
or [Linux](https://docs.python-guide.org/starting/install3/linux/).
</i>

### Getting Started

Complete the following setps to run the demo application:

1. Once you have the correct Python setup, copy the example environment variables file .env.example from the root of the repo into your own environment file called .env:
    ```bash
    cp .env.example .env
    ```

1. Update your .env file with your unique Attentive API keys and any other configuration details you might want to add.
   The <b>env</b> variables are managed through the `python-dotenv` package.

1. Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to manage the packages and state your application needs:

    ```bash
    cd apps/python
    python3 -m venv env
    source env/bin/activate
    ```

1. Run `pip install` to fetch the Python packages Attentive uses:
    ```bash
    pip install -r requirements.txt
    ```

1. Export our Flask app and run:
    ```bash
    export FLASK_APP=./src/app.py
    python3 -m flask run
    ```

You should now see the demo application running on `http://localhost:3000`
