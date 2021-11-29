const express = require("express");
const axios = require("axios");
const dotenv = require("dotenv").config();
const crypto = require("crypto");
const qs = require("qs");

const { getState, setState } = require("./dal");

const ATTENTIVE_API_URL = "https://api-devel.attentivemobile.com/v1";
const ACCESS_TOKEN_ENDPOINT =
  "https://api-devel.attentivemobile.com/v1/authorization-codes/tokens";

const CLIENT_ID = dotenv.parsed.CLIENT_ID; // Your client id
const CLIENT_SECRET = dotenv.parsed.CLIENT_SECRET; // Your secret
const REDIRECT_URI = dotenv.parsed.REDIRECT_URI; // Your redirect uri
const PORT = 3002;

let app = express();
app.use(express.json());

app.get("/", (req, res) => {
  try {
    res.send({ message: "Your Application is running successfully!" });
  } catch (ex) {
    console.error("unexpected error", ex);
    res.status(500).json({ message: "Unexpected error" });
  }
});

app.get("/install", async (req, res) => {
  try {
    // Generates a random string containing numbers and letters
    const state = crypto.randomBytes(5).toString("hex");

    // List of scopes that your app needs
    const scopes = ["ecommerce:write", "events:write", "subscriptions:write"];

    setState(state, {});
    const redirect_url =
      `https://ui-devel.attentivemobile.com/integrations/oauth-install?client_id=${CLIENT_ID}` +
      `&redirect_uri=${REDIRECT_URI}` +
      `&scope=${scopes.join("+")}` +
      `&state=${state}`;

    res.status(302).redirect(redirect_url);
  } catch (ex) {
    console.error("unexpected error", ex);
    res.status(500).json({ message: "Unexpected error" });
  }
});

app.get("/callback", async (req, res) => {
  try {
    const authorization_code = req.query.code;
    const state = req.query.state;

    let application = getState(state);
    if (!application) {
      return res.status(400).send({
        message: `Your Application did not successfully install due to no application in memory`,
      });
    }

    const payload = {
      grant_type: "authorization_code",
      code: authorization_code,
      redirect_uri: REDIRECT_URI,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    };
    // your application makes a request to exchange an authorization code for an access_token
    const response = await axios.post(
      ACCESS_TOKEN_ENDPOINT,
      qs.stringify(payload),
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
    if (!response) {
      return res.status(400).send({
        message: `Your Application did not successfully install due to ${response.status_code} from ${ACCESS_TOKEN_ENDPOINT}/me`,
      });
    }

    const access_token = response.data.access_token;
    const me_response = await axios.get(`${ATTENTIVE_API_URL}/me`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    });
    if (!me_response) {
      return res.status(400).send({
        message: `Your Application did not successfully install due to ${me_response.status_code} from ${ATTENTIVE_API_URL}/me`,
      });
    }

    const company_name = me_response.data.companyName;

    // store access token and information about the installing company if necessary
    application["token"] = access_token;
    application["name"] = company_name;
    setState(state, application);

    // build redirect url and return 302
    res
      .status(200)
      .send({ message: "Your Application is installed successfully!" });
  } catch (ex) {
    console.error("unexpected error", ex);
    res.status(500).json({ message: "Unexpected error" });
  }
});

app.post("/webhooks", async (req, res) => {
  try {
    const webhook_secret = dotenv.parsed.WEBHOOK_SECRET;
    const payload = JSON.stringify(req.body);
    if (webhook_secret) {
      const signature = req.headers["x-attentive-hmac-sha256"];

      const hmac = crypto.createHmac("sha256", webhook_secret);
      const digest = Buffer.from(hmac.update(payload).digest("hex"), "utf8");
      const checksum = Buffer.from(signature, "utf8");

      if (
        checksum.length !== digest.length ||
        !crypto.timingSafeEqual(digest, checksum)
      ) {
        console.log(
          `‼️ Webhook received with invalid signature! digest: ${digest}, checksum: ${checksum}, ` +
            `request body: ${payload}`
        );
        res.status(403).json({ status: "invalid signature" });
        return;
      }
    }

    const event_type = req.body.type;
    console.log(`🔔 Webhook of type ${event_type} received! ${payload}`);
    res.status(200).json({ status: "success" });
  } catch (ex) {
    console.error("unexpected error", ex);
    res.status(500).json({ message: "Unexpected error" });
  }
});

app.listen(PORT, () => {
  console.log(`Demo app is listening at http://localhost:${PORT}`);
});
