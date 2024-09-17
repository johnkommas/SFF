#  Copyright (c) Ioannis E. Kommas 2024. All Rights Reserved
from typing import List, Dict
import pandas as pd


def create_section(text):
    """
        Creates a section block for a Slack message along with a divider.

        This function creates a section block for a Slack message, which is
        suitable to display text information. This function also adds a divider
        block preceding the section.

        Parameters:
        text (str): The text content to display in the section block.

        Returns:
        tuple: A tuple containing a dictionary for the divider block and a
        dictionary for the section block.
    """
    return {
        "type": "divider"
    }, {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        }
    }


def create_action_block(buttons: List[Dict]) -> Dict[str, List[Dict]]:
    """
        Creates an action block for a Slack message.

        This function creates an action block which holds interactive components
        like buttons. The `buttons` parameter should be a List of Dicts where each
        Dict defines a button (in Slack button JSON format).

        Parameters:
        buttons (List[Dict]): A list of dictionaries where each dictionary is a
        Slack formatted button component.

        Returns:
        dict: A dictionary representing a Slack 'action' block containing all
        supplied buttons.
    """
    return {
        "type": "actions",
        "elements": buttons
    }


def create_button(text: str, action_id: str) -> Dict[str, str]:
    """
        Creates a button for a Slack message.

        This function creates a single Slack formatted button component
        with plain text and a specified action ID.

        Parameters:
        text (str): The text to be displayed on the button.
        action_id (str): A unique identifier for the button. When the button is
                         clicked, Slack sends an interaction payload which
                         includes actions and the `action_id`.

        Returns:
        dict: A dictionary representing a Slack 'button' component.
    """
    return {
        "type": "button",
        "text": {"type": "plain_text", "text": text, "emoji": True},
        # "style": "danger",
        "value": "approve",
        "action_id": action_id,
    }


def expose_statistics():
    """
    Aggregate and expose button press statistics.

    This function reads from a CSV file named 'statistic_records.csv', which contains records of button presses from
    users. It aggregates these statistics both globally and on a per-user basis. It then formats the aggregated data
    into a Slack-friendly format called 'blocks' for easy message construction.

    Returns:
    list: A list of Slack blocks representing the statistics information.
    """
    df = pd.read_csv('statistic_records.csv')
    total_presses = df['report'].count()
    user_presses = df.groupby('username')['report'].count()

    # Group by both 'username' and 'report' and count the occurrences
    user_button_presses = df.groupby(['username', 'report']).size()

    # Count total button presses globally
    total_button_presses = df.groupby('report').size()

    user_images = df.groupby('username')['user_image'].first()

    blocks = [
        {"type": "divider"},
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Statistics"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Total Button Presses:* {total_presses}"
            }
        },
    ]

    # Sort `total_button_presses` by count/value
    sorted_total_presses = sorted(total_button_presses.items(), key=lambda item: item[1], reverse=True)

    elements = [
        {"type": "mrkdwn",
         "text": f"`{'█' * int((count / total_presses) * 10) + ' ' * (10 - int((count / total_presses) * 10))}` "
                 f"({button}: {count / total_presses * 100:.1f}% - {count} times)"
         } for button, count in sorted_total_presses
    ]

    blocks.append({
        "type": "context",
        "elements": elements
    })

    blocks.append({"type": "divider"})
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "User's Statistics"
        }
    })
    for user, presses in user_presses.items():
        user_reports = user_button_presses[user]
        user_image = user_images[user]

        # Add user's profile picture to blocks
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{user}:*\n> Total:{presses}"
            },
            "accessory": {
                "type": "image",
                "image_url": user_image,
                "alt_text": f"{user}'s profile picture"
            }
        })

        # Sort `user_reports` by count/value
        sorted_reports = sorted(user_reports.items(), key=lambda item: item[1], reverse=True)

        elements = [
            {"type": "mrkdwn",
             "text": f"`{'█' * int((count / presses) * 10) + ' ' * (10 - int((count / presses) * 10))}` "
                     f"({button}: {count / presses * 100:.1f}% - {count} times)"
             } for button, count in sorted_reports
        ]

        blocks.append({
            "type": "context",
            "elements": elements
        })

        blocks.append({"type": "divider"})

    return blocks


