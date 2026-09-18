## Supportpal API Lib, by Simmotipo

from __future__ import annotations
from typing import List, Union, Literal
from enum import IntEnum
import json
from dateutil import parser

import requests
from requests.auth import HTTPBasicAuth

URL = ""
TKN = ""

class utils:
    def GET(url, tkn, params=None):
        return requests.get(
            url,
            auth=HTTPBasicAuth(tkn, ''),
            params=params
        )

    def POST(url, tkn, data=None):
        response = requests.post(
            url, 
            auth=HTTPBasicAuth(tkn, ''), 
            json=data
        )
        return response

    def PUT(url, tkn, data=None):
        response = requests.put(
            url, 
            auth=HTTPBasicAuth(tkn, ''), 
            json=data
        )
        return response

    def DELETE(url, tkn):
        response = requests.delete(
            url, 
            auth=HTTPBasicAuth(tkn, '')
        )
        return response
    
    def CLEANJSON(json):
        return json

    def _resolve_id(val: any) -> any:
        """Helper to extract an ID attribute or return the raw value."""
        return getattr(val, "id", val)

    def _format_list_or_val(val: any) -> str:
        """Formats single entities or lists into comma-separated ID strings."""
        if isinstance(val, (list, tuple)):
            return ",".join(str(utils._resolve_id(item)) for item in val)
        return str(utils._resolve_id(val))

    def _to_timestamp(val: Union[int, str, None]) -> int | None:
        """Parses timestamps safely."""
        if val is None or isinstance(val, int):
            return val
        return int(parser.parse(val, dayfirst=True).timestamp())

class Enums:
    class MessageType(IntEnum):
        """0 = message; 1 = note"""
        MESSAGE = 0
        NOTE = 1

class Operator:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)
        self.id: int = data.get('id')
        self.firstname: str = data.get('firstname')
        self.lastname: str = data.get('lastname')
        self.email: str = data.get('email')
        self.active: int = data.get('active') or 0
        self.groups: List[OperatorGroup] = []
        self.formatted_name: str = data.get('formatted_name')
        for group in data.get('groups') or {}:
            self.groups.append(OperatorGroup(group))

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "active": self.active,
            "groups": [group.to_json() for group in self.groups]
        })
    
class OperatorGroup:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)

        self.id: int = data.get('id')
        self.name: str = data.get('name') or "Unnamed Group"
        self.description: str = data.get('description') or ""
        self.colour: str = data.get('colour') or "#777777"
        self.administrator: int = data.get('administrator') or 0

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "colour": self.colour,
            "administrator": self.administrator
        })

class User:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)

        self.id: int = data.get('id')
        self.firstname: str = data.get('firstname')
        self.lastname: str = data.get('lastname')
        self.email: str = data.get('email')
        self.active: int = data.get('active')
        self.organisation_id: int = data.get('organisation_id')
        self.organisation_access_level: int = data.get('organisation_access_level')
        self.organisation_notifications: int = data.get('organisation_notifications')
        self.formatted_name: str = data.get('formatted_name')
        if not data.get('organisation') == None:
            self.organisation: Organisation = Organisation(data.get('organisation'))

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "active": self.active,
            "organisation_id": self.organisation_id,
            "organisation_access_leve": self.organisation_access_level,
            "organisation_notifications": self.organisation_notifications,
            "formatted_name": self.formatted_name
        })
    
class Organisation:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)

        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.users: List[User] = []
        if data.get('users'):
            for user in data.get('users'):
                self.users.append(User(user))

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "name": self.name
        })
    
