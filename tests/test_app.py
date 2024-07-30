import pytest
from quart import Quart
from quart.testing import QuartClient
import json
from ra_for_cataclysm.app import app, get_access_token, TOKEN_URL, CLIENT_ID, CLIENT_SECRET
from unittest.mock import AsyncMock, MagicMock
from aioresponses import aioresponses
import aiohttp

@pytest.fixture
def test_app():
    return app

@pytest.fixture
def client(test_app):
    return QuartClient(test_app)

@pytest.mark.asyncio
async def test_get_access_token_success():
    with aioresponses() as m:
        m.post(TOKEN_URL, status=200, payload={"access_token": "mock_token"})
        token = await get_access_token()
        assert token == "mock_token"

@pytest.mark.asyncio
async def test_get_access_token_failure():
    with aioresponses() as m:
        m.post(TOKEN_URL, status=400)
        token = await get_access_token()
        assert token is None

@pytest.mark.asyncio
async def test_get_access_token_correct_request():
    with aioresponses() as m:
        m.post(TOKEN_URL, status=200, payload={"access_token": "mock_token"})
        await get_access_token()
        request = m.requests[('POST', TOKEN_URL)][0]
        assert request.kwargs['data'] == {"grant_type": "client_credentials"}
        assert 'Authorization' in request.kwargs['headers']
        # We can't check the exact auth value, but we can check it's present

@pytest.mark.asyncio
async def test_fetch_fight_with_events_success(client, mocker):
    # Mock the get_access_token function
    mocker.patch('ra_for_cataclysm.app.get_access_token', return_value="mock_token")
    
    # Mock the aiohttp ClientSession
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"data": {"reportData": {"report": {"code": "ABC123"}}}}
    
    mock_post = AsyncMock()
    mock_post.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post.return_value = mock_post

    mocker.patch('aiohttp.ClientSession', return_value=mock_session)
    
    response = await client.get('/api/fight/ABC123/1')
    assert response.status_code == 200
    data = json.loads(await response.get_data(as_text=True))
    assert data == {"data": {"reportData": {"report": {"code": "ABC123"}}}}

@pytest.mark.asyncio
async def test_fetch_fight_with_events_failure(client, mocker):
    # Mock the get_access_token function to return None
    mocker.patch('ra_for_cataclysm.app.get_access_token', return_value=None)
    
    response = await client.get('/api/fight/ABC123/1')
    assert response.status_code == 500
    data = json.loads(await response.get_data(as_text=True))
    assert data == {"error": "Failed to obtain access token"}

@pytest.mark.asyncio
async def test_fetch_fight_with_events_api_failure(client, mocker):
    # Mock the get_access_token function
    mocker.patch('ra_for_cataclysm.app.get_access_token', return_value="mock_token")
    
    # Mock the aiohttp ClientSession
    mock_response = AsyncMock()
    mock_response.status = 400
    
    mock_post = AsyncMock()
    mock_post.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post.return_value = mock_post

    mocker.patch('aiohttp.ClientSession', return_value=mock_session)
    
    response = await client.get('/api/fight/ABC123/1')
    assert response.status_code == 400
    data = json.loads(await response.get_data(as_text=True))
    assert data == {"error": "Failed to query WarcraftLogs API"}
