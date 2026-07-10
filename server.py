import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

# Read Bugcrowd API credentials from environment variables
BUGCROWD_API_USERNAME = os.getenv("BUGCROWD_API_USERNAME")
BUGCROWD_API_PASSWORD = os.getenv("BUGCROWD_API_PASSWORD")
BUGCROWD_API_BASE = "https://api.bugcrowd.com"
BUGCROWD_API_VERSION = "2025-04-23"


async def bugcrowd_request(method, endpoint, **kwargs):
    """
    Async helper to make authenticated requests to the Bugcrowd API.
    """
    if not BUGCROWD_API_USERNAME or not BUGCROWD_API_PASSWORD:
        raise RuntimeError(
            "BUGCROWD_API_USERNAME and BUGCROWD_API_PASSWORD must be set in environment variables."
        )
    url = f"{BUGCROWD_API_BASE}{endpoint}"
    headers = kwargs.pop("headers", {})
    headers["Accept"] = "application/vnd.bugcrowd+json"
    headers["Authorization"] = f"Token {BUGCROWD_API_USERNAME}:{BUGCROWD_API_PASSWORD}"
    headers["Bugcrowd-Version"] = BUGCROWD_API_VERSION

    # Check if params is empty and remove it to avoid 400 bad request
    params = kwargs.get("params")
    if params is not None:
        is_empty = False
        if isinstance(params, dict):
            is_empty = not params or all(not v for v in params.values())
        elif isinstance(params, str):
            is_empty = not params.strip()
        elif hasattr(params, "__len__"):
            is_empty = len(params) == 0
        else:
            is_empty = not params
        if is_empty:
            kwargs.pop("params", None)

    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()


# Create the MCP server
mcp = FastMCP("Bugcrowd-MCP")


# ACCESS INVITATIONS
@mcp.tool()
async def get_access_invitations(query_params: dict = None):
    """List all access invitations."""
    return await bugcrowd_request("GET", "/access_invitations", params=query_params)


@mcp.tool()
async def get_access_invitation(id: str, query_params: dict = None):
    """Get a specific access invitation by ID."""
    return await bugcrowd_request(
        "GET", f"/access_invitations/{id}", params=query_params
    )


@mcp.tool()
async def post_access_invitations(data: dict):
    """Create a new access invitation."""
    return await bugcrowd_request("POST", "/access_invitations", json=data)


@mcp.tool()
async def delete_access_invitation(id: str):
    """Delete an access invitation by ID."""
    return await bugcrowd_request("DELETE", f"/access_invitations/{id}")


# ASSETS
# NOTE: /customer_assets returns 404 – this path does not exist in the Bugcrowd API.
@mcp.tool()
async def get_customer_assets(query_params: dict = None):
    """[UNVERIFIED] List customer assets. The /customer_assets path is not available on the public Bugcrowd API and currently returns 404."""
    return await bugcrowd_request("GET", "/customer_assets", params=query_params)


@mcp.tool()
async def get_customer_asset(id: str, query_params: dict = None):
    """[UNVERIFIED] Get a specific customer asset by ID. The /customer_assets path currently returns 404."""
    return await bugcrowd_request("GET", f"/customer_assets/{id}", params=query_params)


@mcp.tool()
async def post_customer_assets(data: dict):
    """[UNVERIFIED] Create a new customer asset. The /customer_assets path currently returns 404."""
    return await bugcrowd_request("POST", "/customer_assets", json=data)


@mcp.tool()
async def patch_customer_asset(id: str, data: dict):
    """[UNVERIFIED] Update a customer asset by ID. The /customer_assets path currently returns 404."""
    return await bugcrowd_request("PATCH", f"/customer_assets/{id}", json=data)


@mcp.tool()
async def delete_customer_asset(id: str):
    """[UNVERIFIED] Delete a customer asset by ID. The /customer_assets path currently returns 404."""
    return await bugcrowd_request("DELETE", f"/customer_assets/{id}")


# ORGANIZATIONS
@mcp.tool()
async def get_organizations(query_params: dict = None):
    """List all organizations."""
    return await bugcrowd_request("GET", "/organizations", params=query_params)


@mcp.tool()
async def get_organization(id: str, query_params: dict = None):
    """Get a specific organization by ID."""
    return await bugcrowd_request("GET", f"/organizations/{id}", params=query_params)


@mcp.tool()
async def patch_organization(id: str, data: dict):
    """Update an organization by ID."""
    return await bugcrowd_request("PATCH", f"/organizations/{id}", json=data)


# PROGRAMS
@mcp.tool()
async def get_programs(query_params: dict = None):
    """List all programs."""
    return await bugcrowd_request("GET", "/programs", params=query_params)


@mcp.tool()
async def get_program(id: str, query_params: dict = None):
    """Get a specific program by ID."""
    return await bugcrowd_request("GET", f"/programs/{id}", params=query_params)


# REPORTS
# NOTE: /reports returns 404 – this path does not exist in the Bugcrowd API.
@mcp.tool()
async def get_reports(query_params: dict = None):
    """[UNVERIFIED] List reports. The /reports path is not available on the public Bugcrowd API and currently returns 404."""
    return await bugcrowd_request("GET", "/reports", params=query_params)


