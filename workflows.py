# @@@SNIPSTART email-subscription-project-python-workflows

import asyncio
from datetime import timedelta

from temporalio import workflow

from shared_objects import ComposeEmail

with workflow.unsafe.imports_passed_through():
    from activities import send_email


@workflow.defn
class SendEmailWorkflow:
    def __init__(self) -> None:
        self._email: str = "<no email>"
        self._message: str = "<no message>"
        self._subscribed: bool = False
        self._count: int = 0

    @workflow.run
    async def run(self, email: str):
        self._email = f"{email}"
        self._message = "Welcome to our Subscription Workflow!"
        self._subscribed = True
        self._count = 0

        while self._subscribed is True:
            self._count += 1
            if self._count > 1:
                self._message = "Thank you for staying subscribed!"

            await workflow.start_activity(
                send_email,
                ComposeEmail(self._email, self._message, self._count),
                start_to_close_timeout=timedelta(seconds=10),
            )
            await asyncio.sleep(12)

        return ComposeEmail(self._email, self._message, self._count)

    @workflow.query
    def greeting(self) -> str:
        return self._email

    @workflow.query
    def message(self) -> str:
        return self._message

    @workflow.query
    def count(self) -> int:
        return self._count


# @@@SNIPEND
