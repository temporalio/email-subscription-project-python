# @@@SNIPSTART email-subscription-project-python-activity_function
from shared_objects import ComposeEmail
from temporalio import activity


@activity.defn
async def send_email(details: ComposeEmail) -> str:
    print(
        f"Sending email to {details.email} with message: {details.message}, count: {details.count}"
    )
    return "success"


# @@@SNIPEND
