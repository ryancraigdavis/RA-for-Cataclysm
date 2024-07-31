from quart import Blueprint, jsonify, current_app
import aiohttp
from ..utils.auth import get_access_token
from ..queries.fight_queries import FETCH_SINGLE_FIGHT_WITH_EVENTS

bp = Blueprint('fight', __name__)

@bp.route("/api/fight/<report_code>/<int:fight_id>", methods=["GET"])
async def fetch_fight_with_events(report_code, fight_id):
    token = await get_access_token()
    if not token:
        return jsonify({"error": "Failed to obtain access token"}), 500

    variables = {
        "reportCode": report_code,
        "fightID": fight_id
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(current_app.config['API_URL'], 
                                json={"query": FETCH_SINGLE_FIGHT_WITH_EVENTS, "variables": variables}, 
                                headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return jsonify(data)
            else:
                current_app.logger.error(f"Failed to query WarcraftLogs API. Status: {response.status}")
                return jsonify({"error": "Failed to query WarcraftLogs API"}), response.status
