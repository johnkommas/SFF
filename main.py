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
    """
    Handles message events occurring within a Slack App.

    This function listens for "message" events that are fired within a Slack App,
    which occur when a message is sent in a channel, a direct message, or in a multi-person conversation.

    Parameters:
    body (dict): The event payload from the message event.
    logger (Logger): A Logger instance for logging the event payload.

    Returns:
    None

    Note:
    In this function, the incoming data captured in 'body' is simply logged. However, in more
    complex implementations, this function could be responsible for a range of responses and
    interactions, such as replying to the message or performing some action based on the message content.
    """

    logger.info(body)



@app.action("request_arxeio")
def action_button_click(body, ack, say, logger, client):
    """
    Handles the click of a button named 'request_arxeio' within a Slack App.

    This function is activated when a button with the action_id 'request_arxeio' is clicked within a Slack App.
    Upon activation, the function sends an acknowledgment back to Slack to ensure smooth processing.
    Next, it calls the 'views_open' method from the Slack client, which opens a new modal window in Slack.
    The content of the modal window is specified by the function 'modals.choose_archive()'.

    Parameters:
    body (dict): The event payload from the button click event.
    ack (function): A function to send acknowledgments from a callback to Slack's APIs.
    say (function): A function that sends a message to the channel from which the event was triggered.
    logger (Logger): A Logger instance for logging the event payload.
    client (SlackClient): An authenticated Slack client for making API calls.

    Returns:
    None

    Note:
    The 'ack()' function should be called immediately at the start of the event handler to acknowledge Slack.
    The 'client.views_open()' function opens a new view (modal) within the Slack interface.
    """

    # print(body)
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient

    client.views_open(
        trigger_id=body["trigger_id"],
        view=modals.choose_archive())

