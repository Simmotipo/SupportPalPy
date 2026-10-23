import os
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP
import supportpal as sp
import re
from html.parser import HTMLParser

class utils:
    BLOCK_TAGS = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}
    SKIP_TAGS = {"img", "script", "style", "head", "svg", "picture"}
    
    class TextExtractor(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.parts = []
            self.skip_depth = 0
    
        def handle_starttag(self, tag, attrs):
            if tag in utils.SKIP_TAGS:
                if tag != "img":  # img is void - no end tag
                    self.skip_depth += 1
            elif tag in utils.BLOCK_TAGS:
                self.parts.append("\n")
    
        def handle_startendtag(self, tag, attrs):
            if tag in utils.BLOCK_TAGS:
                self.parts.append("\n")
    
        def handle_endtag(self, tag):
            if tag in utils.SKIP_TAGS and tag != "img":
                self.skip_depth = max(0, self.skip_depth - 1)
            elif tag in utils.BLOCK_TAGS:
                self.parts.append("\n")
    
        def handle_data(self, data):
            if not self.skip_depth:
                self.parts.append(data)
    
    
    def html_to_text(html: str) -> str:
        """Convert an HTML string to plain text."""
        parser = utils.TextExtractor()
        parser.feed(html or "")
        text = "".join(parser.parts).replace("\xa0", " ")
        text = "\n".join(line.strip() for line in text.splitlines())
        return re.sub(r"\n{3,}", "\n\n", text).strip()

# Initialize FastMCP Server
mcp = FastMCP("SupportPal Helpdesk")

# Configuration via environment variables
sp.URL, sp.TKN = sp.SanitiseUrl(os.getenv("SUPPORTPAL_BASE_URL", "")), os.getenv("SUPPORTPAL_API_TOKEN", "")

ENABLED_FEATURES = [f.strip().upper() for f in os.getenv("ENABLED_FEATURES_CSV", "").split(",") if f.strip()]

@mcp.tool()
async def list_available_features() -> Dict[str, any]:
    """Returns dictionary of features and whether they're enabled in the user's MCP config"""
    return {
        "TICKET_GET": {"desc": "Fetch and search ticket(s), messages on them, statuses, priorities and custom fields", "enabled": "TICKET_GET" in ENABLED_FEATURES},
        "TICKET_EDIT": {"desc": "Edit ticket custom fields", "enabled": "TICKET_EDIT" in ENABLED_FEATURES},
        "TICKET_ADDNOTE": {"desc": "Add new Operator Notes to tickets", "enabled": "TICKET_ADDNOTE" in ENABLED_FEATURES},
        "TICKET_CREATEMESSAGE": {"desc": "Create a message onto a ticket (as draft only!)", "enabled": "TICKET_CREATEMESSAGE" in ENABLED_FEATURES},
        "OPERATOR_GET": {"desc": "Fetch Operator information", "enabled": "OPERATOR_GET" in ENABLED_FEATURES},
        "USER_GET": {"desc": "Fetch User information", "enabled": "USER_GET" in ENABLED_FEATURES},
        "ORGANISATION_GET": {"desc": "Fetch Organisation information", "enabled": "ORGANISATION_GET" in ENABLED_FEATURES},
        "ARTICLE_GET": {"desc": "Fetch and search for selfservice articles", "enabled": "ARTICLE_GET" in ENABLED_FEATURES},
        "ARTICLE_DEL": {"desc": "Delete selfservice articles", "enabled": "ARTICLE_DEL" in ENABLED_FEATURES},
        "ARTICLE_ADD": {"desc": "Create new selfservice articles", "enabled": "ARTICLE_ADD" in ENABLED_FEATURES},
        "SELFSERVEMETA_GET": {"desc": "Fetch metadata regarding selfservice functionality, such as Article Types, Tags, and Categories", "enabled": "SELFSERVEMETA_GET" in ENABLED_FEATURES},
        "SELFSERVEMETA_ADDTAG": {"desc": "Create a new selfservice tag", "enabled": "SELFSERVEMETA_ADDTAG" in ENABLED_FEATURES},
        "SELFSERVEMETA_DELTAG": {"desc": "Delete selfservice tags", "enabled": "SELFSERVEMETA_DELTAG" in ENABLED_FEATURES}
    }

@mcp.tool()
async def search_tickets(
    status_id: Optional[str | List[str]] = None,
    user_id: Optional[str | List[str]] = None,
    search: Optional[str] = None,
    limit: Optional[int] = 20,
    operator_id: Optional[str | List[str]] = None,
    updated_at_min: Optional [int] = None,
    updated_at_max: Optional [int] = None,
    created_at_min: Optional [int] = None,
    created_at_max: Optional [int] = None,
    include_last_reply_info: Optional[bool] = True,
    organisation_id: Optional[str] = None,
    number: Optional[str] = None
) -> Dict[str, Any]:
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    tickets: List[sp.Ticket] = sp.GetTickets(status=status_id, user=user_id, search=search, updated_at_max=updated_at_max, updated_at_min=updated_at_min, created_at_max=created_at_max,created_at_min=created_at_min, limit=limit, assigned=operator_id, number=number, organisation=organisation_id)
    return {
        "tickets": [ticket.to_json(include_last_reply_info) for ticket in tickets]
    }

@mcp.tool()
async def get_ticket_details(ticket_id: int) -> Dict[str, Any]:
    """Retrieve full details, including, status, timesheet, message history for a specific ticket."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    tkt: sp.Ticket = sp.GetTicketById(ticket_id)
    return {
        "ticket": tkt.to_json(in_reply_format=False),
        "timesheet": tkt.GetTimesheet()
    }

@mcp.tool()
async def get_messages_on_ticket(ticket_id: int, limit: Optional[int] = 20, include_drafts: Optional[bool] = False) -> Dict[str, Any]:
    """Retrieve messages on a given ticket."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    messages = sp.GetMessages(ticket_id=ticket_id, limit=limit, include_drafts=include_drafts)
    for message in messages:
        message.purified_text = utils.html_to_text(message.purified_text)
        message.text = None
    return {
        "messages": [msg.to_json() for msg in messages]
    }

async def get_message_n_on_ticket(ticket_id: int, index: int, limit: Optional[int] = 20, include_drafts: Optional[bool] = False) -> Dict[str, Any]:
    """Retrieve Nth message on a given ticket."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "message": sp.GetMessages(ticket_id=ticket_id, limit=None, include_drafts=include_drafts)[index].to_json()
    }

@mcp.tool()
async def create_message_or_note_on_ticket(
    ticket_id: int,
    operator_id: int,
    is_note: bool,
    text: str
    ) -> Dict[str, Any]:
    """Create new new note or message onto a given ticket. Notes are created, while messages are forcibly saved as drafts only: they are never sent to the customer. Users must manually go to the Helpdesk and hit send to ensure they know what they are sending, and to prevent AI error."""
    if is_note:
        if not "TICKET_ADDNOTE" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_ADDNOTE to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    elif not "TICKET_CREATEMESSAGE" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_CREATEMESSAGE to their ENABLED_FEATURES_CSV key if they need to use this functionality"}

    ticket = sp.GetTicketById(ticket_id)
    if not ticket: return {"error": "Ticket wasn't found, or failed to fetch"}
    return {
        "result": ticket.CreateMessage(operator=operator_id, is_note=is_note, is_draft=False if is_note else True, message_text=text).to_json() # We do 'is_draft=False if is_note else True' as, if the ticket is a note, we want to add it to the ticket; if it isn't a note, we need to make sure it is only ever added as a draft and not sent
    }

@mcp.tool()
async def get_operators(
    email: str,
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of operators."""
    if not "OPERATOR_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add OPERATOR_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    operators: List[sp.Operator] = sp.GetOperators(email=email, limit=limit)
    return {
        "operators": [operator.to_json() for operator in operators]
    }

@mcp.tool()
async def get_operator_timesheeting(start_unix: int, operator_id: Optional[int] = None, end_unix: Optional[int] = None) -> Dict[str, Any]:
    """Retrieve a breakdown of a user's timesheet entries in the given window. If an operator_id is provided, it will only look at tickets assigned to the user; if no operator is provided, it will return all timesheeting info (including entries for users on tickets assigned to others)"""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    tkts: List[sp.Ticket] = []
    skip = 0
    batch = sp.GetTickets(assigned=operator_id, updated_at_min=start_unix, updated_at_max=end_unix, limit=25, start=skip)
    while len(batch) == 25:
        for tkt in batch: tkts.append(tkt)
        skip += 25
        batch = sp.GetTickets(assigned=operator_id, updated_at_min=start_unix, updated_at_max=end_unix, limit=25, start=skip)
    for tkt in batch: tkts.append(tkt)

    data = {"tickets": {}, "operators": {}}
    for tkt in tkts:
        if not tkt.number in data['tickets']:
            data['tickets'][tkt.number] = {'id': tkt.id, 'number': tkt.number, 'subject': tkt.subject, 'entries': []}
        sheets = tkt.GetTimesheet()
        for sheet in sheets:
            data['tickets'][tkt.number]['entries'].append({
                'operator_id': sheet.get('user_id'),
                'operator_name': sheet.get('user_name'),
                'start_time': sheet.get('start_time'),
                'duration_s': sheet.get('time'),
                'description': sheet.get('description'),
            })
            if not str(sheet.get('user_id')) in data['operators']:
                data['operators'][str(sheet.get('user_id'))] = {'id': sheet.get('user_id'), 'name': sheet.get('user_name'), 'entries': []}
            data['operators'][str(sheet.get('user_id'))]['entries'].append({
                'ticket_id': tkt.id,
                'ticket_number': tkt.number,
                'ticket_subject': tkt.subject,
                'start_time': sheet.get('start_time'),
                'duration_s': sheet.get('time'),
                'description': sheet.get('description'),
            })
    return data




@mcp.tool()
async def get_users(
    email: str,
    limit: Optional[int] = 20,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    organisation_id: Optional[int] = None
    ) -> Dict[str, Any]:
    """Retrieve list of users."""
    if not "USER_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add USER_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    users: List[sp.User] = sp.GetUsers(email=email, limit=limit, firstname=firstname, lastname=lastname, organisation=organisation_id)
    return {
        "users": [user.to_json() for user in users]
    }

@mcp.tool()
async def get_organisations(
    search: str,
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of organisations."""
    if not "ORGANISATION_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add ORGANISATION_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    orgs: List[sp.Organisation] = sp.GetOrganisations(search=search, limit=limit)
    return {
        "orgs": [org.to_json() for org in orgs]
    }

@mcp.tool()
async def get_statuses(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of valid ticket statuses."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    statuses: List[sp.Status] = sp.GetStatuses(limit=limit)
    return {
        "statuses": [status.to_json() for status in statuses]
    }

@mcp.tool()
async def get_priorities(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of valid ticket priorities."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    priorities: List[sp.Priority] = sp.GetPriorities(limit=limit)
    return {
        "priorities": [priority.to_json() for priority in priorities]
    }

@mcp.tool()
async def get_custom_fields(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of custom ticket fields including, if relevant, the options available (for option-select types)."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    custom_properties: List[sp.CustomField] = sp.GetCustomFields(limit=limit)
    return {
        "custom_fields": [custom_property.to_json() for custom_property in custom_properties]
    }

@mcp.tool()
async def get_articles(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of articles."""
    if not "ARTICLE_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add ARTICLE_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    articles: List[sp.Article] = sp.GetArticles(limit=limit)
    return {
        "articles": [article.to_json() for article in articles]
    }

@mcp.tool()
async def get_article(
    id: int,
    ) -> Dict[str, Any]:
    """Retrieve article by ID."""
    if not "ARTICLE_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add ARTICLE_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "article": sp.GetArticleById(id).to_json()
    }

@mcp.tool()
async def search_articles(
    term: str,
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Search for articles matching a given term. The SupportPal search endpoint is remarkably basic, and requires exact syntax matches of the provided term specifically, so - if possible - aim to be overly broad in your terms. Typically a single word works best if possible."""
    if not "ARTICLE_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add ARTICLE_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    articles: List[sp.Article] = sp.SearchArticles(term=term, limit=limit)
    return {
        "articles": [article.to_json() for article in articles]
    }

@mcp.tool()
async def delete_article(
    id: int,
    ) -> Dict[str, Any]:
    """Delete article by ID."""
    if not "ARTICLE_DEL" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add ARTICLE_DEL to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "reply": sp.DeleteArticle(id).to_json()
    }

@mcp.tool()
async def create_article(
    author_user_id: int,
    title: str,
    excerpt: Optional[str],
    article_body_html: str,
    category_ids: List[int],
    tag_names: Optional[List[str]],
    published: Optional[bool] = False,
    public: Optional[bool] = False,
    pinned: Optional[bool] = False
    ) -> Dict[str, Any]:
    """Create new article."""
    if not "ARTICLE_ADD" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add ARTICLE_ADD to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    article: sp.Article = sp.Article({
        "author_id": author_user_id,
        "title": title,
        "excerpt": excerpt,
        "text": article_body_html,
        "category": category_ids,
        "tag": tag_names,
        "published": published,
        "protected": not public,
        "pinned": pinned
    })

    return {
        "article": sp.CreateArticle(article)
    }

@mcp.tool()
async def get_categories(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of article/selfservice categories."""
    if not "SELFSERVEMETA_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    categories: List[sp.Category] = sp.GetCategories(limit=limit)
    return {
        "categories": [category.to_json() for category in categories]
    }

@mcp.tool()
async def get_category(
    id: int,
    ) -> Dict[str, Any]:
    """Retrieve article/selfservice category by ID."""
    if not "SELFSERVEMETA_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "category": sp.GetCategoryById(id).to_json()
    }

@mcp.tool()
async def get_types(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of article/selfservice types."""
    if not "SELFSERVEMETA_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    types: List[sp.ArticleType] = sp.GetTypes(limit=limit)
    return {
        "types": [type.to_json() for type in types]
    }

@mcp.tool()
async def get_type(
    id: int,
    ) -> Dict[str, Any]:
    """Retrieve article/selfservice type by ID."""
    if not "SELFSERVEMETA_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "type": sp.GetTypeById(id).to_json()
    }

@mcp.tool()
async def get_ticket_tags(
    limit: Optional[int] = 20,
    skip: Optional[int] = 0
    ) -> Dict[str, Any]:
    """Retrieve list of ticket tags."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    tags: List[sp.TicketTag] = sp.GetTicketTags(limit=limit, skip=skip)
    return {
        "tags": [tag.to_json() for tag in tags]
    }

@mcp.tool()
async def get_ticket_tag(
    id: int,
    ) -> Dict[str, Any]:
    """Retrieve ticket tag by ID."""
    if not "TICKET_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "tag": sp.GetTicketTagById(id).to_json()
    }

@mcp.tool()
async def get_selfserve_tags(
    limit: Optional[int] = 20
    ) -> Dict[str, Any]:
    """Retrieve list of article/selfservice tags."""
    if not "SELFSERVEMETA_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    tags: List[sp.ArticleTag] = sp.GetSelfServiceTags(limit=limit)
    return {
        "tags": [tag.to_json() for tag in tags]
    }

@mcp.tool()
async def get_selfserve_tag(
    id: int,
    ) -> Dict[str, Any]:
    """Retrieve article/selfservice tag by ID."""
    if not "SELFSERVEMETA_GET" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_GET to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "tag": sp.GetSelfServiceTagById(id).to_json()
    }

