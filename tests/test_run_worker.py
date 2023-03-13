# @@@SNIPSTART email-subscription-project-python-test_run_worker


import pytest
from temporalio.client import Client, WorkflowExecutionStatus, WorkflowFailureError
from temporalio.exceptions import CancelledError
from temporalio.worker import Worker

from activities import send_email
from run_worker import SendEmailWorkflow


@pytest.mark.asyncio
async def test_execute_workflow(client: Client):
    task_queue_name = "subscription"
    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[SendEmailWorkflow],
        activities=[send_email],
    ):
        handle = await client.start_workflow(
            SendEmailWorkflow.run,
            args=("test@example.com", "Here's your message!"),
            id="subscription",
            task_queue=task_queue_name,
        )
        await handle.cancel()

        with pytest.raises(WorkflowFailureError) as err:
            await handle.result()
        assert isinstance(err.value.cause, CancelledError)

    assert WorkflowExecutionStatus.CANCELED == (await handle.describe()).status


# @@@SNIPEND