@app.action("reuest_phones")
def action_button_click(body, ack, say, logger, client):
    """
    Handles the click of a button named 'reuest_phones' within a Slack App.

    This function is activated when a button with the action_id 'reuest_phones' is clicked within a Slack App.
    The click event first triggers a report using 'reports.button_reports()'. The button click event
    'body', authenticated Slack client, logger, and a specific text 'ΤΗΛΕΦΩΝΑ ΕΠΙΚΟΙΝΩΝΙΑΣ' are sent to this function.
    Next, it sends an acknowledgment to Slack using 'ack()', and opens a new modal window in Slack using
    'client.views_open()' method. The content of the modal window is specified by the function 'modals.send_phones()'.

    Parameters:
    body (dict): The event payload from the button click event.
    ack (function): A function to send acknowledgments from a callback to Slack's APIs.
    say (function): A function that sends a message to the channel from which the event was triggered.
    logger (Logger): A Logger instance for logging the event payload.
    client (SlackClient): An authenticated Slack client for making API calls.

    Returns:
    None

    Note:
    The 'ack()' function should be called immediately at the start of the event handler to acknowledge Slack.
    The 'client.views_open()' function opens a new view (modal) within the Slack interface.
    """

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
    """
    Handles the submission of a modal view form named 'button_archive_step_b' within a Slack App.

    This function is activated upon the submission of a modal view form with the callback_id 'button_archive_step_b'.
    It first responds back with an acknowledgment to Slack using the 'ack()' function. Then, it logs the submission
    body using logger and processes the view submission using the 'modals.handle_archive_step_b()' function.
    The button reports are created based on the submission body, a predefined text 'ΑΡΧΕΙΟ ΟΙ ΑΙΤΗΣΕΙΣ ΜΑΣ ', and the 'key'
    returned by 'handle_archive_step_b()', using the 'reports.button_reports()' function.
    Finally, a new modal window is opened in Slack using 'client.views_open()' method, with the modal contents
    specified by 'modals.represent_data(key)' function based on the 'key'.

    Parameters:
    ack (function): A function to send acknowledgments from a callback to Slack's APIs.
    body (dict): The payload from the view submission event.
    view (dict): The current view object, containing the state and values of the form inputs.
    logger (Logger): A Logger instance for logging the event payload.
    client (SlackClient): An authenticated Slack client for making API calls.

    Returns:
    None

    Raises:
    Exception: If an error occurs while handling the form submission, an exception is raised, error message is logged.

    Note:
    The 'ack()' function should be called immediately at the start of the event handler to acknowledge Slack.
    The 'client.views_open()' function opens a new view (modal) within the Slack interface.
    """

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
    """
    Handles the action of a component named 'archive_step_b' within a Slack App.

    This function is activated when a component with the action_id 'archive_step_b' triggers an interaction within
    a Slack App. The function sends an acknowledgment back to Slack to ensure smooth processing. It also logs the
    event payload using a logger provided as a parameter.

    Parameters:
    ack (function): A function to send acknowledgments from a callback to Slack's APIs.
    body (dict): The payload from the action event.
    logger (Logger): A Logger instance for logging the event payload.

    Returns:
    None

    Note:
    The 'ack()' function should be called immediately at the start of the action handler to acknowledge Slack.
    """

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
    """
    Handles the 'app_home_opened' event within a Slack App.

    This function is activated when user open the app home within Slack. The user can reach the App Home from the 
    conversation list within Slack or by clicking on the app's name in messages. The function retrieves the user 
    details and checks if the user is an admin. Depending on the user status ('is_admin'), it delivers a specific 
    home page view to the user by calling 'home_page.run()' and publishes it to the user's home using 
    'client.views_publish()' method.

    Parameters:
    client (SlackClient): An authenticated Slack client for making API calls.
    event (dict): The payload from the 'app_home_opened' event.
    logger (Logger): A Logger instance for logging errors.

    Returns:
    None

    Raises:
    Exception: If an error occurs while publishing the view to Home Tab, an exception is raised and logged.

    Note:
    For this function to work, Home Tab must be enabled (App Home > Show Tabs Section) and the following must be added 
    to Event subscription(s):  'app_home_opened'. There are no required scopes.
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
    """
    Handles the POST requests on the '/slack/events' endpoint.

    This function receives POST requests on the '/slack/events' endpoint and passes them to the Slack app's event
    handler 'app_handler'. The 'app_handler.handle()' method processes the incoming request and generates
    the appropriate response.

    Parameters:
    req (Request): The incoming HTTP request.

    Returns:
    Response: The HTTP response generated by 'app_handler.handle()'.

    Note:
    The end point '/slack/events' is commonly used to listen to incoming events from Slack. Make sure your app is
    verified and 'Event Subscriptions' is enabled in your app configuration on Slack API.
    """

    return await app_handler.handle(req)


@api.get("/status")
async def get_status():
    """
    Handles GET requests to the '/status' endpoint.

    This function is a simple health check function that returns the status of the server when a GET request
    is sent to '/status'.

    Parameters:
    None

    Returns:
    dict: A dictionary with the key 'status' and the value 'Server is running' as the response to indicate that the server is up and running.

    Note:
    This endpoint is commonly used for health checking the server or the application.
    """

    return {"status": "Server is running"}


@api.get("/")
async def root():
    """
    Handles GET requests to the root ('/') endpoint.

    This function returns a dictionary response when a GET request is sent to the root endpoint ('/').

    Parameters:
    None

    Returns:
    dict: A dictionary with the key 'print' and the value 'Hello World' as the response.

    Note:
    This endpoint can be used as a basic check to ensure that the application is routing requests correctly.
    """

    x = {'print': 'Hello World'}
    return x


def get_ip_address():
    """
    Retrieves the IP address of the current machine.

    This function uses a UDP connection (which does not perform actual data sending) to a known server
    ("8.8.8.8" is typically used as it's a Google DNS server which is highly reliable) to determine the
    IP address of the local machine. The IP address is extracted from the socket's address information.

    Parameters:
    None

    Returns:
    str: The IP address of the local machine.

    Note:
    The function does not verify internet connectivity. The function just checks the preferred outgoing
    IP address of the computer, which may not be an actual online IP in cases where there's no actual
    internet connectivity.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":
    """
    This block of code is usually placed at the bottom of a Python script. It checks if the script is being run 
    directly and not being imported as a module. If true, it executes the block of code within it.

    Here, it calls the function 'get_ip_address()' to get the IP address of the local machine and assigns it to 'my_ip'.
    Then it starts a Uvicorn server with the application 'main:api' bound to localhost on port 3200 by calling 'uvicorn.run()'.
    The server's logging level is set to 'info' and the 'reload' option is set to 'True' which enables auto reloading of 
    the server when it detects code changes.

    Parameters:
    None

    Runs:
    Function 'get_ip_address' to get the local IP address.

    Returns:
    None. This is the script's entry point and isn't meant to be imported as a module, so it doesn't return a value.

    Note:
    This block is only run when the script is run directly. If the script is imported as a module, this block is not executed.
    """

    my_ip = get_ip_address()
    uvicorn.run("main:api", host=my_ip, port=3200, log_level="info", reload=True)
