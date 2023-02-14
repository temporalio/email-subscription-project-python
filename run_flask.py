# @@@SNIPSTART run_flask
from typing import Any, Dict

from flask import Flask, g, jsonify, request
from run_worker import SendEmailWorkflow
from temporalio.client import Client

app = Flask(__name__)


async def get_client():
    if Client not in g:
        g.client = await Client.connect("localhost:7233")
    return g.client


@app.route("/subscribe/", methods=["POST"])
async def start_subscription():
    client = await get_client()

    await g.client.start_workflow(
        SendEmailWorkflow.run,
        args=(request.form["email"], request.form["message"]),
        id="send-email-activity",
        task_queue="hello-activity-task-queue",
    )
    handle = g.client.get_workflow_handle(
        "send-email-activity",
    )
    emails_sent: int = await handle.query(SendEmailWorkflow.count)
    email: str = await handle.query(SendEmailWorkflow.greeting)

    return jsonify({"status": "ok", "email": email, "emails_sent": emails_sent})


# GET
@app.route("/get-details/", methods=["GET"])
async def get_query():
    client = await get_client()
    handle = g.client.get_workflow_handle(
        "send-email-activity",
    )
    count: int = await handle.query(SendEmailWorkflow.count)
    greeting: str = await handle.query(SendEmailWorkflow.greeting)
    message: str = await handle.query(SendEmailWorkflow.message)

    return jsonify(
        {
            "status": "ok",
            "numberOfEmailsSent": count,
            "email": greeting,
            "message": message,
        }
    )


# patch or delete
@app.route("/unsubscribe/", methods=["DELETE"])
async def end_subscription():
    client = await get_client()
    handle = g.client.get_workflow_handle(
        "send-email-activity",
    )
    await handle.cancel()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
# @@@SNIPEND
