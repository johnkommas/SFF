#  Copyright (c) Ioannis E. Kommas 2024. All Rights Reserved

from dev_slack import functions
import json
import os
from dotenv import load_dotenv
load_dotenv()

def handle_archive_step_b(view):
    """
        Extracts the selected archive date from the view.

        This function reads the data from a Slack view and extracts the selected start and end dates
        from the 'archive_step_b' component.

        Parameters:
        view (dict): A dictionary representing the state of the Slack view from which the dates are
                     to be extracted.

        Returns:
        str: The value of the selected option in 'archive_step_b' component.
    """

    key = view['state'].get('values').keys()
    key = list(key)
    selected_value = view["state"]["values"][key[0]]["archive_step_b"]["selected_option"]["value"]
    return selected_value


def choose_katastatiko():
    """
    Creates a modal view for katastatiko search.

    This function generates a modal view in Slack that allows users to choose from a list of requests.
    The requests are loaded into the options for a static select menu, and the selected request's key
    is returned when the user submits the form.

    Returns:
    dict: A dictionary representing a Slack modal view with a static select menu of requests.
    """
    image_url = os.getenv('FILARMONIKI_LOGO')
    text = f'<{os.getenv('KATASTATIKO')}|ΚΑΤΑΣΤΑΤΙΚΟ>'
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "ΚΑΤΑΣΤΑΤΙΚΟ", "emoji": True},
        "blocks": [
            {
                "type": "image",
                "image_url": image_url,
                "alt_text": "name",
            },

            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": text},
            }
        ],
    }



def choose_archive():
    """
    Creates a modal view for archive search.

    This function generates a modal view in Slack that allows users to choose from a list of requests.
    The requests are loaded into the options for a static select menu, and the selected request's key
    is returned when the user submits the form.

    Returns:
    dict: A dictionary representing a Slack modal view with a static select menu of requests.
    """

    my_options = []
    requests = functions.load_requests()
    for key, value in requests.items():
        my_options.append({
            "text": {
                "type": "plain_text",
                "emoji": True,
                "text": value.get('name').upper()
            },
            "value": key
        })

    return {
        "type": "modal",
        "callback_id": "button_archive_step_b",
        "submit": {
            "type": "plain_text",
            "text": "ΑΝΑΖΗΤΗΣΗ",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "ΑΚΥΡΩΣΗ",
            "emoji": True
        },
        "title": {
            "type": "plain_text",
            "text": ":sffn: ΈΝΑΡΞΗ ΑΝΑΖΗΤΗΣΗΣ",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "ΣΥΛΛΟΓΟΣ ΦΙΛΩΝ ΦΙΛΑΡΜΟΝΙΚΗΣ ΝΕΑΠΟΛΕΩΣ",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*ΑΙΤΗΣΕΙΣ ΠΡΟΣ: ΔΗΜΟ ΑΓ. ΝΙΚΟΛΑΟΥ*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "ΕΠΙΛΕΞΤΕ",
                        "emoji": True
                    },
                    "options": my_options,
                    "action_id": "archive_step_b"
                }
            }
        ]
    }


def represent_data(key):
    """
    Creates a modal to represent search results.

    Given a key, this function retrieves a collection of requests, then generates
    a representation of the status of the request associated with that key. The generated
    status is used to create a Slack modal that presents the results to the user.

    Parameters:
    key (str): The key representing the request to find in the loaded requests.

    Returns:
    dict: A dictionary representing a Slack modal with content containing the data
          from the selected request.
    """

    requests = functions.load_requests()
    data = functions.display_status(requests, key)

    return {
        "type": "modal",

        "close": {
            "type": "plain_text",
            "text": "ΤΕΛΟΣ",
            "emoji": True
        },
        "title": {
            "type": "plain_text",
            "text": "ΑΠΟΤΕΛΕΣΜΑΤΑ",
            "emoji": True
        },
        "blocks": data
    }


def send_phones():
    """
    Creates a modal with contact phone numbers.

    This function creates a Slack modal that shows an image and displays a list of
    phone numbers from a text file 'phones.txt'.

    Returns:
    dict: A dictionary representing a Slack modal with an image block and section block containing phone numbers.
    """

    image = os.getenv('FILARMONIKI_PHOTO')

    # Read the text from a .txt file
    with open('data/phones.txt', 'r') as file:
        text = file.read()

    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "ΤΗΛΕΦΩΝΑ", "emoji": True},
        "blocks": [
            {
                "type": "image",
                "image_url": image,
                "alt_text": "name",
            },

            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": text},
            }
        ],
    }


def format_data_for_slack(data):
    image_url = os.getenv('AGIOS_NIKOLAOS_LOGO')
    blocks = []
    for (outer_key, outer_value) in data.items():
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{outer_key}*"
            },
            "accessory": {
                "type": "image",
                "image_url": image_url,
                "alt_text": 'image'
            }
        })
        for (inner_key, nested_dict) in outer_value.items():
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_{inner_key}_"
                }
            })
            for key, value in nested_dict.items():
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{key}:* {value}"
                    }
                })
            blocks.append({"type": "divider"})
    return blocks


def send_request_sinelefsi():
    with open("data/meetings.json", "r") as read_file:
        data = json.load(read_file)

    blocks = format_data_for_slack(data)

    view = {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Meeting Info"
        },
        "blocks": blocks
    }

    return view
