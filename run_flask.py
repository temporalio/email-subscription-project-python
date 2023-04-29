# @@@SNIPSTART email-subscription-project-python-run_flask

import asyncio
from flask import Flask, jsonify, current_app, request, make_response
from temporalio.client import Client

from run_worker import SendEmailWorkflow
from shared_objects import TaskQueueName, EmailDetails, WorkflowOptions

app = Flask(__name__)

async def connect_temporal(app):
    client: Client = await Client.connect('localhost:7233')
    app.temporal_client = client

def get_client() -> Client:
    return current_app.temporal_client

@app.route("/subscribe", methods=["POST"])
async def start_subscription():
    client: Client = get_client()
    if request.method == "POST":
        email_id: str = str(request.json.get("email"))
        data: WorkflowOptions = WorkflowOptions(email = email_id)
        await client.start_workflow(
            SendEmailWorkflow.run,
            data,
            id=data.email,
            task_queue=TaskQueueName,
        )

        message = jsonify({"message": "Resource created successfully"})
        response = make_response(message, 201)
        return response

    return jsonify({"message": "This endpoint requires a POST request."})


@app.route("/get_details", methods=["GET"])
async def get_query():
    client: Client = get_client()
    email_id = request.args.get("email")
    handle = client.get_workflow_handle(email_id)
    results = await handle.query(SendEmailWorkflow.details)

    message =  jsonify(
        {
            "email": results.email,
            "message": results.message,
            "subscribed": results.subscribed,
            "numberOfEmailsSent": results.count
        }
    )

    response = make_response(message, 200)
    return response


@app.route("/unsubscribe", methods=["DELETE"])
async def end_subscription():
    client = get_client()
    email_id: str = str(request.json.get("email"))
    handle = client.get_workflow_handle(
        email_id,
    )
    await handle.cancel()
    message = jsonify({"message": "Requesting cancellation"})

    # Return 202 because this is a request to cancel and the API has accepted
    # the request but has not processed yet.
    response = make_response(message, 202)
    return response

if __name__ == "__main__":
    # Create Temporal connection.
    asyncio.run(connect_temporal(app))

    # Start API
    app.run(debug=True)
# @@@SNIPEND
