#  Copyright (c) Ioannis E. Kommas 2024. All Rights Reserved
from typing import List, Dict
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def create_section(text, after=None):
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
    if after:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }, {
            "type": "divider"
        }
    else:
        return {
            "type": "divider"
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }


def create_block(simple, block_id, text, image, button_text, action_id):
    if simple:
        block_element = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": button_text, "emoji": True},
                    "style": "danger",
                    "value": "approve",
                    "action_id": action_id,
                },
            ],
        }
        block_element_2 = {
            "type": "divider"
        }
        return [block_element, block_element_2]
    else:
        block_element_1 = {
            "type": "section",
            "block_id": block_id,
            "text": {
                "type": "mrkdwn",
                "text": text
            },
            "accessory": {
                "type": "image",
                "image_url": image,
                "alt_text": ":mask:"
            }
        }

        block_element_2 = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":pushpin: Only Administrators can access this section."
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": button_text
                },

                "action_id": action_id
            }
        }
        block_element_3 = {
            "type": "divider"
        }

        return [block_element_1, block_element_2, block_element_3]


def expose_statistics():
    """
    Aggregate and expose button press statistics.

    This function reads from a CSV file named 'statistic_records.csv', which contains records of button presses from
    users. It aggregates these statistics both globally and on a per-user basis. It then formats the aggregated data
    into a Slack-friendly format called 'blocks' for easy message construction.

    Returns:
    list: A list of Slack blocks representing the statistics information.
    """
    df = pd.read_csv('data/statistic_records.csv')
    total_presses = df['report'].count()
    user_presses = df.groupby('username')['report'].count()

    # Group by both 'username' and 'report' and count the occurrences
    user_button_presses = df.groupby(['username', 'report']).size()

    # Count total button presses globally
    total_button_presses = df.groupby('report').size()

    user_images = df.groupby('username')['user_image'].last()

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


def run(event, admin, super_user):
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
    part_d = f""":gear: Ακολουθήστε μας:  \t<{os.getenv('FACEBOOK_LINK')}|:facebook: Facebook >
"""
    katastatiko = f""":gear: ΚΑΤΑΣΤΑΤΙΚΟ  \t<{os.getenv('KATASTATIKO')}|:pdf: ONLINE HERE >
:pushpin: Only Administrators can see this section."""
    mitroo = f""":gear: ΜΗΤΡΩΟ ΜΕΛΩΝ ΣΥΛΛΟΓΟΥ  \t<{os.getenv('MHTRO')}|:excel: ONLINE HERE>
:pushpin: Only Administrators can see this section."""

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
        {
            "type": "divider"
        },
    ]
    # block_id, text, image, button_text, action_id

    a = """
> *ΑΣΦΑΛΕΙΑ*: 🔑 ΜΟΝΟ ΜΕΛΗ ΔΣ
> *ΣΥΧΝΟΤΗΤΑ*: :date: MHNIAIO
> *ΠΟΛΥΕΤΑΙΡΙΚΟ*: OXI
    """
    b = """
> *ΑΣΦΑΛΕΙΑ*: 🔑 ΜΟΝΟ ΜΕΛΗ ΔΣ
> *ΣΥΧΝΟΤΗΤΑ*: :date: ΕΒΔΟΜΑΔΙΑΙΟ
> *ΠΟΛΥΕΤΑΙΡΙΚΟ*: NAI
    """

    admin_buttons_texts_ids = [
        (0, "block_id_c", a, os.getenv('FILARMONIKI_LOGO'), ":card_index_dividers: ΑΡΧΕΙΟ ΟΙ ΑΙΤΗΣΕΙΣ ΜΑΣ",
         "request_arxeio"),
        (0, "block_id_d", b, os.getenv('AGIOS_NIKOLAOS_LOGO'), ":card_index_dividers: ΠΡΑΚΤΙΚΑ ΓΕΝΙΚΩΝ ΣΥΝΕΛΕΥΣΕΩΝ",
         "request_sinelefsi"),
        (0, "block_id_e", a, os.getenv('FILARMONIKI_LOGO'), ":card_index_dividers: ΠΡΑΚΤΙΚΑ ΔΙΟΙΚΗΤΙΚΟΥ ΣΥΜΒΟΥΛΙΟΥ",
         "request_ds"),
        (0, "block_id_f", a, os.getenv('FILARMONIKI_LOGO'), ":card_index_dividers: ΒΙΒΛΙΟ ΕΣΟΔΩΝ ΕΞΟΔΩΝ",
         "request_money"),
        (0, "block_id_g", a, os.getenv('FILARMONIKI_LOGO'), ":card_index_dividers: ΒΙΒΛΙΟ ΠΕΡΙΟΥΣΙΑΚΩΝ ΣΤΟΙΧΕΙΩΝ",
         "request_periousia"),
        (0, "block_id_h", a, os.getenv('FILARMONIKI_LOGO'), ":card_index_dividers: ΠΡΩΤΟΚΟΛΛΟ ΑΛΛΗΛΟΓΡΑΦΙΑΣ",
         "request_protocol"),
    ]

    if admin:
        a = create_section(katastatiko, 1)
        blocks.extend(a,)
        b = create_section(mitroo, 1)
        blocks.extend(b)
        for simple, block_id, text, image, button_text, action_id in admin_buttons_texts_ids:
            action_block = create_block(simple, block_id, text, image, button_text, action_id)
            blocks.extend(action_block)
    if super_user:
        blocks.extend(expose_statistics())

    return {
        "type": "home",
        "blocks": blocks
    }