@mcp.tool()
async def get_report(id: str, query_params: dict = None):
    """[UNVERIFIED] Get a specific report by ID. The /reports path currently returns 404."""
    return await bugcrowd_request("GET", f"/reports/{id}", params=query_params)


@mcp.tool()
async def post_reports(data: dict):
    """[UNVERIFIED] Create a new report. The /reports path currently returns 404."""
    return await bugcrowd_request("POST", "/reports", json=data)


@mcp.tool()
async def patch_report(id: str, data: dict):
    """[UNVERIFIED] Update a report by ID. The /reports path currently returns 404."""
    return await bugcrowd_request("PATCH", f"/reports/{id}", json=data)


@mcp.tool()
async def delete_report(id: str):
    """[UNVERIFIED] Delete a report by ID. The /reports path currently returns 404."""
    return await bugcrowd_request("DELETE", f"/reports/{id}")


# SUBMISSIONS
@mcp.tool()
async def get_submissions(query_params: dict = None):
    """List all submissions. Supported filter keys: filter[program], filter[state], filter[severity], filter[assignee], filter[search], include, page[limit], page[offset], sort.

    IMPORTANT — filter[state] support:
      - Supported (returns results): new, unresolved
      - Unsupported (returns HTTP 400): informational, not_applicable, not_reproducible, out_of_scope
      - Invalid (returns HTTP 400): blocked

    To count submissions in unsupported states, retrieve all submissions without a state filter and count client-side.
    """
    # Guard against states known to cause HTTP 400 from the API
    UNSUPPORTED_STATES = {"informational", "not_applicable", "not_reproducible", "out_of_scope"}
    if query_params:
        state = query_params.get("filter[state]")
        if state in UNSUPPORTED_STATES:
            return {
                "error": f"The Bugcrowd API does not support filtering by state '{state}'. "
                         f"Unsupported states: {sorted(UNSUPPORTED_STATES)}. "
                         "To find submissions in this state, retrieve all submissions without a state filter and count client-side."
            }
    return await bugcrowd_request("GET", "/submissions", params=query_params)


@mcp.tool()
async def get_submission(id: str):
    """Get a specific submission by UUID. No query params supported on this endpoint."""
    return await bugcrowd_request("GET", f"/submissions/{id}")


@mcp.tool()
async def post_submissions(data: dict):
    """Create a new submission."""
    return await bugcrowd_request("POST", "/submissions", json=data)


@mcp.tool()
async def patch_submission(id: str, data: dict):
    """Update a submission by ID."""
    return await bugcrowd_request("PATCH", f"/submissions/{id}", json=data)


@mcp.tool()
async def delete_submission(id: str):
    """Delete a submission by ID."""
    return await bugcrowd_request("DELETE", f"/submissions/{id}")


# SUBMISSION ACTIVITIES
@mcp.tool()
async def get_submission_activities(submission_id: str, query_params: dict = None):
    """List all activities for a specific submission. Requires the submission UUID as submission_id."""
    return await bugcrowd_request(
        "GET", f"/submissions/{submission_id}/activities", params=query_params
    )


@mcp.tool()
async def get_submission_activity(
    submission_id: str, id: str, query_params: dict = None
):
    """Get a specific submission activity by ID."""
    return await bugcrowd_request(
        "GET", f"/submissions/{submission_id}/activities/{id}", params=query_params
    )


# SUBMISSION COMMENTS
@mcp.tool()
async def get_submission_comments(submission_id: str, query_params: dict = None):
    """List all comments for a specific submission. Requires the submission UUID as submission_id."""
    return await bugcrowd_request(
        "GET", f"/submissions/{submission_id}/comments", params=query_params
    )


@mcp.tool()
async def get_submission_comment(
    submission_id: str, id: str, query_params: dict = None
):
    """Get a specific submission comment by ID."""
    return await bugcrowd_request(
        "GET", f"/submissions/{submission_id}/comments/{id}", params=query_params
    )


# AUTHENTICATION LOGS
@mcp.tool()
async def get_authentication_logs(query_params: dict = None):
    """List authentication logs. REQUIRED: filter[start_date] and filter[end_date] (ISO 8601, within last 30 days). Example: {'filter[start_date]': '2026-02-01', 'filter[end_date]': '2026-02-26'}."""
    return await bugcrowd_request("GET", "/authentication_logs", params=query_params)


# AUTHORIZATION LOGS
@mcp.tool()
async def get_authorization_logs(query_params: dict = None):
    """List authorization logs. REQUIRED: filter[start_date] and filter[end_date] (ISO 8601, within last 30 days). Example: {'filter[start_date]': '2026-02-01', 'filter[end_date]': '2026-02-26'}."""
    return await bugcrowd_request("GET", "/authorization_logs", params=query_params)


