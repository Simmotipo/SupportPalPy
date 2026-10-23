## Supportpal API Lib, by Simmotipo
### Modified 23-10-26 18:04

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
    
    def CLEANJSON(d):
        if isinstance(d, dict):
            return {k: utils.CLEANJSON(v) for k, v in d.items() if v not in [None, "None", "none", "null"]}
        elif isinstance(d, list):
            return [utils.CLEANJSON(v) for v in d if v not in [None, "None", "none", "null"]]
        else:
            return d

class Category:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)

        self.id: int = data.get('id')
        self.type_id: int = data.get('type_id')
        self.parent_id: int = data.get('parent_id')
        self.name: str = data.get('name')
        self.slug: str = data.get('slug')
        self.public: bool = data.get('public')
        self.parent_public: bool = data.get('parent_public')
        self.created_at: int = data.get('created_at')
        self.updated_at: int = data.get('updated_at')
        self.frontend_url: str = data.get('frontend_url')

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return utils.CLEANJSON({
            'id': self.id,
            'type_id': self.type_id,
            'parent_id': self.parent_id,
            'name': self.name,
            'slug': self.slug,
            'public': int(self.public),
            'parent_public': int(self.parent_public),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'frontend_url': self.frontend_url
        })

class ArticleType:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)

        self.id: int = data.get('id')
        self.brand_id: int = data.get('brand_id')
        self.name: str = data.get('name')
        self.slug: str = data.get('slug')
        self.description: str = data.get('description')
        self.order: int = data.get('order')
        self.enabled: bool = data.get('enabled')
        self.protected: bool = data.get('protected')
        self.internal: bool = data.get('internal')
        self.is_external_link: bool = data.get('content')
        self.view: int = data.get('view')
        self.icon: str = data.get('icon')
        self.icon_label: str = data.get('icon_label')
        self.article_ordering: int = data.get('article_ordering')
        self.show_on_dashboard: bool = data.get('show_on_dashboard')
        self.external_link: str = data.get('external_link')

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return utils.CLEANJSON({
            'id': self.id,
            'brand_id': self.brand_id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'order': self.order,
            'enabled': int(self.enabled),
            'protected': int(self.protected),
            'internal': int(self.internal),
            'content': int(self.is_external_link),
            'view': self.view,
            'icon': self.icon,
            'icon_label': self.icon_label,
            'article_ordering': self.article_ordering,
            'show_on_dashboard': int(self.show_on_dashboard) if self.show_on_dashboard else None,
            'external_link': self.external_link,
        })

class ArticleTag:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)

        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.slug: str = data.get('slug')

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return utils.CLEANJSON({
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        })

class TicketTag:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)

        self.id: int = data.get('id')
        self.name: str = data.get('name')
        self.colour: str = data.get('colour')

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return utils.CLEANJSON({
            'id': self.id,
            'name': self.name,
            'colour': self.colour
        })

