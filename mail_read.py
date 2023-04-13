import json
import requests
from flask import Flask, request, redirect
from msal import ConfidentialClientApplication

app = Flask(__name__)

# Get Azure APP API creds from config.py
from config import tenant_id, client_id, client_secret

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/Mail.Read"]

msal_app = ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)

@app.route("/")
def index():
    auth_url = msal_app.get_authorization_request_url(scopes, redirect_uri="http://localhost:5000/callback")
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    result = msal_app.acquire_token_by_authorization_code(code, scopes, redirect_uri="http://localhost:5000/callback")

    if "access_token" in result:
        access_token = result["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "odata-version": "4.0"}

        messages_url = "https://graph.microsoft.com/v1.0/me/messages"
        response = requests.get(messages_url, headers=headers)

        if response.status_code == 200:
            messages = response.json()["value"]
            # Save messages to a file
            with open("messages.txt", "w") as file:
                for message in messages:
                    file.write(json.dumps(message, indent=4))
                    file.write("\n\n")
            return json.dumps(messages, indent=4)
        else:
            return f"Error getting messages: {response.status_code} - {response.text}"
    else:
        return "Error acquiring token"

if __name__ == "__main__":
    app.run(debug=True)
