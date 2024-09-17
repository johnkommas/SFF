from datetime import datetime as dt
from dev_slack import channels, slack_todo
import csv


def log_to_csv(id, user_image, user_name, button, key):
    with open('statistic_records.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([id, user_image, user_name, button, key, dt.now()])


def button_reports(body, client, logger, text, key=None):
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
