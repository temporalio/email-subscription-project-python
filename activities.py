# @@@SNIPSTART email-subscription-project-python-activity_function
from temporalio import activity

from shared_objects import EmailDetails


@activity.defn
async def send_email(details: EmailDetails) -> str:
    print(
        f"Sending email to {details.email} with message: {details.message}, count: {details.count}"
    )
    return "success"


# @@@SNIPEND
