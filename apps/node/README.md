# Attentive Application Demo — Node Server

This demo uses a simple [Express 4x](https://expressjs.com/) application as the server to demonstrate the
Attentive OAuth install flow.

View [Authentication](https://docs.attentivemobile.com/pages/authentication/) for more details on Attentive's Authorization
flow.

### Prerequistes:

- [Node v12.0.0](https://nodejs.org/en/download/)
 
### Getting Started

Complete the following setps to run the demo application:

1. Once you have the correct Node setup, copy the example environment variables file .env.example from the root of the repo into your own environment file called .env:
    ```bash
    cp .env.example .env
    ```

1. Update your .env file with your unique Attentive API keys and any other configuration details you might want to add.
   The <b>env</b> variables are managed through the `dotenv` node package.

1. Setup the node environment

    ```bash
    cd apps/node
    npm install
    ```

1. Run `npm start` to fetch the Python packages Attentive uses:
    ```bash
    npm start
    ```

1. (bonus) For hot reloading for development purposes, install Nodemon
    ```bash
    npm install -G nodemon
    nodemon
    ```

You should now see the demo application running on `http://localhost:3002`
