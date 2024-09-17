from datetime import datetime as dt
from dev_slack import channels, slack_todo
import csv


def log_to_csv(id, user_image, user_name, button, key):
    """
    Logs the user interaction to a CSV file.

    The function records the details of user interaction into a CSV file named 'statistic_records.csv'.
    It appends a row with the user's ID, their image, their name, the button they've clicked,
    the key associated with the button, and the current date and time.

    Parameters:
    id (str): The ID of the user.
    user_image (str): The URL of the user's profile image.
    user_name (str): The name of the user.
    button (str): The button the user has clicked.
    key (str): The key associated with the button.
    """

    with open('statistic_records.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([id, user_image, user_name, button, key, dt.now()])


def button_reports(body, client, logger, text, key=None):
    """
    Reports a user interaction to Slack and logs it to a CSV file.

    This function retrieves user information, logs the interaction and then broadcasts a
    pre-formatted message in a Slack channel notifying about the user's interaction
    (action) along with other related information.

    Parameters:
    body (dict): A dictionary with Slack's action payload.
    client (any): Slack client that contains methods to interact with Slack API.
    logger (any): An instance of a logging class for logging purposes.
    text (str): The text or description of the interaction to be reported.
    key (str, optional): An optional key related to the interaction.

    Note:
    This function handles errors by logging them and doesn't halt the execution
    of the program if any error occurs in retrieving user's info.
    """

    day = dt.now().strftime('%d/%m/%Y %H:%M:%S')
    user = body["user"]["id"]
    response = client.users_info(user=user)
    if response["ok"]:
        # Extract username from the response
        user_name = response["user"]["profile"]["real_name"]
        user_image = response['user']['profile']['image_original']
    else:
        logger.error("Failed to retrieve user info")
    if key:
        report = f'{text} || {key}'
    else:
        report = f'{text}'

    log_to_csv(user, user_image, user_name, text, key)

    a = [

        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"> *ΑΝΑΦΟΡΑ ΔΡΑΣΤΗΡΙΟΤΗΤΑΣ*"
            }
        },
        {
            "type": "section",
            "block_id": "section567",
            "text": {
                "type": "mrkdwn",
                "text": f"> :slack: ΗΜΕΡΟΜΗΝΙΑ: *{day}*\n"
                        f"> :slack: ΧΡΗΣΤΗΣ: *{user_name}*\n"
                        f"> :slack: BUTTON: *{report}*"

            },
            "accessory": {
                "type": "image",
                "image_url": f"{user_image}",
                "alt_text": "apple"
            }
        },
        {
            "type": "context",
            "elements": [

                {
                    "type": "image",
                    "image_url": f"{user_image}",
                    "alt_text": f"{user_name}"}
                , {
                    "type": "mrkdwn",
                    "text": "Do you have something to include in the newsletter?\n"
                },
            ]
        }

    ]

    b = [{
        "type": "divider"
    }]

    # -------------------- DEFINE TEXT OUTPUT --------------------
    report = f"ΔΗΜΟΣΙΕΥΜΑ"
    # -------------------- SLACK BOT SEND TEXT --------------------
    slack_todo.send_text(report, channels.channels_id[1], blocks=a)
    # -------------------- SLACK BOT SEND DIVIDER --------------------
    slack_todo.send_text(report, channels.channels_id[1], blocks=b)
