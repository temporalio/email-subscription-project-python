import uuid

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from subscription.shared_objects import ComposeEmail
from subscription.activity_function import send_email
from subscription.run_worker import SendEmailWorkflow
import logging

logger = logging.getLogger(__name__)


async def test_execute_workflow(client: Client):
    task_queue_name = str(uuid.uuid4())

    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[SendEmailWorkflow],
        activities=[send_email],
    ):
        assert "Sending email to test@example.com with message: Here's your message!, count: 1" == await client.execute_workflow(
            SendEmailWorkflow.run,
            args=("test@example.com", "Here's your message!"),
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )


@activity.defn(name="send_email")
async def send_email_mocked(input: ComposeEmail) -> str:
    print(
        f"Sending email to test@example.com with message: {input.message}, count: {input.count}"
        
    )
    return "success"


async def test_mock_activity(client: Client):
    task_queue_name = str(uuid.uuid4())
    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[SendEmailWorkflow],
        activities=[send_email_mocked],
    ):
        assert "Sending email to test@example.com with message: Here's your message!, count: 1" == await client.execute_workflow(
            SendEmailWorkflow.run,
            args=("test@example.com", "Here's your message!"),
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )