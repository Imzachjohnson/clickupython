from typing import Optional, List, Any

from pydantic import BaseModel, ValidationError, validator, Field

import json


class Priority(BaseModel):

    priority: str
    color: str


class Status(BaseModel):
    status: str = None
    color: str = None

    hide_label: bool = None


class StatusElement(BaseModel):

    id: Optional[str]
    status: str

    orderindex: int
    color: str

    type: str


class Asssignee(BaseModel):
    id: str = None
    color: str = None
    username: str = None
    initials: str = None

    profilePicture: str = None


class ListFolder(BaseModel):
    id: str
    name: str

    hidden: Optional[bool]

    access: bool


class SingleList(BaseModel):
    id: str = None
    name: str = None

    deleted: bool = None

    archived: bool = None

    orderindex: int = None

    override_statuses: bool = None

    priority: Optional[Priority] = None

    assignee: Asssignee = None
    due_date: str = None
    start_date: str = None

    folder: ListFolder = None

    space: ListFolder = None

    statuses: Optional[List[StatusElement]] = None

    inbound_address: str = None

    permission_level: str = None

    content: Optional[str] = None

    status: Optional[Status] = None

    task_count: Optional[int] = None

    start_date_time: Optional[str] = None

    due_date_time: Optional[bool] = None

    # return a single list

    def build_list(self):

        return SingleList(**self)


class AllLists(BaseModel):

    lists: List[SingleList] = None

    # return a list of lists

    def build_lists(self):

        return AllLists(**self)


class ChecklistItem(BaseModel):
    id: str = None
    name: str = None

    orderindex: int = None

    assignee: Optional[Asssignee]


class Checklist(BaseModel):

    id: Optional[str]

    task_id: str = None
    name: str = None

    orderindex: int = None

    resolved: int = None

    unresolved: int = None

    items: List[ChecklistItem] = None

    def add_item(self, client_instance, name: str, assignee: str = None):

        return client_instance.create_checklist_item(
            self.id, name=name, assignee=assignee
        )


class Checklists(BaseModel):

    checklist: Checklist

    def build_checklist(self):

        final_checklist = Checklists(**self)

        return final_checklist.checklist


class Attachment(BaseModel):

    id: str

    version: int
    date: str
    title: str

    extension: str

    thumbnail_small: str

    thumbnail_large: str
    url: str

    def build_attachment(self):

        return Attachment(**self)