def run(event, admin):
    """
    Generate a block kit suitable for a Home tab view in a Slack App.

    This function creates a formatted collection of message blocks for a Home tab view in Slack. It includes several statically defined message sections and buttons. If the user has admin permissions, additional buttons and statistical data are added to the view.

    Parameters:
    event (dict): A dictionary containing data about the triggering event, such as the user ID of the user who interacted with the button.
    admin (bool): A boolean specifying if the user has admin permissions.

    Returns:
    dict: A dictionary representing a Slack Home tab view in block kit format.
    """

    part_a = f"""
\tΣκοπός του Συλλόγου είναι η υποστήριξη της Δημοτικής :musical_note:Φιλαρμονικής της πόλης της Νεάπολης Λασιθίου, η διάδοση, ανάδειξη και παραγωγή πολιτιστικών δραστηριοτήτων, στην ευρύτερη περιοχή του Δήμου Αγίου Νικολάου, η συνεργασία με άλλα ομοειδή σωματεία, σε όλη την επικράτεια, η συνένωση όλων των κατοίκων της Νεάπολης σε μια μαζική οργάνωση για την ανάδειξη των δραστηριοτήτων της :notes:Φιλαρμονικής της πόλης, η βελτίωση και καλυτέρευση της πολιτιστικής και κοινωνικής ζωής των κατοίκων της Νεάπολης με κάθε πρόσφορο μέσο, η μελέτη, προώθηση και επίλυση κάθε θέματος που αφορά την μουσική δραστηριότητα στην πόλη.
"""
    part_b = f"""
\tΤα μέσα για την επίτευξη του παραπάνω μη κερδοσκοπικού σκοπού είναι κυρίως: η παροχή :handshake: κάθε είδους βοήθειας και δη οικονομικής :moneybag: και υλικοτεχνικής στην Φιλαρμονική της Νεάπολης, όπως όργανα :musical_keyboard:, στολές, κ.λ.π, η πραγματοποίηση πολιτιστικών εκδηλώσεων και ειδικότερα μουσικών συναυλιών :microphone:, η ενεργή συμμετοχή στις κάθε είδους εκδηλώσεις που αφορούν εθνικές επετείους :calendar:, θρησκευτικές εορτές :church: και δημοτικές εκδηλώσεις, και κάθε εν γένει δραστηριότητα που προσιδιάζει στην φύση και τον προορισμό του Συλλόγου ως πολιτιστικού :museum: με γνώμονα πάντα την πνευματική ανάπτυξη της πόλης της Νεάπολης καθώς και κάθε άλλη νομική :scales: ή υλική πράξη που κρίνεται αναγκαία από τα αρμόδια όργανα για την επίτευξη των στόχων του Σωματείου :dart:.
"""
    part_c = f"""
\tΓια την πληρέστερη :dart: επιτυχία των επιδιώξεών του, το σωματείο θα επιδιώκει τη συνεργασία :handshake: με όλα τα ομοειδή Σωματεία της ευρύτερης περιοχής του Νομού Λασιθίου, με τον Δήμο Αγίου Νικολάου:office: , τη Δημοτική Κοινότητα Νεάπολης:cityscape: και εν γένει φορείς οι οποίοι έχουν στο καταστατικό τους κοινούς ή όμοιους σκοπούς:flags:.
"""
    part_d = f""":gear: Ακολουθήστε μας:  \t<https://www.facebook.com/profile.php?id=61565483531332|:facebook: Facebook >
"""

    sections = [
        create_section(part_a),
        # create_section(part_b),
        # create_section(part_c),
        create_section(part_d),
    ]

    sections_flat = [section for section_tuple in sections for section in section_tuple]

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f" *:rocket: Καλώς Ορίσατε, <@{event['user']}> :house: στο κανάλι μας*\n\n\n\n"
                        "*:wave:Σύντομος Χαιρετισμός, ο Σκοπός του Συλλόγου μας*"
            }
        }, *sections_flat,
        {
            "type": "divider"
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": ":link: ΤΗΛΕΦΩΝΑ ΕΠΙΚΟΙΝΩΝΙΑΣ", "emoji": True},
                    "style": "primary",
                    "value": "approve",
                    "action_id": "reuest_phones",
                },
            ],
        },
    ]

    admin_buttons_texts_ids = [
        (":card_index_dividers: ΚΑΤΑΣΤΑΤΙΚΟ ΣΥΛΛΟΓΟΥ", "request_katastatiko"),
        (":card_index_dividers: ΑΡΧΕΙΟ ΟΙ ΑΙΤΗΣΕΙΣ ΜΑΣ", "request_arxeio"),
        (":card_index_dividers: ΑΡΧΕΙΟ ΣΥΝΕΛΕΥΣΕΙΣ ΔΣ", "request_sinelefsi"),
    ]

    if admin:
        for text, action_id in admin_buttons_texts_ids:
            button = create_button(text, action_id)
            action_block = create_action_block([button])
            blocks.append(action_block)
        blocks.extend(expose_statistics())

    return {
        "type": "home",
        "blocks": blocks
    }
