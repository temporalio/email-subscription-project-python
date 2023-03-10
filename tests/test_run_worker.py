# @@@SNIPSTART email-subscription-project-python-test_run_worker

import uuid

import pytest
from temporalio import activity
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from activities import send_email
from run_worker import SendEmailWorkflow
from shared_objects import ComposeEmail


@pytest.mark.asyncio
async def test_execute_workflow():
    task_queue_name = "subscription"
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[SendEmailWorkflow],
            activities=[send_email],
        ):
            assert (
                "Sending email to test@example.com with message: Here's your message!, count: 1"
                == await env.client.execute_workflow(
                    SendEmailWorkflow.run,
                    args=("test@example.com", "Here's your message!"),
                    id=str(uuid.uuid4()),
                    task_queue=task_queue_name,
                )
            )


@activity.defn(name="send_email")
async def send_email_mocked(input: ComposeEmail) -> str:
    return f"Sending email to {input.email} with message: {input.message}, count: {input.count} from mocked activity!"


@pytest.mark.asyncio
async def test_mock_activity():
    task_queue_name = "subscription"
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[SendEmailWorkflow],
            activities=[send_email],
        ):
            assert (
                "Sending email to test@example.com with message: Here's your message!, count: 1"
                == await env.client.execute_workflow(
                    SendEmailWorkflow.run,
                    args=("test@example.com", "Here's your message!"),
                    id=str(uuid.uuid4()),
                    task_queue=task_queue_name,
                )
            )


# @@@SNIPEND
