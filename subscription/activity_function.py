# @@@SNIPSTART email-subscription-project-python-activity_function
from temporalio import activity

from subscription.shared_objects import ComposeEmail  # noqa: F401


@activity.defn
async def send_email(details: ComposeEmail) -> str:
    print(
        f"Sending email to {details.email} with message: {details.message}, count: {details.count}"
    )
    return "success"


# @@@SNIPEND
