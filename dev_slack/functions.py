import json


def load_requests():
    """
    Function to load the request data from the json file.
    :return: Dictionary object containing the request data
    """
    with open('requests.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def create_section(part_text, image_url):
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
    hyperlink = 'https://raw.githubusercontent.com/johnkommas/CodeCademy_Projects/master/img/'
    image_urls = [f"{hyperlink}{img}" for img in ['Signpng.png', 'images.png', 'onedrive.png']]

    management_map = {
        'management_a': 'ΣΥΝΕΛΕΥΣΗ ΔΣ',
        'management_b': 'ΥΠΟΓΡΑΦΗ', }

    municipality_map = {
        'municipality_a': f'{protocol}',
        'municipality_b': 'ΑΡΜΟΔΙΑ ΥΠΗΡΕΣΙΑ',
        'municipality_c': 'ΘΕΜΑ ΣΤΟ ΣΥΜΒΟΥΛΙΟ',
        'municipality_d': 'ΑΠΟΦΑΣΗ'}

    onedrive_map = {
        'onedrive_link_a': '(PDF) ΑΡΧΙΚΟ ΑΙΤΗΜΑ '
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
    requests = load_requests()
    all_keys = list(requests.keys())
    for key, value in requests.items():
        # Fetch request details using the protocol number
        request_data = requests.get(key)
        # Display the status of the request
        display_status(request_data, key)