class Ticket:
    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        self.id: int = data.get('id')
        self.number: str = data.get('number')
        self.user: User = User(data.get('user'))
        self.status: Status = Status(data.get('status'))
        self.priority: Priority = Priority(data.get('priority'))
        self.sla: SLAPlan = SLAPlan(data.get('slaplan'))
        self.subject: str = data.get('subject')
        self.duetime: int = data.get('due_time')
        self.resolved_time: int = data.get('resolved_time')
        self.reopened_time: int = data.get('reopened_time')
        self.cc: List[str] = data.get('cc')
        self.locked: int = data.get('locked')
        self.internal: int = data.get('internal')
        self.merged: int = data.get('merged')
        self.messages_count: int = data.get('messages_count')
        self.notes_count: int = data.get('notes_count')
        self.has_attachments: int = data.get('has_attachments')
        self.has_draft: bool = data.get('has_draft')
        self.last_reply_time: int = data.get('last_reply_time')
        self.last_message_time: int = data.get('last_message_time')
        self.last_reply_id: int = data.get('last_reply_id')
        self.last_message_id: int = data.get('last_message_id')
        self.created_at: int = data.get('created_at')
        self.updated_at: int = data.get('updated_at')
        self.deleted_at: int = data.get('deleted_at')
        self.frontend_url: str = data.get('frontend_url')
        self.operator_url: str = data.get('operator_url')
        self.assigned: List[Operator] = []
        for operator in data.get('assigned'):
            self.assigned.append(Operator(operator))
        self.custom_field_values: List[CustomFieldValue] = []
        for customfieldvalue in data.get('customfields'):
            self.custom_field_values.append(CustomFieldValue(customfieldvalue))
        self.last_reply: Message = Message(data.get('last_reply'))
        self.tags: List = data.get('tags')

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def GetTimesheet(self, user: int | User = None) -> json:
        args = "&"
        if user:
            if isinstance(user, int):
                args += f"user_id={user}&"
            elif isinstance(user, User):
                args += f"user_id={user.id}&"
        target = f"{URL}/plugin/timetracking/timelog?ticket_id={self.id}{args[:-1]}"
        return json.loads(utils.GET(target, TKN).text)['data']

    def CreateTimesheetEntry(self, user: int | User, startunix, duration_seconds, description: str = None, billable: bool = False) -> json:
        data = {
            "ticket_id": self.id,
            "user_id": user if isinstance(user, int) else user.id,
            "start_time": startunix,
            "time": duration_seconds,
            "description": description if not description == None else None,
            "billable": billable,
            "status": 2
        }
        target = f"{URL}/plugin/timetracking/timelog"
        return json.loads(utils.POST(target, TKN, data).text)

    def CreateMessage(self, operator: int | Operator, message_text: str, message_on_behalf_of: int | User = None) -> Message | str:
        data = {
            "ticket_id": self.id,
            "user_id": operator.id if isinstance(operator, Operator) else operator if isinstance(operator, int) else None,
            "on_behalf_of": message_on_behalf_of.id if isinstance(message_on_behalf_of, User) else message_on_behalf_of if isinstance(message_on_behalf_of, int) else None,
            "text": message_text
        }

        target = f"{URL}/ticket/message"
        resp = utils.POST(target, TKN, data)
        return Message(json.loads(resp.text)['data']) if resp.status_code == 200 else resp.text

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "number": self.number,
            "user_id": self.user.id,
            "status_id": self.status.id,
            "priority_id": self.priority.id,
            "sla_plan_id": self.sla.id or None,
            "duetime": self.duetime,
            "cc": self.cc,
            "locked": self.locked,
            "internal": self.internal,
            "merged": self.merged,
            "assigned": [op.to_json() for op in self.assigned],
            "customfields": [cf.to_json() for cf in self.custom_field_values]
        })

class Message:
    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        self.id: int = data.get('id')
        self.ticket_id: int = data.get('ticket_id')
        self.user_id: int = data.get('user_id')
        self.user_name: str = data.get('user_name')
        self.is_from_customer: Literal[0, 1] = data.get('by') # 0 = operator; 1 = customer
        self.is_note: Literal[0, 1] = data.get('type')
        self.excerpt: str = data.get('excerpt')
        self.text: str = data.get('text')
        self.purified_text: str = data.get('purified_text')
        self.is_draft: int = data.get('is_draft') # 0 = no; 1 = yes
        self.created_at: int = data.get('created_at')
        self.updated_at: int = data.get('updated_at')
    
    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "by": self.is_from_customer,
            "type": self.is_note,
            "excerpt": self.excerpt,
            "text": self.text,
            "purified_text": self.purified_text,
            "is_draft": self.is_draft
        })

class CustomFieldValue:
    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        self.id: int = data.get('id')
        self.customfield_id: int = data.get('field_id')
        self.ticket_id: int = data.get('ticket_id')
        self.value = data.get('value')
        self.encrypted: int = data.get('encrypted')
    
    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "field_id": self.customfield_id,
            "ticket_id": self.ticket_id,
            "value": self.value,
            "encrypted": self.encrypted
        })

class CustomFieldOption:
    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        self.id: int = data.get('id')
        self.customfield_id: int = data.get('field_id')
        self.order: int = data.get('order')
        self.value = data.get('value')
        self.created_at: int = data.get('created_at')
        self.updated_at: int = data.get('updated_at')
    
    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "field_id": self.customfield_id,
            "ticket_id": self.ticket_id,
            "value": self.value,
            "encrypted": self.encrypted
        })
    