# DISCLOSURE REQUESTS
@mcp.tool()
async def get_disclosure_requests(query_params: dict = None):
    """List all disclosure requests. NOTE: pagination (page[limit]/page[offset]) is not supported on this endpoint."""
    return await bugcrowd_request("GET", "/disclosure_requests", params=query_params)


@mcp.tool()
async def get_disclosure_request(id: str, query_params: dict = None):
    """Get a specific disclosure request by ID."""
    return await bugcrowd_request(
        "GET", f"/disclosure_requests/{id}", params=query_params
    )


@mcp.tool()
async def post_disclosure_requests(data: dict):
    """Create a new disclosure request."""
    return await bugcrowd_request("POST", "/disclosure_requests", json=data)


# EXTERNAL ISSUES
# NOTE: /external_issues returns 404 – this path does not exist in the Bugcrowd API.
@mcp.tool()
async def get_external_issues(query_params: dict = None):
    """[UNVERIFIED] List external issues. The /external_issues path is not available on the public Bugcrowd API and currently returns 404."""
    return await bugcrowd_request("GET", "/external_issues", params=query_params)


@mcp.tool()
async def get_external_issue(id: str, query_params: dict = None):
    """[UNVERIFIED] Get a specific external issue by ID. The /external_issues path currently returns 404."""
    return await bugcrowd_request("GET", f"/external_issues/{id}", params=query_params)


@mcp.tool()
async def post_external_issues(data: dict):
    """[UNVERIFIED] Create a new external issue. The /external_issues path currently returns 404."""
    return await bugcrowd_request("POST", "/external_issues", json=data)


@mcp.tool()
async def patch_external_issue(id: str, data: dict):
    """[UNVERIFIED] Update an external issue by ID. The /external_issues path currently returns 404."""
    return await bugcrowd_request("PATCH", f"/external_issues/{id}", json=data)


@mcp.tool()
async def delete_external_issue(id: str):
    """[UNVERIFIED] Delete an external issue by ID. The /external_issues path currently returns 404."""
    return await bugcrowd_request("DELETE", f"/external_issues/{id}")


# MONETARY REWARDS
# NOTE: /monetary_rewards returns 404 – this path does not exist in the Bugcrowd API.
@mcp.tool()
async def get_monetary_rewards(query_params: dict = None):
    """[UNVERIFIED] List monetary rewards. The /monetary_rewards path is not available on the public Bugcrowd API and currently returns 404."""
    return await bugcrowd_request("GET", "/monetary_rewards", params=query_params)


@mcp.tool()
async def get_monetary_reward(id: str, query_params: dict = None):
    """[UNVERIFIED] Get a specific monetary reward by ID. The /monetary_rewards path currently returns 404."""
    return await bugcrowd_request("GET", f"/monetary_rewards/{id}", params=query_params)


# PAYMENTS
# NOTE: /payments returns 404 – this path does not exist in the Bugcrowd API.
@mcp.tool()
async def get_payments(query_params: dict = None):
    """[UNVERIFIED] List payments. The /payments path is not available on the public Bugcrowd API and currently returns 404."""
    return await bugcrowd_request("GET", "/payments", params=query_params)


@mcp.tool()
async def get_payment(id: str, query_params: dict = None):
    """[UNVERIFIED] Get a specific payment by ID. The /payments path currently returns 404."""
    return await bugcrowd_request("GET", f"/payments/{id}", params=query_params)


# TARGET GROUPS
# NOTE: The Bugcrowd API uses /targets (not /target_groups) as the resource path.
@mcp.tool()
async def get_target_groups(query_params: dict = None):
    """List all targets (bug bounty program target assets). Uses /targets endpoint."""
    return await bugcrowd_request("GET", "/targets", params=query_params)


@mcp.tool()
async def get_target_group(id: str, query_params: dict = None):
    """Get a specific target by ID. Uses /targets/{id} endpoint."""
    return await bugcrowd_request("GET", f"/targets/{id}", params=query_params)


# USERS
# NOTE: /users returns 404 – this path does not exist in the Bugcrowd API.
# The correct path may require a Bugcrowd internal or partner API access tier.
@mcp.tool()
async def get_users(query_params: dict = None):
    """[UNVERIFIED] List users. The /users path is not available on the public Bugcrowd API and currently returns 404."""
    return await bugcrowd_request("GET", "/users", params=query_params)


@mcp.tool()
async def get_user(id: str, query_params: dict = None):
    """[UNVERIFIED] Get a specific user by ID. The /users path is not available on the public Bugcrowd API and currently returns 404."""
    return await bugcrowd_request("GET", f"/users/{id}", params=query_params)


# ENGAGEMENTS
@mcp.tool()
async def get_engagements(query_params: dict = None):
    """List all engagements (bug bounty program engagements/briefs)."""
    return await bugcrowd_request("GET", "/engagements", params=query_params)


@mcp.tool()
async def get_engagement(id: str, query_params: dict = None):
    """Get a specific engagement by ID."""
    return await bugcrowd_request("GET", f"/engagements/{id}", params=query_params)


# ... more tools for other endpoints can be added in the same pattern ...

if __name__ == "__main__":
    mcp.run()
