import os
from quart import Quart
from dotenv import load_dotenv

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

# Add configuration
app.config['WCL_CLIENT_ID'] = CLIENT_ID
app.config['WCL_CLIENT_SECRET'] = CLIENT_SECRET
app.config['API_URL'] = API_URL

# Import and register routes
from ra_for_cataclysm.routes import fight

app.register_blueprint(fight.bp)

if __name__ == "__main__":
    app.run()
