import os
import aiohttp
from quart import current_app

TOKEN_URL = "https://www.warcraftlogs.com/oauth/token"

async def get_access_token():
    client_id = current_app.config['WCL_CLIENT_ID']
    client_secret = current_app.config['WCL_CLIENT_SECRET']

    async with aiohttp.ClientSession() as session:
        async with session.post(TOKEN_URL, 
                                auth=aiohttp.BasicAuth(client_id, client_secret),
                                data={"grant_type": "client_credentials"}) as response:
            if response.status == 200:
                data = await response.json()
                return data["access_token"]
            else:
                current_app.logger.error(f"Failed to obtain access token. Status: {response.status}")
                return None
