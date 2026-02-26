"""
Bugcrowd MCP server test suite.

Unit tests (default):
  - Mock all httpx calls via respx.
  - Verify every tool function calls the correct URL + HTTP method.

Integration tests (requires real credentials in .env):
  - Hit the live Bugcrowd API for all safe GET list endpoints.
  - Run with: pytest -m integration
  - Skip unit tests with: pytest -m "not integration"
"""

import os
import sys
import pytest
import respx
import httpx
from dotenv import load_dotenv

# Ensure project root is on the path so `import server` works from tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server as srv

BASE = "https://api.bugcrowd.com"
FAKE_ID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
MOCK_CREDS = ("test_user", "test_pass")
MOCK_JSON = {"data": []}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_creds(monkeypatch):
    """Patch module-level credential vars for unit tests."""
    monkeypatch.setattr(srv, "BUGCROWD_API_USERNAME", MOCK_CREDS[0])
    monkeypatch.setattr(srv, "BUGCROWD_API_PASSWORD", MOCK_CREDS[1])


@pytest.fixture(scope="session")
def live_creds():
    """Load real credentials for integration tests. Skip if missing."""
    load_dotenv()
    username = os.getenv("BUGCROWD_API_USERNAME")
    password = os.getenv("BUGCROWD_API_PASSWORD")
    if not username or not password:
        pytest.skip(
            "No live credentials found – set BUGCROWD_API_USERNAME and BUGCROWD_API_PASSWORD"
        )
    # Ensure the module also sees the real values (they may have been read at import)
    srv.BUGCROWD_API_USERNAME = username
    srv.BUGCROWD_API_PASSWORD = password
    return username, password


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _mock_route(method: str, path: str):
    """Register a respx mock route and return it."""
    return respx.route(method=method, url=f"{BASE}{path}").mock(
        return_value=httpx.Response(200, json=MOCK_JSON)
    )


# ---------------------------------------------------------------------------
# Unit tests – route construction
# ---------------------------------------------------------------------------


class TestAccessInvitations:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/access_invitations")
            await srv.get_access_invitations()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/access_invitations/{FAKE_ID}")
            await srv.get_access_invitation(FAKE_ID)
            assert r.called

    async def test_post(self, mock_creds):
        with respx.mock:
            r = _mock_route("POST", "/access_invitations")
            await srv.post_access_invitations(data={"type": "access_invitations"})
            assert r.called

    async def test_delete(self, mock_creds):
        with respx.mock:
            r = _mock_route("DELETE", f"/access_invitations/{FAKE_ID}")
            await srv.delete_access_invitation(FAKE_ID)
            assert r.called


class TestCustomerAssets:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/customer_assets")
            await srv.get_customer_assets()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/customer_assets/{FAKE_ID}")
            await srv.get_customer_asset(FAKE_ID)
            assert r.called

    async def test_post(self, mock_creds):
        with respx.mock:
            r = _mock_route("POST", "/customer_assets")
            await srv.post_customer_assets(data={"type": "customer_assets"})
            assert r.called

    async def test_patch(self, mock_creds):
        with respx.mock:
            r = _mock_route("PATCH", f"/customer_assets/{FAKE_ID}")
            await srv.patch_customer_asset(FAKE_ID, data={})
            assert r.called

    async def test_delete(self, mock_creds):
        with respx.mock:
            r = _mock_route("DELETE", f"/customer_assets/{FAKE_ID}")
            await srv.delete_customer_asset(FAKE_ID)
            assert r.called


class TestOrganizations:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/organizations")
            await srv.get_organizations()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/organizations/{FAKE_ID}")
            await srv.get_organization(FAKE_ID)
            assert r.called

    async def test_patch(self, mock_creds):
        with respx.mock:
            r = _mock_route("PATCH", f"/organizations/{FAKE_ID}")
            await srv.patch_organization(FAKE_ID, data={})
            assert r.called


