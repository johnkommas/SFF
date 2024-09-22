#  Copyright (c) Ioannis E. Kommas 2024. All Rights Reserved

import json
import os
from dotenv import load_dotenv
load_dotenv()


def load_requests():
    """
    Function to load the request data from the json file.
    :return: Dictionary object containing the request data
    """
    with open('data/requests.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def create_section(part_text, image_url):
    """
        Create a Slack 'section' block.

        This function is used to generate one Slack message 'section' block.
        A 'section' block is one of the many block layouts available in Slack
        and it is suitable for text and image display.

        Parameters:
        part_text (str): The text that will be displayed in the section.
        image_url (str): The URL of the image that will be displayed on the side of the text.

        Returns:
        dict: Returns a dictionary formatted as a Slack 'section' block.
    """
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": part_text
        },
        "accessory": {
            "type": "image",
            "image_url": image_url,
            "alt_text": "Airstream Suite"
        }
    }


def display_status(request, protocol):
    """
    Function to display the status of a request in the format.
    :param: request_info: Dictionary with the request details
    :param: protocol: String that represents the protocol number
    :return: None
    """
    request_info = request.get(protocol)
    image_urls = [os.getenv('FILARMONIKI_LOGO'), os.getenv('AGIOS_NIKOLAOS_LOGO'), os.getenv('ONE_DRIVE_LOGO')]

    management_map = {
        'management_a': 'ΣΥΝΕΛΕΥΣΗ ΔΣ',
        'management_b': 'ΥΠΟΓΡΑΦΗ', }

    municipality_map = {
        'municipality_a': f'{protocol}',
        'municipality_b': 'ΑΡΜΟΔΙΑ ΥΠΗΡΕΣΙΑ',
        'municipality_c': 'ΘΕΜΑ ΣΤΟ ΣΥΜΒΟΥΛΙΟ',
        'municipality_d': 'ΑΠΟΦΑΣΗ'}

    onedrive_map = {
        'onedrive_link_a': ':pdf: ΑΡΧΙΚΟ ΑΙΤΗΜΑ '
    }

    onedrive_pins = {
        'onedrive_pin_a': '|| 🔑'
    }

    management_part = ''
    municipality_part = ''
    onedrive_part = ''

    for stage, label in management_map.items():
        if stage_info := request_info.get(stage):
            management_part += f"{stage_info} || {label} \n\n"

    for stage, label in municipality_map.items():
        if stage_info := request_info.get(stage):
            municipality_part += f"{stage_info} || {label} \n\n"

    for (stage, label), (stage_keys, label_keys) in zip(onedrive_map.items(), onedrive_pins.items()):
        if stage_info := request_info.get(stage):
            onedrive_part += f"<{stage_info}|{label}> {label_keys} {request_info.get(stage_keys)}"

    sections_list = [
        create_section(management_part, image_urls[0]),
        {
            "type": "divider"
        },
        create_section(municipality_part, image_urls[1]),
        {
            "type": "divider"
        },
        create_section(onedrive_part, image_urls[2])
    ]
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f"{request_info.get('name').upper()}",
                "emoji": True
            }
        },
        {
            "type": "divider"
        },
        *sections_list
    ]


def check():
    """
    Check the status of all requests.

    This function iterates over all the requests in the system and displays
    their status. The function does this by:
    - Loading all available requests
    - Iterating through every request
    - Fetching detailed data for each specific request
    - Displaying the status of each request

    Parameters:
    None

    Returns:
    None
    """
    requests = load_requests()  # Load all existing requests
    all_keys = list(requests.keys())  # Get all request keys
    for key, value in requests.items():  # Iterate over each request
        request_data = requests.get(key)  # Retrieve specific request data
        display_status(request_data, key)  # Display status of the request
