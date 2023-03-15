# @@@SNIPSTART email-subscription-project-python-run_flask

from flask import Flask, g, jsonify, request
from temporalio.client import Client

from run_worker import SendEmailWorkflow

app = Flask(__name__)


async def get_client():
    if Client not in g:
        g.client = await Client.connect("localhost:7233")
    return g.client


@app.route("/subscribe", methods=["POST", "GET"])
async def start_subscription():
    await get_client()
    email_id = str(request.json.get("email"))
    if request.method == "POST":
        await g.client.start_workflow(
            SendEmailWorkflow.run,
            args=(email_id,),
            id=email_id,
            task_queue="subscription",
        )
        return jsonify({"status": "ok"})
    else:
        return jsonify({"message": "This endpoint requires a POST request."})


@app.route("/get_details", methods=["GET"])
async def get_query():
    await get_client()
    email_id = str(request.json.get("email"))
    handle = g.client.get_workflow_handle(
        email_id,
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


@app.route("/unsubscribe", methods=["DELETE"])
async def end_subscription():
    await get_client()
    email_id = str(request.json.get("email"))
    handle = g.client.get_workflow_handle(
        email_id,
    )
    await handle.cancel()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
# @@@SNIPEND