class Article:
    def __init__(self, data: dict | str):
        if isinstance(data, str):
            data = json.loads(data)
        self.id: int = data.get('id')
        self.author_id: int = data.get('author_id')
        self.title: str = data.get('title')
        self.slug: str = data.get('slug')
        self.excerpt: str = data.get('excerpt')
        self.text: str = data.get('text')
        self.published: bool = data.get('published')
        self.protected: bool = data.get('protected')
        self.pinned: bool = data.get('pinned')
        self.types: List[ArticleType] = [ArticleType(d) for d in data.get('types', {})]
        self.tags: List[ArticleTag | str] = [ArticleTag(t) if isinstance(t, dict) else ArticleTag({"name": t}) for t in data.get('tag', {})]
        self.attachments = data.get('attachments')
        self.category_ids: List[int] = data.get('category')

    def __str__(self):
        return json.dumps(self.to_json())
    
    def __repr__(self):
        return json.dumps(self.to_json())
    
    def to_json(self):
        return utils.CLEANJSON({
            'id': self.id,
            'author_id': self.author_id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'text': self.text,
            'published': int(self.published),
            'protected': int(self.protected),
            'pinned': int(self.pinned),
            'types': [t.to_json() for t in self.types],
            'tag': [t.name if isinstance(t, ArticleTag) else t for t in self.tags],
            'attachments': self.attachments,
            'category': self.category_ids
        })

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
        self.tags: List[TicketTag | str] = [ArticleTag(t) if isinstance(t, dict) else ArticleTag({"name": t}) for t in data.get('tag', {})]

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

    def CreateMessage(self, operator: int | Operator, message_text: str, message_on_behalf_of: int | User = None, is_note: bool = False, is_draft: bool = False) -> 'Message | str':
        data = {
            "ticket_id": self.id,
            "user_id": operator.id if isinstance(operator, Operator) else operator if isinstance(operator, int) else None,
            "on_behalf_of": message_on_behalf_of.id if isinstance(message_on_behalf_of, User) else message_on_behalf_of if isinstance(message_on_behalf_of, int) else None,
            "text": message_text,
            "message_type": 1 if is_note else 0,
            "is_draft": 1 if is_draft else 0,
        }

        target = f"{URL}/ticket/message"
        resp = utils.POST(target, TKN, data)
        return Message(json.loads(resp.text)['data']) if resp.status_code == 200 else resp.text

    def Update(self) -> 'dict':
        resp: requests.Response = utils.PUT(f"{URL}/ticket/ticket/{self.id}", TKN, self.to_json(in_reply_format=False))
        return {"code": resp.status_code, "txt": resp.text, "requestbody": self.to_json(in_reply_format=False)}

    def to_json(self, include_last_reply: bool = False, in_reply_format = True):
        return utils.CLEANJSON({
            "id": self.id,
            "number": self.number,
            "user": self.user.id,
            "status": self.status.id if isinstance(self.status, Status) else self.status,
            "priority": self.priority.id if isinstance(self.priority, Priority) else self.priority,
            "sla_plan_id": self.sla.id or None,
            "reply_due_time": self.duetime if self.duetime else None,
            "cc": self.cc,
            "locked": self.locked,
            "internal": self.internal,
            "merged": self.merged,
            "subject": self.subject,
            "assignedto": [op.id if isinstance(op, Operator) else int(op) for op in self.assigned],
            "customfield": {cf.customfield_id: cf.value for cf in self.custom_field_values},
            'tag': [t.id if isinstance(t, TicketTag) else int(t) for t in self.tags],
            "last_reply": self.last_reply.to_json() if self.last_reply and include_last_reply else None
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
            "is_draft": self.is_draft,
            "created_at": self.created_at
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
        self.options: List[CustomFieldValue] | None = [CustomFieldValue(objdata) for objdata in data.get("options", {})]
    
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
            "public": self.public,
            "options": [option.to_json() for option in self.options] if self.options else None
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

def GetTickets(filter: int = None, filter_operator: Operator | int = None, search: str = None, number: str = None, status: str | Status | List[str] | List[Status] = None, priority: str | Priority = None, user: User | List[User] | str = None, user_email: str = None, organisation: Organisation | str = None, assigned: Operator | List[Operator] | str | List[str] = None, internal: bool = None, start: int = None, created_at_min: int | str = None, created_at_max: int | str = None, updated_at_min: int | str = None, updated_at_max: int | str = None, limit: int = 50, order_direction: str = "asc", order_column: str = "id") -> List[Ticket]:
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
        elif isinstance(status, str):
            target += f"&status={status}"
        elif isinstance(status, list) and isinstance(status[0], str):
            target += f"&status="
            for st in status: target += f"{st},"
            target = target[0:-1]
        elif isinstance(status, list) and isinstance(status[0], Status):
            target += f"&status="
            for st in status: target += f"{st.id},"
            target = target[0:-1]
    if not priority == None:
        if isinstance(priority, Priority):
            target += f"&priority={priority.id}"
        else:
            target += f"&priority={priority}"
    if not user == None:
        if isinstance(user, User):
            target += f"&user={user.id}"
        elif isinstance(user, list) and isinstance(user[0], User):
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
        elif isinstance(assigned, list) and isinstance(assigned[0], Operator):
            target += f"&assigned="
            for eachUser in user:
                target += eachUser.id + ","
            target = target[0:-1]
        elif isinstance(assigned, list) and isinstance(assigned[0], str):
            target += f"&assigned="
            for eachUser in user:
                target += eachUser + ","
            target = target[0:-1]
        else:
            target += f"&assigned={assigned}"
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
    if not order_direction == None: target += f"&order_direction={order_direction}"
    if not order_column == None: target += f"&order_column={order_column}"
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

def GetArticles(limit: int = 20) -> List[Article]:
    articles_json = json.loads(utils.GET(f"{URL}/selfservice/article?limit={limit}", tkn=TKN).text)['data']
    articles = []
    for article in articles_json:
        articles.append(Article(article)) 
    return articles

def GetArticleById(id) -> Article:
    articles_json = json.loads(utils.GET(f"{URL}/selfservice/article/{id}", tkn=TKN).text)['data']
    print(articles_json)
    return Article(articles_json)

def SearchArticles(term: str, limit: int = 20, published_only: bool = False, include_protected: bool = True) -> List[Article]:
    articles_json = json.loads(utils.GET(f"{URL}/selfservice/article/search?limit={limit}&published={published_only}&protected={include_protected}&term={term}", tkn=TKN).text)['data']
    print(f"{URL}/selfservice/article/search?limit={limit}&published={published_only}&protected={include_protected}&term={term}")
    articles = []
    for article in articles_json:
        articles.append(Article(article)) 
    return articles

def DeleteArticle(article: int | Article):
    response = json.loads(utils.DELETE(f"{URL}/selfservice/article/{article.id if isinstance(article, Article) else article}", tkn=TKN).text)['data']
    return response

def CreateArticle(article: dict | Article):
    if isinstance(article, dict): article = Article(article)
    response = json.loads(utils.POST(f"{URL}/selfservice/article", tkn=TKN, data=article.to_json()).text)
    return response

def GetCategories(limit: int = 20) -> List[Article]:
    categories_json = json.loads(utils.GET(f"{URL}/selfservice/category?limit={limit}", tkn=TKN).text)['data']
    categories = []
    for category in categories_json:
        categories.append(Category(category)) 
    return categories

def GetCategoryById(id) -> Article:
    categories_json = json.loads(utils.GET(f"{URL}/selfservice/category/{id}", tkn=TKN).text)['data']
    return Category(categories_json)

def CreateCategory(category: dict | Category):
    if isinstance(category, dict): category = Category(category)
    response = json.loads(utils.POST(f"{URL}/selfservice/category", tkn=TKN, data=category.to_json()).text)
    return response

def GetTicketTags(limit: int = 20, skip: int = 0) -> List[TicketTag]:
    tags_json = json.loads(utils.GET(f"{URL}/ticket/tag?limit={limit}&start={skip}", tkn=TKN).text)['data']
    tags = []
    for tag in tags_json:
        tags.append(TicketTag(tag)) 
    return tags

def GetTicketTagById(id) -> ArticleTag:
    tags_json = json.loads(utils.GET(f"{URL}/ticket/tag/{id}", tkn=TKN).text)['data']
    return TicketTag(tags_json)

def GetSelfServiceTags(limit: int = 20) -> List[ArticleTag]:
    tags_json = json.loads(utils.GET(f"{URL}/selfservice/tag?limit={limit}", tkn=TKN).text)['data']
    tags = []
    for tag in tags_json:
        tags.append(ArticleTag(tag)) 
    return tags

def GetSelfServiceTagById(id) -> ArticleTag:
    tags_json = json.loads(utils.GET(f"{URL}/selfservice/tag/{id}", tkn=TKN).text)['data']
    return ArticleTag(tags_json)

def CreateSelfServiceTag(tag: dict | ArticleTag):
    if isinstance(tag, dict): tag = ArticleTag(tag)
    response = json.loads(utils.POST(f"{URL}/selfservice/tag", tkn=TKN, data=tag.to_json()).text)
    return response

def DeleteSelfServiceTag(tag: int | Article):
    response = json.loads(utils.DELETE(f"{URL}/selfservice/tag/{tag.id if isinstance(tag, ArticleTag) else tag}", tkn=TKN).text)['data']
    return response

def GetTypes(limit: int = 20) -> List[ArticleType]:
    types_json = json.loads(utils.GET(f"{URL}/selfservice/type?limit={limit}", tkn=TKN).text)['data']
    types = []
    for type in types_json:
        types.append(ArticleType(type)) 
    return types

def GetTypeById(id) -> ArticleType:
    types_json = json.loads(utils.GET(f"{URL}/selfservice/type/{id}", tkn=TKN).text)['data']
    return ArticleType(types_json)

def CreateType(type: dict | ArticleType):
    if isinstance(type, dict): type = ArticleType(type)
    response = json.loads(utils.POST(f"{URL}/selfservice/type", tkn=TKN, data=type.to_json()).text)
    return response
