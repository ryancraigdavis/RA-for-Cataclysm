import os
from quart import Quart, jsonify, request
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Quart(__name__)

# WarcraftLogs API details
TOKEN_URL = "https://www.warcraftlogs.com/oauth/token"
API_URL = "https://www.warcraftlogs.com/api/v2/client"

# Load client credentials from environment variables
CLIENT_ID = os.getenv("WCL_CLIENT_ID")
CLIENT_SECRET = os.getenv("WCL_CLIENT_SECRET")

if CLIENT_ID is None or CLIENT_SECRET is None:
    raise ValueError("CLIENT_ID and CLIENT_SECRET must be set")

async def get_access_token():
    async with aiohttp.ClientSession() as session:
        async with session.post(TOKEN_URL, 
                                auth=aiohttp.BasicAuth(CLIENT_ID, CLIENT_SECRET),
                                data={"grant_type": "client_credentials"}) as response:
            if response.status == 200:
                data = await response.json()
                return data["access_token"]
            else:
                return None

@app.route("/")
async def hello():
    return "Welcome to the Warcraft Logs API Proxy!"

@app.route("/api/fight/<report_code>/<int:fight_id>", methods=["GET"])
async def fetch_fight_with_events(report_code, fight_id):
    token = await get_access_token()
    if not token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    query = """
    query FetchSingleFightWithEvents($reportCode: String!, $fightID: Int!) {
      reportData {
        report(code: $reportCode) {
          code
          title
          fights(fightIDs: [$fightID]) {
            id
            name
            difficulty
            encounterID
            startTime
            endTime
            averageItemLevel
            bossPercentage
            fightPercentage
            lastPhase
            kill
            size
            completeRaid
            enemyPlayers
            friendlyPlayers
            gameZone {
              id
              name
            }
            enemyNPCs {
              id
              gameID
              instanceCount
            }
            dungeonPulls {
              startTime
              endTime
              enemyNPCs {
                id
                gameID
              }
            }
            maps {
              id
            }
          }
          events(fightIDs: [$fightID], limit: 10000) {
            data
            nextPageTimestamp
          }
        }
      }
    }
    """

    variables = {
        "reportCode": report_code,
        "fightID": fight_id
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json={"query": query, "variables": variables}, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return jsonify(data)
            else:
                return jsonify({"error": "Failed to query WarcraftLogs API"}), response.status

if __name__ == "__main__":
    app.run()
