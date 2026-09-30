import os
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
import supportpal as sp

# Initialize FastMCP Server
mcp = FastMCP("SupportPal Helpdesk")

# Configuration via environment variables
sp.URL, sp.TKN = sp.SanitiseUrl(os.getenv("SUPPORTPAL_BASE_URL", "")), os.getenv("SUPPORTPAL_API_TOKEN", "")

@mcp.tool()
def search_tickets(
    status_id: Optional[str | List[str]] = None,
    user_id: Optional[str | List[str]] = None,
    search: Optional[str] = None,
    limit: Optional[int] = 20,
    operator_id: Optional[str | List[str]] = None,
    updated_at_min: Optional [int] = None,
    updated_at_max: Optional [int] = None,
    created_at_min: Optional [int] = None,
    created_at_max: Optional [int] = None,
    include_last_reply_info: Optional[bool] = True
) -> Dict[str, Any]:
    tickets: List[sp.Ticket] = sp.GetTickets(status=status_id, user=user_id, search=search, updated_at_max=updated_at_max, updated_at_min=updated_at_min, created_at_max=created_at_max,created_at_min=created_at_min, limit=limit, assigned=operator_id)
    return {
        "tickets": [ticket.to_json(include_last_reply_info) for ticket in tickets]
    }

@mcp.tool()
async def get_ticket_details(ticket_id: int) -> Dict[str, Any]:
    """Retrieve full details, status, and message history for a specific ticket."""
    return {
        "ticket": sp.GetTicketById(ticket_id).to_json()
    }

@mcp.tool()
async def get_messages_on_ticket(ticket_id: int, limit: Optional[int] = 20) -> Dict[str, Any]:
    """Retrieve messages on a given ticket."""
    return {
        "messages": [msg.to_json() for msg in sp.GetMessages(ticket_id=ticket_id, limit=limit)]
    }

async def get_message_text_on_ticket(ticket_id: int, limit: Optional[int] = 20) -> Dict[str, Any]:
    """Retrieve messages on a given ticket (excluding images and attachments, retaining purified_text field instead)."""
    messages: List[sp.Message] = sp.GetMessages(ticket_id=ticket_id, limit=limit)
    i = 0
    while i < len(messages):
        messages[i].excerpt = None
        messages[i].text = None
        i += 1
    return {
        "messages": [msg.to_json() for msg in messages]
    }

@mcp.tool()
async def get_operators(
    email: str,
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of operators."""
    operators: List[sp.Operator] = sp.GetOperators(email=email, limit=limit)
    return {
        "operators": [operator.to_json() for operator in operators]
    }

@mcp.tool()
async def get_statuses(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of valid ticket statuses."""
    statuses: List[sp.Status] = sp.GetStatuses(limit=limit)
    return {
        "statuses": [status.to_json() for status in statuses]
    }

@mcp.tool()
async def get_priorities(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of valid ticket priorities."""
    priorities: List[sp.Priority] = sp.GetPriorities(limit=limit)
    return {
        "priorities": [priority.to_json() for priority in priorities]
    }

if __name__ == "__main__":
    mcp.run()