class User(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None

    profilePicture: str = None

    initials: Optional[str] = None

    role: Optional[int] = None

    custom_role: Optional[None] = None

    last_active: Optional[str] = None

    date_joined: Optional[str] = None

    date_invited: Optional[str] = None


class AssignedBy(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None
    profile_picture: str = None


class CommentComment(BaseModel):

    text: str = None


class Comment(BaseModel):
    id: str = None

    comment: List[CommentComment] = None

    comment_text: str = None

    user: AssignedBy = None

    resolved: bool = None

    assignee: AssignedBy = None

    assigned_by: AssignedBy = None

    reactions: List[Any] = None
    date: str = None
    hist_id: str = None

    def build_comment(self):

        return Comment(**self)


class Comments(BaseModel):

    comments: List[Comment] = None

    def __iter__(self):

        return iter(self.comments)

    def build_comments(self):

        return Comments(**self)


class Creator(BaseModel):
    id: int = None
    username: str = None
    color: str = None
    profile_picture: str = None


class TypeConfig(BaseModel):

    include_guests: Optional[bool]

    include_team_members: Optional[bool]


class CustomItems:

    enabled: bool = None


class DueDates(BaseModel):

    enabled: bool = None

    start_date: bool = None

    remap_due_dates: bool = None

    remap_closed_due_date: bool = None


class CustomField(BaseModel):
    id: str = None
    name: str = None

    type: str = None

    type_config: TypeConfig = None
    date_created: str = None

    hide_from_guests: bool = None

    value: Optional[Any] = None

    required: bool = None


class TimeTracking(BaseModel):

    enabled: bool = False

    harvest: bool = False

    rollup: bool = False


class Sprints(BaseModel):

    enabled: bool = False


class Points(BaseModel):

    enabled: bool = False


class Zoom(BaseModel):

    enabled: bool = False


class Milestones(BaseModel):

    enabled: bool = False


class Emails(BaseModel):

    enabled: bool = False


class CustomItems(BaseModel):

    enabled: bool = False


class MultipleAssignees(BaseModel):

    enabled: bool = False


class TagsStatus(BaseModel):

    enabled: bool = False


class CustomFieldsStatus(BaseModel):

    enabled: bool = False


class DependencyWarning(BaseModel):

    enabled: bool = False


class TimeEstimateStatus(BaseModel):

    enabled: bool = False


class RemapDependenciesStatus(BaseModel):

    enabled: bool = False


class ChecklistsStatus(BaseModel):

    enabled: bool = False


class PortfoliosStatus(BaseModel):

    enabled: bool = False


class Features(BaseModel):

    due_dates: DueDates = None

    multiple_assignees: MultipleAssignees = None

    sprints: Sprints = None

    start_date: bool = False

    remap_due_dates: bool = False

    remap_closed_due_date: bool = False

    time_tracking: Optional[TimeTracking]

    tags: Optional[TagsStatus]

    time_estimates: Optional[TimeEstimateStatus]

    checklists: Optional[ChecklistsStatus]

    custom_fields: Optional[CustomFieldsStatus]

    remap_dependencies: Optional[RemapDependenciesStatus]

    dependency_warning: DependencyWarning = None

    portfolios: Optional[PortfoliosStatus]

    points: Points = None

    custom_items: CustomItems = None

    zoom: Zoom = None

    milestones: Milestones = None

    emails: Emails = None

    class Config:

        validate_assignment = True

    @validator("time_tracking", pre=True, always=True)
    def set_tt(cls, time_tracking):

        return time_tracking or {"enabled": False}

    @validator("custom_fields", pre=True, always=True)
    def set_cf(cls, custom_fields):

        return custom_fields or {"enabled": False}

    @validator("tags", pre=True, always=True)
    def set_tags(cls, tags):

        return tags or {"enabled": False}

    @validator("multiple_assignees", pre=True, always=True)
    def set_ma(cls, multiple_assignees):
        return multiple_assignees or {"enabled": False}

    @validator("checklists", pre=True, always=True)
    def set_checklists(cls, checklists):
        return checklists or {"enabled": False}

    @validator("portfolios", pre=True, always=True)
    def set_portfolios(cls, portfolios):
        return portfolios or {"enabled": False}


class SpaceFeatures(BaseModel):

    due_dates: bool = False

    multiple_assignees: bool = False

    start_date: bool = False

    remap_due_dates: bool = False

    remap_closed_due_date: bool = False

    time_tracking: bool = False

    tags: bool = False

    time_estimates: bool = False

    checklists: bool = False

    custom_fields: bool = False

    remap_dependencies: bool = False

    dependency_warning: bool = False

    portfolios: bool = False

    points: bool = False

    custom_items: bool = False

    zoom: bool = False

    milestones: bool = False

    emails: bool = False

    @property
    def all_features(self):

        return {
            "due_dates": {
                "enabled": self.due_dates,
                "start_date": self.start_date,
                "remap_due_dates": self.remap_due_dates,
                "remap_closed_due_date": self.remap_closed_due_date,
            },
            "time_tracking": {"enabled": self.time_tracking},
            "tags": {"enabled": self.tags},
            "time_estimates": {"enabled": self.time_estimates},
            "checklists": {"enabled": self.checklists},
            "custom_fields": {"enabled": self.custom_fields},
            "remap_dependencies": {"enabled": self.remap_dependencies},
            "dependency_warning": {"enabled": self.dependency_warning},
            "portfolios": {"enabled": self.portfolios},
            "milestones": {"enabled": self.milestones},
        }


class Space(BaseModel):

    id: Optional[str] = None

    name: Optional[str] = None

    access: Optional[bool] = None

    features: Optional[Features]

    multiple_assignees: Optional[bool] = None

    private: Optional[bool] = False

    statuses: Optional[List[Status]] = None

    archived: Optional[bool] = None

    def build_space(self):

        return Space(**self)


class Spaces(BaseModel):

    spaces: List[Space] = None

    def __iter__(self):

        return iter(self.spaces)

    def build_spaces(self):

        return Spaces(**self)


class Folder(BaseModel):
    id: str = None
    name: str = None

    orderindex: int = None

    override_statuses: bool = False

    hidden: bool = False

    space: Optional[Space] = None

    task_count: int = None

    lists: List[SingleList] = []

    def build_folder(self):

        return Folder(**self)

    def delete(self, client_instance):

        model = "folder/"

        deleted_folder_status = client_instance._delete_request(model, self.id)


class Folders(BaseModel):

    folders: List[Folder] = None

    def build_folders(self):

        return Folders(**self)


class Priority(BaseModel):
    id: int = None

    priority: str = None
    color: str = None

    orderindex: str = None


class Status(BaseModel):

    id: Optional[str] = None
    status: str = None
    color: str = None

    orderindex: int = None

    type: str = None


class ClickupList(BaseModel):
    id: str = None


# class Folder(BaseModel):

#     id: str = None


class Task(BaseModel):

    id: str = None
    custom_id: str = None
    name: str = None

    text_content: str = None
    description: str = None

    status: Status = None

    orderindex: str = None
    date_created: str = None
    date_updated: str = None
    date_closed: str = None

    creator: Creator = None

    assignees: List[Asssignee] = None

    task_checklists: List[Any] = Field(None, alias="checklists")

    task_tags: List[Any] = Field(None, alias="tags")
    parent: str = None

    priority: int = None
    due_date: str = None
    start_date: str = None
    time_estimate: str = None

    time_spent: Optional[str] = None

    custom_fields: Optional[List[CustomField]]
    list: ClickupList = None

    folder: Folder = None

    space: Folder = None
    url: str = ""

    def build_task(self):

        return Task(**self)

    def delete(self):

        client.ClickUpClient.delete_task(self, self.id)

    def upload_attachment(self, client_instance, file_path: str):

        return client_instance.upload_attachment(self.id, file_path)

    def update(
        self,
        client_instance,
        name: str = None,
        description: str = None,
        status: str = None,
        priority: int = None,
        time_estimate: int = None,
        archived: bool = None,
        add_assignees: List[str] = None,
        remove_assignees: List[int] = None,
    ):

        return client_instance.update_task(
            self.id,
            name,
            description,
            status,
            priority,
            time_estimate,
            archived,
            add_assignees,
            remove_assignees,
        )

    def add_comment(
        self,
        client_instance,
        comment_text: str,
        assignee: str = None,
        notify_all: bool = True,
    ):

        return client_instance.create_task_comment(
            self.id, comment_text, assignee, notify_all
        )

    def get_comments(self, client_instance):

        return client_instance.get_task_comments(self.id)


class Tasks(BaseModel):

    tasks: List[Task] = None

    def __iter__(self):

        return iter(self.tasks)

    def build_tasks(self):

        return Tasks(**self)


class User(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None

    profilePicture: str = None

    initials: Optional[str] = None

    role: Optional[int] = None

    custom_role: Optional[None] = None

    last_active: Optional[str] = None

    date_joined: Optional[str] = None

    date_invited: Optional[str] = None


class InvitedBy(BaseModel):
    id: str = None
    username: str = None
    color: str = None
    email: str = None
    initials: str = None
    profile_picture: None = None


class Member(BaseModel):

    user: User

    invited_by: Optional[InvitedBy] = None


class Members(BaseModel):

    members: List[User] = None

    def __iter__(self):

        return iter(self.members)

    def build_members(self):

        return Members(**self)


class Team(BaseModel):
    id: str = None
    name: str = None
    color: str = None

    avatar: str = None

    members: List[Member] = None


class Teams(BaseModel):

    teams: List[Team] = None

    def __iter__(self):

        return iter(self.teams)

    def build_teams(self):

        return Teams(**self)


class Goal(BaseModel):
    id: str = None
    name: str = None
    team_id: int = None
    date_created: str = None
    start_date: str = None
    due_date: str = None
    description: str = None

    private: bool = None

    archived: bool = None
    creator: int = None
    color: str = None

    pretty_id: int = None

    multiple_owners: bool = None
    folder_id: str = None

    members: List[User] = None

    owners: List[User] = None

    key_results: List[Any] = None
    percent_completed: int = None

    history: List[Any] = None

    pretty_url: str = None

    def build_goal(self):

        return Goal(**self)


class Goals(BaseModel):

    goal: Goal

    def build_goals(self):

        built_goal = Goals(**self)

        return built_goal.goal


class GoalsList(BaseModel):

    goals: List[Goal] = None
    folders: List[Folder] = None

    def __iter__(self):

        return iter(self.goals)

    def build_goals(self):

        return GoalsList(**self)


class Tag(BaseModel):
    name: str = None

    tag_fg: str = None

    tag_bg: str = None

    def build_tag(self):

        return Tag(**self)


class Tags(BaseModel):

    tags: List[Tag] = None

    def __iter__(self):

        return iter(self.tags)

    def build_tags(self):

        return Tags(**self)


class Shared(BaseModel):

    tasks: Optional[List[Tasks]]

    lists: Optional[List[SingleList]]

    folders: Optional[List[Folder]]

    def build_shared(self):
        return Shared(**self)

    def __iter__(self):
        return iter(self.shared)


class SharedHierarchy(BaseModel):
    shared: Shared

    def build_shared(self):
        return SharedHierarchy(**self)

    def __iter__(self):
        return iter(self.shared)


class TimeTrackingData(BaseModel):
    id: str = ""
    task: Task = None
    wid: str = ""
    user: User = None
    billable: bool = False
    start: str = ""
    end: str = ""
    duration: int = None
    description: str = ""
    tags: List[Tag] = None
    source: str = ""
    at: str = ""

    def build_data(self):
        return TimeTrackingData(**self)


class TimeTrackingDataList(BaseModel):
    data: List[TimeTrackingData] = None

    def build_data(self):
        return TimeTrackingDataList(**self)

    def __iter__(self):
        return iter(self.data)


class TimeTrackingDataSingle(BaseModel):
    data: TimeTrackingData = None

    def build_data(self):
        return TimeTrackingDataSingle(**self)

    def __iter__(self):
        return iter(self.data)