@mcp.tool()
async def create_selfserve_tag(
    name: str,
    slug: Optional[str]
    ) -> Dict[str, Any]:
    """Create new tag."""
    if not "SELFSERVEMETA_ADDTAG" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_ADDTAG to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    tag: sp.ArticleTag = sp.ArticleTag({
        "name": name,
        "slug": slug
    })

    return {
        "article": sp.CreateSelfServiceTag(tag)
    }

@mcp.tool()
async def delete_selfserve_tag(
    id: int,
    ) -> Dict[str, Any]:
    """Delete selfservice tag by ID."""
    if not "SELFSERVEMETA_DELTAG" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add SELFSERVEMETA_DELTAG to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    return {
        "reply": sp.DeleteSelfServiceTag(id).to_json()
    }

@mcp.tool()
async def set_custom_field_value_on_ticket(
    ticket_id: int,
    custom_field_id: int,
    custom_field_value: str
    ) -> Dict[str, Any]:
    """Set the value of a specific Custom Field on a given ticket to the provided value"""
    if not "TICKET_EDIT" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_EDIT to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    ticket: sp.Ticket = sp.GetTicketById(ticket_id)
    found_field: bool = False
    for cfv in ticket.custom_field_values:
        if cfv.customfield_id == custom_field_id:
            cfv.value = custom_field_value
            found_field = True
            break
    if not found_field:
        field_to_update = sp.CustomFieldValue({"field_id": custom_field_id, "ticket_id": ticket_id, "value": custom_field_value})
        ticket.custom_field_values.append(field_to_update)

    return {"response": ticket.Update()}

