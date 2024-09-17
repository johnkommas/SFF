import socket
import threading
import uvicorn
from fastapi import FastAPI, Request
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from dotenv import load_dotenv
from dev_slack import home_page, modals, reports
import os

# load .env file
load_dotenv()
app = App(signing_secret=os.getenv('SLACK_SECRET'),
          token=os.getenv('SLACK_TOKEN'))

app_handler = SlackRequestHandler(app)
token_holder = {}


@app.event("message")
def handle_message_events(body, logger,):
    logger.info(body)



@app.action("request_arxeio")
def action_button_click(body, ack, say, logger, client):
    # print(body)
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient

    client.views_open(
        trigger_id=body["trigger_id"],
        view=modals.choose_archive())

@app.action("reuest_phones")
def action_button_click(body, ack, say, logger, client):
    text = 'ΤΗΛΕΦΩΝΑ ΕΠΙΚΟΙΝΩΝΙΑΣ'
    reports.button_reports(body, client, logger, text)
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient

    client.views_open(
        trigger_id=body["trigger_id"],
        view=modals.send_phones())


@app.view("button_archive_step_b")
def handle_submission(ack, body, view, logger, client):
    text = 'ΑΡΧΕΙΟ ΟΙ ΑΙΤΗΣΕΙΣ ΜΑΣ '
    ack()
    try:
        logger.info(body)
        key = modals.handle_archive_step_b(view)
        reports.button_reports(body,client, logger, text, key)
        client.views_open(
            trigger_id=body["trigger_id"],
            view=modals.represent_data(key))
    except Exception as e:
        logger.error(f"Error responding to 'archive_step_b' button click: {e}")


@app.action("archive_step_b")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)


@app.event("app_home_opened")
def publish_home_view(client, event, logger):
    """
    The Home tab is a persistent, yet dynamic interface for apps.
    The user can reach the App Home from the conversation list
    within Slack or by clicking on the app's name in messages.
    Note: you *must* enable Home Tab (App Home > Show Tabs Section)
    to receive this event.
    Please see the 'Event Subscriptions' and 'OAuth & Permissions'
    sections of your app's configuration to add the following:
    Event subscription(s):  app_home_opened
    Required scope(s):      none
    Further Information & Resources
    https://slack.dev/bolt-python/concepts#app-home
    https://api.slack.com/surfaces/tabs
    """

    admin_users = os.getenv('SLACK_ADMINISTRATORS')
    user_info = client.users_info(user=event["user"])
    user_image = user_info['user']['profile']['image_original']
    is_admin = event["user"] in admin_users
    if is_admin:
        print(f'Admin User {event["user"]}, {user_info['user'].get('real_name')}\n')
    else:
        print(f'Single User {event["user"]}, {user_info['user'].get('real_name')}')
    try:
        client.views_publish(
            user_id=event["user"],
            view=home_page.run(event, is_admin))
    except Exception as e:
        logger.error(f"Error publishing view to Home Tab: {e}")


api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@api.get("/status")
async def get_status():
    return {"status": "Server is running"}


@api.get("/")
async def root():
    x = {'print': 'Hello World'}
    return x


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":
    my_ip = get_ip_address()
    uvicorn.run("main:api", host=my_ip, port=3200, log_level="info", reload=True)