class CustomField:
    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.description: str = data.get('description')
        self.type: int = data.get('type')
        self.required: int = data.get('required')
        self.public: int = data.get('public')
        self.options: List[CustomFieldOption] = []
        for option in data.get('options'): self.options.append(CustomFieldOption(option))

    
    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "required": self.required,
            "public": self.public
        })

class SLAPlan:
    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        elif data == None:
            data = {}
        self.id = data.get('id') or None
        self.name = data.get('name')
        self.description = data.get('description')
        self.all_hours = data.get('all_hours')
    
    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "all_hours": self.all_hours
        })
    
class StatusPriority:
    def __init__(self, data):
        if isinstance(data, str):
            data = json.loads(data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.colour = data.get('colour')
    
    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return utils.CLEANJSON({
            "id": self.id,
            "name": self.name,
            "colour": self.colour
        })
    
class Status(StatusPriority):
    pass

class Priority(StatusPriority):
    pass

def SanitiseUrl(URL):
    if not "https://" in URL:
        URL = f"https://{URL}"
    if not "api" in URL:
        if not URL.endswith('/'):
            URL += '/'
        URL += 'api'
    if URL.endswith('/'):
        URL = URL[0:len(URL)-2]
    return URL

def GetTickets(
    filter: int = None,
    filter_operator: Operator | int = None,
    search: str = None,
    number: str = None,
    status: str | Status | List[str] | List[Status] = None,
    priority: str | Priority = None,
    user: User | List[User] | str = None,
    user_email: str = None,
    organisation: Organisation | str | List[Organisation] | List[str] = None,
    assigned: Operator | List[Operator] | str = None,
    internal: bool = None,
    start: int = None,
    created_at_min: int | str = None,
    created_at_max: int | str = None,
    updated_at_min: int | str = None,
    updated_at_max: int | str = None,
    limit: int = 50,
    order_column: str = None,
    order_direction: str = None,
) -> List[Ticket]:

    # Build params dictionary directly
    params = {"limit": limit}

    mapping = {
        "filter": filter,
        "filter_operator": utils._resolve_id(filter_operator) if filter_operator is not None else None,
        "search": search,
        "number": number,
        "status": (
            [utils._resolve_id(s) for s in status]
            if isinstance(status, (list, tuple, set))
            else utils._resolve_id(status)
        ) if status is not None else None,
        "priority": utils._resolve_id(priority) if priority is not None else None,
        "user": utils._format_list_or_val(user) if user is not None else None,
        "user_email": user_email,
        "organisation": utils._format_list_or_val(organisation) if organisation is not None else None,
        "assigned": utils._format_list_or_val(assigned) if assigned is not None else None,
        "internal": int(internal) if internal is not None else None,
        "start": start,
        "created_at_min": utils._to_timestamp(created_at_min),
        "created_at_max": utils._to_timestamp(created_at_max),
        "updated_at_min": utils._to_timestamp(updated_at_min),
        "updated_at_max": utils._to_timestamp(updated_at_max),
        "order_column": order_column,
        "order_direction": order_direction,
    }

    # Prune unset parameters
    params.update({k: v for k, v in mapping.items() if v is not None})
    response = utils.GET(f"{URL}/ticket/ticket", TKN, params=params)
    data = response.json().get("data", [])
    return [Ticket(ticket) for ticket in data]

def GetTicketById(id: int) -> Ticket:
    target = f"{URL}/ticket/ticket/{id}"
    return Ticket(json.loads(utils.GET(target, TKN).text)['data'])

def GetMessages(ticket_id: int = None, is_from_customer: bool = None, is_note: bool = None, include_drafts: bool = None, start: int = None, created_at_min: int | str = None, created_at_max: int | str = None, updated_at_min: int | str = None, updated_at_max: int | str = None, limit: int = 50) -> List[Message]:
    target = f"{URL}/ticket/message?limit={limit}"
    if not ticket_id == None:
        target += f"&ticket_id={ticket_id}"
    if is_from_customer is not None: target += f"by={int(is_from_customer)}"
    if is_note is not None: target += f"type={int(is_note)}"
    if include_drafts is not None: target += f"include_draft={int(include_drafts)}"
    if not start == None:
        target += f"&start={start}"
    if not updated_at_max == None:
        if isinstance(updated_at_max, int):
            target += f"&updated_at_max={updated_at_max}"
        else:
            target += f"&updated_at_max={int(parser.parse(updated_at_max, dayfirst=True).timestamp())}"
    if not updated_at_min == None:
        if isinstance(updated_at_min, int):
            target += f"&updated_at_min={updated_at_min}"
        else:
            target += f"&updated_at_min={int(parser.parse(updated_at_min, dayfirst=True).timestamp())}"
    if not created_at_max == None:
        if isinstance(created_at_max, int):
            target += f"&created_at_max={created_at_max}"
        else:
            target += f"&created_at_max={int(parser.parse(created_at_max, dayfirst=True).timestamp())}"
    if not created_at_min == None:
        if isinstance(created_at_min, int):
            target += f"&created_at_min={created_at_min}"
        else:
            target += f"&created_at_min={int(parser.parse(created_at_min, dayfirst=True).timestamp())}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for msg in data:
        results.append(Message(msg))
    return results

def GetMessageById(id: int) -> Message:
    target = f"{URL}/ticket/message/{id}"
    return Message(json.loads(utils.GET(target, TKN).text)['data'])

def GetOperators(email: str = None, limit: int = 50) -> List[Operator]:
    target = f"{URL}/user/operator?limit={limit}"
    if not email == None:
        target += f"&email={email}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for user in data:
        results.append(Operator(user))
    return results

def GetOperatorById(id: int) -> Operator:
    target = f"{URL}/user/operator/{id}"
    return Operator(json.loads(utils.GET(target, TKN).text)['data'])

def GetOrganisations(search: str = None, limit: int = 50) -> List[Organisation]:
    target = f"{URL}/user/organisation?limit={limit}"
    if not search == None:
        target += f"&search={search}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for org in data:
        results.append(Organisation(org))
    return results

def GetOrganisationById(id: int | str) -> Organisation:
    target = f"{URL}/user/organisation/{id}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    return Organisation(data)

def GetUsers(search: str = None, firstname: str = None, lastname: str = None, email: str = None, organisation: int | str | Organisation = None, limit: int = 50) -> List[User]:
    target = f"{URL}/user/user?limit={limit}"
    if not search == None:
        target += f"&search={search}"
    if not firstname == None:
        target += f"&firstname={firstname}"
    if not lastname == None:
        target += f"&lastname={lastname}"
    if not email == None:
        target += f"&email={email}"
    if not organisation == None:
        if isinstance(organisation, int):
            target += f"&organisation_id={organisation}"
        elif isinstance(organisation, str):
            try:
                target += f"&organisation_id={int(organisation)}"
            except:
                target += f"&organisation_name={organisation}"
        else:
            target += f"&organisation_id={organisation.id}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for user in data:
        results.append(User(user))
    return results

def GetUserById(id: int) -> User:
    target = f"{URL}/user/user/{id}"
    return User(json.loads(utils.GET(target, TKN).text)['data'])

def GetStatuses(limit: int = 50) -> List[Status]:
    target = f"{URL}/ticket/status?limit={limit}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for obj in data:
        results.append(Status(obj))
    return results

def GetStatusById(id: int | str) -> Status:
    target = f"{URL}/ticket/status/{id}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    return Status(data)

def GetPriorities(limit: int = 50) -> List[Priority]:
    target = f"{URL}/ticket/priority?limit={limit}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for obj in data:
        results.append(Priority(obj))
    return results

def GetPriorityById(id: int | str) -> Priority:
    target = f"{URL}/ticket/priority/{id}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    return Priority(data)

def GetCustomFields(limit: int = 50) -> List[CustomField]:
    target = f"{URL}/ticket/customfield?limit={limit}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for obj in data:
        results.append(CustomField(obj))
    return results

def GetCustomFieldById(id: int | str) -> CustomField:
        target = f"{URL}/ticket/customfield/{id}"
        data = json.loads(utils.GET(target, TKN).text)['data']
        return CustomField(data)

def CreateTicket(department: int, assignees: list[int | Operator], internal: bool, subject: str, message_text: str, priority: int | Priority, status: int | Status, user: int | User = None, message_on_behalf_of: int | User = None) -> Ticket | str:
    """Returns instance of Ticket if successful, or response text as string if fails"""
    payload = {
        "department": department,
        "status": status.id if isinstance(status, Status) else status,
        "internal": internal,
        "assignedto": [assignee.id if isinstance(assignee, Operator) else assignee for assignee in assignees], # API expects an array for assignedto
        "subject": subject,
        "text": message_text,
        "on_behalf_of": message_on_behalf_of.id if isinstance(message_on_behalf_of, User | Operator) else message_on_behalf_of if isinstance(message_on_behalf_of, int) else None,
        "priority": priority.id if isinstance(priority, Priority) else priority,
        "user": user.id if isinstance(user, User) else user
    }

    payload = utils.CLEANJSON(payload) # Remove None / null values
    target = f"{URL}/ticket/ticket"
    resp = utils.POST(target, TKN, payload)
    return Ticket(json.loads(resp.text)['data']) if resp.status_code == 200 else resp.text
