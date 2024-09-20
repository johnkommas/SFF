#  Copyright (c) Ioannis E. Kommas 2024. All Rights Reserved

from dev_slack import slack_todo, channels


def initialize_button(represent):
    """
    Function to initialize a button for a Slack message.

    Args:
        represent (str): The representational text used for the button in the Slack message.

    Returns:
        list: A list containing a dictionary with the structure of a Slack message button.

    """
    return [
        # TEST_STARTS_

        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{represent}* :raised_hands:"

            },

        },

    ]
    # TEST END


def set_status(represent, cid):
    """
    Function to set a status in a specific Slack channel.
    The previous status (if any) is deleted before the new one is set.

    Args:
        represent (str): The representational text used to generate the Slack message button.
        cid : The channel id where the status is being set.

    Returns:
        None
    """
    try:
        slack_todo.delete_with_specific_text(channel_id=channels.channels_id[cid], text="ONLINE OFFLINE")
    except Exception as e:
        print(f"An error occurred While Trying To Delete Specific Message from Channel {channels.channels[cid]}: {e}")
    finally:
        print(f"BOT ACTION DELETE: {channels.channels[cid]}")
    btn = initialize_button(represent)
    try:
        slack_todo.send_text("ONLINE OFFLINE", channels.channels_id[cid], btn)
    except Exception as e:
        print(f"An error occurred While Trying to Send a Message in Channel {channels.channels[cid]}: {e}")
    finally:
        print(f"BOT ACTION SEND: {channels.channels[cid]}")
