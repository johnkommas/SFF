from dev_slack import functions


def handle_archive_step_b(view):
    """
    Διαβάζει τις ημερομηνίες έναρξης και Λήξης
    :param view:
    :return: None
    """

    key = view['state'].get('values').keys()
    key = list(key)
    selected_value = view["state"]["values"][key[0]]["archive_step_b"]["selected_option"]["value"]
    return selected_value


def choose_archive():
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
    image = 'filarmoniki.png'

    # Read the text from a .txt file
    with open('phones.txt', 'r') as file:
        text = file.read()

    return {
            "type": "modal",
            "title": {"type": "plain_text", "text": "ΤΗΛΕΦΩΝΑ", "emoji": True},
            "blocks": [
                {
                "type": "image",
                "image_url": f"https://raw.githubusercontent.com/johnkommas/CodeCademy_Projects/master/img/{image}",
                "alt_text": "name",
            },

                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": text},
                }
            ],
        }