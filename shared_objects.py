# @@@SNIPSTART email-subscription-project-python-shared_objects
from dataclasses import dataclass


@dataclass
class ComposeEmail:
    email: str
    message: str
    count: int = 0


# @@@SNIPEND