class TestPrograms:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/programs")
            await srv.get_programs()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/programs/{FAKE_ID}")
            await srv.get_program(FAKE_ID)
            assert r.called


class TestReports:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/reports")
            await srv.get_reports()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/reports/{FAKE_ID}")
            await srv.get_report(FAKE_ID)
            assert r.called

    async def test_post(self, mock_creds):
        with respx.mock:
            r = _mock_route("POST", "/reports")
            await srv.post_reports(data={"type": "reports"})
            assert r.called

    async def test_patch(self, mock_creds):
        with respx.mock:
            r = _mock_route("PATCH", f"/reports/{FAKE_ID}")
            await srv.patch_report(FAKE_ID, data={})
            assert r.called

    async def test_delete(self, mock_creds):
        with respx.mock:
            r = _mock_route("DELETE", f"/reports/{FAKE_ID}")
            await srv.delete_report(FAKE_ID)
            assert r.called


class TestSubmissions:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/submissions")
            await srv.get_submissions()
            assert r.called

    async def test_list_with_filter(self, mock_creds):
        with respx.mock:
            r = respx.get(f"{BASE}/submissions").mock(
                return_value=httpx.Response(200, json=MOCK_JSON)
            )
            await srv.get_submissions(query_params={"filter[program]": "test-prog"})
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/submissions/{FAKE_ID}")
            await srv.get_submission(FAKE_ID)
            assert r.called

    async def test_post(self, mock_creds):
        with respx.mock:
            r = _mock_route("POST", "/submissions")
            await srv.post_submissions(data={"type": "submissions"})
            assert r.called

    async def test_patch(self, mock_creds):
        with respx.mock:
            r = _mock_route("PATCH", f"/submissions/{FAKE_ID}")
            await srv.patch_submission(FAKE_ID, data={})
            assert r.called

    async def test_delete(self, mock_creds):
        with respx.mock:
            r = _mock_route("DELETE", f"/submissions/{FAKE_ID}")
            await srv.delete_submission(FAKE_ID)
            assert r.called


