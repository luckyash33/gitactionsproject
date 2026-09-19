import pytest
from app import app, uptime


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Route tests ───────────────────────────────────────────────────────────────

class TestHome:
    def test_status_code(self, client):
        assert client.get("/").status_code == 200

    def test_response_fields(self, client):
        data = client.get("/").get_json()
        assert data["status"] == "running"
        assert "app" in data
        assert "batch" in data
        assert "message" in data
        assert "website" in data


class TestHealth:
    def test_status_code(self, client):
        assert client.get("/health").status_code == 200

    def test_response_fields(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "This app is healthy"
        assert "uptime" in data
        assert "timestamp" in data

    def test_timestamp_format(self, client):
        data = client.get("/health").get_json()
        assert data["timestamp"].endswith("Z")


class TestInfo:
    def test_status_code(self, client):
        assert client.get("/info").status_code == 200

    def test_response_fields(self, client):
        data = client.get("/info").get_json()
        assert "python_version" in data
        assert "os" in data
        assert "hostname" in data
        assert "environment" in data
        assert "port" in data
        assert "built_by" in data

    def test_default_environment(self, client):
        data = client.get("/info").get_json()
        assert data["environment"] == "development"

    def test_default_port(self, client):
        data = client.get("/info").get_json()
        assert data["port"] == "5000"


class TestTopics:
    def test_status_code(self, client):
        assert client.get("/topics").status_code == 200

    def test_response_fields(self, client):
        data = client.get("/topics").get_json()
        assert "batch" in data
        assert "track" in data
        assert "topics_covered" in data
        assert "current_session" in data

    def test_topics_is_list(self, client):
        data = client.get("/topics").get_json()
        assert isinstance(data["topics_covered"], list)
        assert len(data["topics_covered"]) > 0

    def test_track_is_devsecops(self, client):
        data = client.get("/topics").get_json()
        assert data["track"] == "DevSecOps"


# ── Unit tests ────────────────────────────────────────────────────────────────

class TestUptime:
    def test_returns_string(self):
        result = uptime()
        assert isinstance(result, str)

    def test_format(self):
        result = uptime()
        assert "h" in result
        assert "m" in result
        assert "s" in result


# ── 404 handling ──────────────────────────────────────────────────────────────

class TestNotFound:
    def test_unknown_route(self, client):
        assert client.get("/nonexistent").status_code == 404
