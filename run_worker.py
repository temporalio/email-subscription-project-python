# @@@SNIPSTART email-subscription-project-python-run_worker
import asyncio

from activities import send_email
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import SendEmailWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[SendEmailWorkflow],
        activities=[send_email],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
# @@@SNIPEND