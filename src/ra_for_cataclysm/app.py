import os
from quart import Quart
from dotenv import load_dotenv
from .routes import fight

# Load environment variables
load_dotenv()

# WarcraftLogs API details
TOKEN_URL = "https://www.warcraftlogs.com/oauth/token"
API_URL = "https://www.warcraftlogs.com/api/v2/client"

# Load client credentials from environment variables
CLIENT_ID = os.getenv("WCL_CLIENT_ID")
CLIENT_SECRET = os.getenv("WCL_CLIENT_SECRET")

if CLIENT_ID is None or CLIENT_SECRET is None:
    raise ValueError("CLIENT_ID and CLIENT_SECRET must be set")

app = Quart(__name__)

app.register_blueprint(fight.bp)

if __name__ == "__main__":
    app.run()