class TestSubmissionActivities:
    """
    These were previously broken (used /submission_activities – flat 404 path).
    Now uses the correct nested route: /submissions/{id}/activities
    """

    async def test_list_uses_nested_route(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/submissions/{FAKE_ID}/activities")
            await srv.get_submission_activities(FAKE_ID)
            assert r.called, (
                "get_submission_activities must call /submissions/{id}/activities, "
                "not the flat /submission_activities path"
            )

    async def test_get_by_id_uses_nested_route(self, mock_creds):
        activity_id = "11111111-2222-3333-4444-555555555555"
        with respx.mock:
            r = _mock_route("GET", f"/submissions/{FAKE_ID}/activities/{activity_id}")
            await srv.get_submission_activity(FAKE_ID, activity_id)
            assert r.called

    async def test_flat_route_is_not_used(self, mock_creds):
        """Regression: the old flat /submission_activities path must NOT be called."""
        with respx.mock:
            bad_route = respx.get(f"{BASE}/submission_activities").mock(
                return_value=httpx.Response(404, json={"error": "not found"})
            )
            good_route = _mock_route("GET", f"/submissions/{FAKE_ID}/activities")
            await srv.get_submission_activities(FAKE_ID)
            assert (
                not bad_route.called
            ), "Flat /submission_activities route should NOT be called"
            assert good_route.called


class TestSubmissionComments:
    """
    These were previously broken (used /submission_comments – flat 404 path).
    Now uses the correct nested route: /submissions/{id}/comments
    """

    async def test_list_uses_nested_route(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/submissions/{FAKE_ID}/comments")
            await srv.get_submission_comments(FAKE_ID)
            assert r.called, (
                "get_submission_comments must call /submissions/{id}/comments, "
                "not the flat /submission_comments path"
            )

    async def test_get_by_id_uses_nested_route(self, mock_creds):
        comment_id = "cccccccc-dddd-eeee-ffff-000000000000"
        with respx.mock:
            r = _mock_route("GET", f"/submissions/{FAKE_ID}/comments/{comment_id}")
            await srv.get_submission_comment(FAKE_ID, comment_id)
            assert r.called

    async def test_flat_route_is_not_used(self, mock_creds):
        """Regression: the old flat /submission_comments path must NOT be called."""
        with respx.mock:
            bad_route = respx.get(f"{BASE}/submission_comments").mock(
                return_value=httpx.Response(404, json={"error": "not found"})
            )
            good_route = _mock_route("GET", f"/submissions/{FAKE_ID}/comments")
            await srv.get_submission_comments(FAKE_ID)
            assert (
                not bad_route.called
            ), "Flat /submission_comments route should NOT be called"
            assert good_route.called


class TestAuthenticationLogs:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/authentication_logs")
            await srv.get_authentication_logs()
            assert r.called


class TestAuthorizationLogs:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/authorization_logs")
            await srv.get_authorization_logs()
            assert r.called


class TestDisclosureRequests:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/disclosure_requests")
            await srv.get_disclosure_requests()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/disclosure_requests/{FAKE_ID}")
            await srv.get_disclosure_request(FAKE_ID)
            assert r.called

    async def test_post(self, mock_creds):
        with respx.mock:
            r = _mock_route("POST", "/disclosure_requests")
            await srv.post_disclosure_requests(data={"type": "disclosure_requests"})
            assert r.called


class TestExternalIssues:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/external_issues")
            await srv.get_external_issues()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/external_issues/{FAKE_ID}")
            await srv.get_external_issue(FAKE_ID)
            assert r.called

    async def test_post(self, mock_creds):
        with respx.mock:
            r = _mock_route("POST", "/external_issues")
            await srv.post_external_issues(data={"type": "external_issues"})
            assert r.called

    async def test_patch(self, mock_creds):
        with respx.mock:
            r = _mock_route("PATCH", f"/external_issues/{FAKE_ID}")
            await srv.patch_external_issue(FAKE_ID, data={})
            assert r.called

    async def test_delete(self, mock_creds):
        with respx.mock:
            r = _mock_route("DELETE", f"/external_issues/{FAKE_ID}")
            await srv.delete_external_issue(FAKE_ID)
            assert r.called


class TestMonetaryRewards:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/monetary_rewards")
            await srv.get_monetary_rewards()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/monetary_rewards/{FAKE_ID}")
            await srv.get_monetary_reward(FAKE_ID)
            assert r.called


class TestPayments:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/payments")
            await srv.get_payments()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/payments/{FAKE_ID}")
            await srv.get_payment(FAKE_ID)
            assert r.called


class TestTargetGroups:
    """Target groups are served via /targets in the Bugcrowd API."""

    async def test_list_uses_targets_path(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/targets")
            await srv.get_target_groups()
            assert r.called, "get_target_groups must call /targets, not /target_groups"

    async def test_get_by_id_uses_targets_path(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/targets/{FAKE_ID}")
            await srv.get_target_group(FAKE_ID)
            assert r.called

    async def test_old_target_groups_path_not_used(self, mock_creds):
        """Regression: /target_groups (old wrong path) must NOT be called."""
        with respx.mock:
            bad = respx.get(f"{BASE}/target_groups").mock(
                return_value=httpx.Response(404, json={})
            )
            good = _mock_route("GET", "/targets")
            await srv.get_target_groups()
            assert not bad.called
            assert good.called


class TestUsers:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/users")
            await srv.get_users()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/users/{FAKE_ID}")
            await srv.get_user(FAKE_ID)
            assert r.called


class TestEngagements:
    async def test_list(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/engagements")
            await srv.get_engagements()
            assert r.called

    async def test_get_by_id(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", f"/engagements/{FAKE_ID}")
            await srv.get_engagement(FAKE_ID)
            assert r.called


class TestAuthHeaders:
    """Verify correct auth/version headers are sent on every request."""

    async def test_authorization_header(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/submissions")
            await srv.get_submissions()
            assert r.called
            req = r.calls.last.request
            assert (
                req.headers["Authorization"] == f"Token {MOCK_CREDS[0]}:{MOCK_CREDS[1]}"
            )

    async def test_accept_header(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/submissions")
            await srv.get_submissions()
            req = r.calls.last.request
            assert req.headers["Accept"] == "application/vnd.bugcrowd+json"

    async def test_bugcrowd_version_header(self, mock_creds):
        with respx.mock:
            r = _mock_route("GET", "/submissions")
            await srv.get_submissions()
            req = r.calls.last.request
            assert req.headers["Bugcrowd-Version"] == srv.BUGCROWD_API_VERSION

    async def test_missing_credentials_raises(self, monkeypatch):
        monkeypatch.setattr(srv, "BUGCROWD_API_USERNAME", "")
        monkeypatch.setattr(srv, "BUGCROWD_API_PASSWORD", "")
        with pytest.raises(RuntimeError, match="BUGCROWD_API_USERNAME"):
            await srv.get_submissions()


# ---------------------------------------------------------------------------
# Integration tests – live API calls
# ---------------------------------------------------------------------------
#
# These hit the real Bugcrowd API.  Run them with:
#   pytest -m integration
#
# They will be skipped automatically when no credentials are present.
# ---------------------------------------------------------------------------

# Unverified endpoints: these paths return 404 on the live Bugcrowd public API
# across all tested API versions.  Kept in server.py for completeness but
# marked xfail here so failures are expected and visible.
UNVERIFIED_ENDPOINTS = [
    "get_users",
    "get_reports",
    "get_monetary_rewards",
    "get_payments",
    "get_customer_assets",
    "get_external_issues",
]

SAFE_GET_ENDPOINTS = [
    ("get_submissions", lambda: srv.get_submissions({"page[limit]": "1"})),
    ("get_programs", lambda: srv.get_programs({"page[limit]": "1"})),
    ("get_organizations", lambda: srv.get_organizations({"page[limit]": "1"})),
    (
        "get_access_invitations",
        lambda: srv.get_access_invitations({"page[limit]": "1"}),
    ),
    ("get_target_groups", lambda: srv.get_target_groups({"page[limit]": "1"})),
    ("get_engagements", lambda: srv.get_engagements({"page[limit]": "1"})),
    ("get_disclosure_requests", lambda: srv.get_disclosure_requests()),  # no pagination
    # The following paths don't exist on the public API (404 every version)
    pytest.param(
        "get_users",
        lambda: srv.get_users({"page[limit]": "1"}),
        marks=pytest.mark.xfail(reason="/users not available on public Bugcrowd API"),
    ),
    pytest.param(
        "get_reports",
        lambda: srv.get_reports({"page[limit]": "1"}),
        marks=pytest.mark.xfail(reason="/reports not available on public Bugcrowd API"),
    ),
    pytest.param(
        "get_monetary_rewards",
        lambda: srv.get_monetary_rewards({"page[limit]": "1"}),
        marks=pytest.mark.xfail(
            reason="/monetary_rewards not available on public Bugcrowd API"
        ),
    ),
    pytest.param(
        "get_payments",
        lambda: srv.get_payments({"page[limit]": "1"}),
        marks=pytest.mark.xfail(
            reason="/payments not available on public Bugcrowd API"
        ),
    ),
    pytest.param(
        "get_customer_assets",
        lambda: srv.get_customer_assets({"page[limit]": "1"}),
        marks=pytest.mark.xfail(
            reason="/customer_assets not available on public Bugcrowd API"
        ),
    ),
    pytest.param(
        "get_external_issues",
        lambda: srv.get_external_issues({"page[limit]": "1"}),
        marks=pytest.mark.xfail(
            reason="/external_issues not available on public Bugcrowd API"
        ),
    ),
]


@pytest.mark.integration
@pytest.mark.parametrize("name,call", SAFE_GET_ENDPOINTS)
async def test_live_get_endpoints(live_creds, name, call):
    """Every GET list endpoint must return a response with a 'data' key."""
    try:
        result = await call()
        assert (
            "data" in result
        ), f"{name}: response missing 'data' key – got keys: {list(result.keys())}"
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        # 403 = endpoint exists but we don't have permission (acceptable)
        # 404 = endpoint does not exist (BUG – fail the test)
        if status == 404:
            pytest.fail(
                f"{name}: received 404 – endpoint path is likely wrong. "
                f"URL called: {exc.request.url}"
            )
        elif status == 403:
            pytest.skip(
                f"{name}: 403 Forbidden – insufficient permissions for this account"
            )
        else:
            raise


@pytest.mark.integration
async def test_live_authentication_logs(live_creds):
    """
    Authentication logs require filter[start_date] + filter[end_date].
    The API enforces a strict 30-day rolling window server-side.
    A 422 means the endpoint exists but the date window was rejected.
    """
    import datetime

    today = datetime.date.today()
    start = (today - datetime.timedelta(days=7)).isoformat()
    end = today.isoformat()
    try:
        result = await srv.get_authentication_logs(
            {"filter[start_date]": start, "filter[end_date]": end}
        )
        assert "data" in result
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 422:
            pytest.skip(f"Endpoint exists but 422 returned: {exc.response.text[:200]}")
        if exc.response.status_code == 404:
            pytest.fail(
                f"get_authentication_logs returned 404 – path may be wrong. URL: {exc.request.url}"
            )
        raise


@pytest.mark.integration
async def test_live_authorization_logs(live_creds):
    """
    Authorization logs require filter[start_date] + filter[end_date].
    The API enforces a strict 30-day rolling window server-side.
    A 422 means the endpoint exists but the date window was rejected.
    """
    import datetime

    today = datetime.date.today()
    start = (today - datetime.timedelta(days=7)).isoformat()
    end = today.isoformat()
    try:
        result = await srv.get_authorization_logs(
            {"filter[start_date]": start, "filter[end_date]": end}
        )
        assert "data" in result
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 422:
            pytest.skip(f"Endpoint exists but 422 returned: {exc.response.text[:200]}")
        if exc.response.status_code == 404:
            pytest.fail(
                f"get_authorization_logs returned 404 – path may be wrong. URL: {exc.request.url}"
            )
        raise


@pytest.mark.integration
async def test_live_get_submission_by_id(live_creds):
    """Fetch the known submission from the earlier investigation to verify /submissions/{id}."""
    known_id = "af39a5dd-6cbf-4880-bde4-e70605307eb6"
    result = await srv.get_submission(known_id)
    assert "data" in result
    assert result["data"]["id"] == known_id


@pytest.mark.integration
async def test_live_submission_comments_nested_route(live_creds):
    """Verify /submissions/{id}/comments works (was broken with flat path)."""
    known_id = "af39a5dd-6cbf-4880-bde4-e70605307eb6"
    try:
        result = await srv.get_submission_comments(known_id)
        assert "data" in result
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            pytest.fail(
                f"get_submission_comments returned 404 – nested route may still be wrong. "
                f"URL: {exc.request.url}"
            )
        raise


@pytest.mark.integration
async def test_live_submission_activities_nested_route(live_creds):
    """Verify /submissions/{id}/activities works (was broken with flat path)."""
    known_id = "af39a5dd-6cbf-4880-bde4-e70605307eb6"
    try:
        result = await srv.get_submission_activities(known_id)
        assert "data" in result
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            pytest.fail(
                f"get_submission_activities returned 404 – nested route may still be wrong. "
                f"URL: {exc.request.url}"
            )
        raise
