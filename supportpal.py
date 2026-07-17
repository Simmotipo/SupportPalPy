## Supportpal API Lib, by Simmotipo

from typing import List
import json
from dateutil import parser

import requests
from requests.auth import HTTPBasicAuth

URL = ""
TKN = ""

class utils:
    def GET(url, tkn):
        response = requests.get(
            url, 
            auth=HTTPBasicAuth(tkn, '')
        )
        return response

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
        self.last_active_at: str = data.get('last_active_at')
        self.created_at: str = data.get('created_at')
        self.updated_at: str = data.get('updated_at')
        self.organisation_access_level: int = data.get('organisation_access_level')
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
            "formatted_name": self.formatted_name,
            "last_active_at": self.last_active_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "organisation_access_level": self.organisation_access_level
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
        self.user_id: str = data.get('user_id')
        self.user_name: str = data.get('user_name')
        self.is_from_customer: int = data.get('by') # 0 = operator; 1 = customer
        self.is_note: int = data.get('type') # 0 = message; 1 = note
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

def GetTickets(filter: int = None, filter_operator: Operator | int = None, search: str = None, number: str = None, status: str | Status = None, priority: str | Priority = None, user: User | List[User] | str = None, user_email: str = None, organisation: Organisation | str = None, assigned: Operator | List[Operator] | str = None, internal: bool = None, start: int = None, created_at_min: int | str = None, created_at_max: int | str = None, updated_at_min: int | str = None, updated_at_max: int | str = None, limit: int = 50) -> List[Ticket]:
    target = f"{URL}/ticket/ticket?limit={limit}"
    if not filter == None:
        target += f"&filter={filter}"
    if not filter == filter_operator:
        if isinstance(filter_operator, Operator):
            target += f"&filter_operator={filter_operator.id}"
        else:
            target += f"&filter_operator={filter_operator}"
    if not search == None:
        target += f"&search={search}"
    if not number == None:
        target += f"&number={number}"
    if not status == None:
        if isinstance(status, Status):
            target += f"&status={status.id}"
        else:
            target += f"&status={status}"
    if not priority == None:
        if isinstance(priority, Priority):
            target += f"&priority={priority.id}"
        else:
            target += f"&priority={priority}"
    if not user == None:
        if isinstance(user, User):
            target += f"&user={user.id}"
        elif isinstance(user, List[User]):
            target += f"&user="
            for eachUser in user:
                target += eachUser.id + ","
            target = target[0:len(target)-2]
        else:
            target += f"&user={user}"
    if not user_email == None:
        target += f"&user_email={user_email}"
    if not organisation == None:
        if isinstance(organisation, Organisation):
            target += f"&organisation={organisation.id}"
        else:
            target += f"&organisation={organisation}"
    if not assigned == None:
        if isinstance(assigned, Operator):
            target += f"&assigned={user.id}"
        elif isinstance(user, List[Operator]):
            target += f"&assigned="
            for eachUser in user:
                target += eachUser.id + ","
            target = target[0:len(target)-2]
        else:
            target += f"&assigned={user}"
    if not internal == None:
        target += f"&internal={int(internal)}"
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
    for ticket in data:
        results.append(Ticket(ticket))
    return results

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
    target = f"{URL}/api/ticket/status?limit={limit}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for obj in data:
        results.append(Status(obj))
    return results

def GetStatusById(id: int | str) -> Status:
    target = f"{URL}/api/ticket/status/{id}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    return Status(data)

def GetPriorities(limit: int = 50) -> List[Priority]:
    target = f"{URL}/api/ticket/priority?limit={limit}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for obj in data:
        results.append(Priority(obj))
    return results

def GetPriorityById(id: int | str) -> Priority:
    target = f"{URL}/api/ticket/priority/{id}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    return Priority(data)

def GetCustomFields(limit: int = 50) -> List[CustomField]:
    target = f"{URL}/api/ticket/customfield?limit={limit}"
    data = json.loads(utils.GET(target, TKN).text)['data']
    results = []
    for obj in data:
        results.append(CustomField(obj))
    return results

def GetCustomFieldById(id: int | str) -> CustomField:
        target = f"{URL}/api/ticket/customfield/{id}"
        data = json.loads(utils.GET(target, TKN).text)['data']
        return CustomField(data)