@mcp.tool()
async def edit_ticket(
    ticket_id: int,
    assigned_operator_ids: Optional[List[int]],
    status_id: Optional[int],
    priority_id: Optional[int],
    duetime_unix: Optional[int],
    subject: Optional[str],
    tags: Optional[list[int]],
    user_id: Optional[int]
    ) -> Dict[str, Any]:
    """Update basic ticket metadata"""
    if not "TICKET_EDIT" in ENABLED_FEATURES: return {"error": "This feature is not enabled in the MCP config, and so permission to run it is denied. Advise the user to add TICKET_EDIT to their ENABLED_FEATURES_CSV key if they need to use this functionality"}
    ticket: sp.Ticket = sp.GetTicketById(ticket_id)

    if assigned_operator_ids:
        operators = []
        for operator_id in assigned_operator_ids:
            operators.append(sp.GetOperatorById(operator_id))
        ticket.assigned = operators
    if status_id: ticket.status = sp.GetStatusById(status_id)
    if priority_id: ticket.priority = sp.GetPriorityById(priority_id)
    if duetime_unix: ticket.duetime = duetime_unix
    if subject: ticket.subject = subject
    if tags: ticket.tags = [str(tag) for tag in tags]
    if user_id: ticket.user = sp.User({"id": user_id})

    return {"response": ticket.Update()}

    
if __name__ == "__main__":
    mcp.run()
