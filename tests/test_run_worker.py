# @@@SNIPSTART email-subscription-project-python-test_run_worker

import pytest
import asyncio

from temporalio.worker import Worker
from temporalio.testing import WorkflowEnvironment
from temporalio.exceptions import CancelledError
from temporalio.client import WorkflowFailureError, WorkflowExecutionStatus

from shared_objects import EmailDetails
from activities import send_email
from run_worker import SendEmailWorkflow
#

@pytest.mark.asyncio
async def test_create_email() -> None:
    task_queue_name: str = "subscription"

    async with await WorkflowEnvironment.start_local() as env:
        data: EmailDetails = EmailDetails(email="test@example.com", message="Here's your message!")

        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[SendEmailWorkflow],
            activities=[send_email],
        ):

            handle = await env.client.start_workflow(
                SendEmailWorkflow.run,
                data,
                id=data.email,
                task_queue=task_queue_name,
            )

            assert WorkflowExecutionStatus.RUNNING == (await handle.describe()).status


@pytest.mark.asyncio
async def test_cancel_workflow() -> None:
    task_queue_name: str = "email_subscription"

    async with await WorkflowEnvironment.start_local() as env:
        data: EmailDetails = EmailDetails(email="test@example.com", message="Here's your message!")

        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[SendEmailWorkflow],
            activities=[send_email],
        ):

            handle = await env.client.start_workflow(
                SendEmailWorkflow.run,
                data,
                id=data.email,
                task_queue=task_queue_name,
            )

            await handle.cancel()

            # Cancelling a workflow requests cancellation. Need to wait for the
            # workflow to complete.
            with pytest.raises(WorkflowFailureError) as err:
                await handle.result()

            assert isinstance(err.value.cause, CancelledError)

            assert WorkflowExecutionStatus.CANCELED == (await handle.describe()).status
# @@@SNIPEND
