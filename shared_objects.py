# @@@SNIPSTART email-subscription-project-python-shared_objects
from dataclasses import dataclass

TaskQueueName: str="email_subscription"

@dataclass
class WorkflowOptions:
    email: str

@dataclass
class EmailDetails:
    email: str = ""
    message: str = ""
    count: int = 0
    subscribed: bool = False


# @@@SNIPEND
