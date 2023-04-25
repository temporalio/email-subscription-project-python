# @@@SNIPSTART email-subscription-project-python-workflows

import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.exceptions import CancelledError

from shared_objects import EmailDetails, WorkflowOptions

with workflow.unsafe.imports_passed_through():
    from activities import send_email


@workflow.defn
class SendEmailWorkflow:
    def __init__(self) -> None:
        self.email_details = EmailDetails()

    @workflow.run
    async def run(self, data: WorkflowOptions):
        duration = 12
        self.email_details.email= data.email
        self.email_details.message = "Welcome to our Subscription Workflow!"
        self.email_details.subscribed = True
        self.email_details.count = 0

        while self.email_details.subscribed is True:
            self.email_details.count += 1
            if self.email_details.count > 1:
                self.email_details.message = "Thank you for staying subscribed!"

            try:
                await workflow.start_activity(
                    send_email,
                    self.email_details,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                await asyncio.sleep(duration)

            except asyncio.CancelledError as err:
                # Cancelled by the user. Send them a goodbye message.
                self.email_details.subscribed = False
                self.email_details.message = "Sorry to see you go"
                await workflow.start_activity(
                    send_email,
                    self.email_details,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                # raise error so workflow shows as cancelled.
                raise err


    @workflow.query
    def details(self) -> EmailDetails:
        return self.email_details

# @@@SNIPEND
