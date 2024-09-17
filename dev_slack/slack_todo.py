#  Copyright (c) Ioannis E. Kommas 2024. All Rights Reserved

import logging
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
import json
import os
from dev_slack import channels
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)
client = WebClient(token=os.getenv('SLACK_TOKEN'))


def delete(channel_id, message_id):
    try:
        # Call the chat.chatDelete method using the built-in WebClient
        result = client.chat_delete(
            channel=channel_id,
            ts=message_id
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error deleting message: {e}")


def get_from_text_history(channel_id, text):
    try:
        x = (history(channel_id))
        thread_id = ''
        for message in x:
            # print(message.get('text'))
            if message.get('text').startswith(text):
                thread_id = message.get('ts')
        return thread_id
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))


def delete_with_specific_text(channel_id, text):
    delete(channel_id, get_from_text_history(channel_id, text))


def history(channel_id):
    try:
        result = client.conversations_history(channel=channel_id)
        conversation_history = result["messages"]
        logger.info("{} messages found in {}".format(len(conversation_history), id))
        return conversation_history
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))


def remove(channel_id, lenght=0):
    try:
        while True:
            x = (history(channels.channels_id[channel_id]))
            bot_messages = []
            if len(x) > lenght:
                for message in x:
                    if message.get('user') == os.getenv('SLACK_BOT') and \
                            message.get('reply_count', 0) == 0 and \
                            message.get('reactions', 0) == 0:
                        bot_messages.append(message)

                    else:
                        break
            if len(bot_messages) > 0:
                for i, message in enumerate(bot_messages):
                    percent = int((100 * (i + 1)) / len(bot_messages))
                    filler = "█" * (percent // 2)
                    remaining = '-' * ((100 - percent) // 2)
                    timer = (bot_messages[i]['ts'])
                    delete(channels.channels_id[channel_id], timer)
                    # print(f'\rDELETING SLACK FILES DONE:[{filler}{remaining}]{percent}%', end='', flush=True)
            else:
                break
            # print()
    except Exception:
        print("Slack Remove Exception")
        return remove(channel_id)


def send_text(txt, channel_id, blocks=None):
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=txt,
            blocks=json.dumps(blocks) if blocks else None
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


def send_text_to_user(txt, channel_id, blocks=None):
    try:
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel_id,
            text=txt,
            blocks=json.dumps(blocks) if blocks else None,
            as_user = True
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


def send_files(txt, file_name, channel_id):
    try:
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        result = client.files_upload(
            channels=channel_id,
            initial_comment=txt,
            file=file_name,
        )
        # Log the result
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))


def chat_block_update(txt, channel_id, posted_text, blocks=None):
    x = history(channel_id)
    # print(x)
    for message in x:
        try:
            # print(message['blocks'][0]['text'].get('text'))
            if message['blocks'][0]['text'].get('text').startswith(posted_text):
                timestamp = message.get('ts')
        except Exception:
            continue
    try:
        result = client.chat_update(
            channel=channel_id,
            text=txt,
            ts=timestamp,
            blocks=json.dumps(blocks) if blocks else None
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


def update(txt, channel_id, posted_text, blocks=None):
    x = history(channel_id)
    # print(x)
    for message in x:
        try:
            # print(message.get('text'))
            if message.get('text').startswith(posted_text):
                timestamp = message.get('ts')
        except Exception:
            continue
    try:
        result = client.chat_update(
            channel=channel_id,
            text=txt,
            ts=timestamp,
            blocks=json.dumps(blocks) if blocks else None
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")


def get_thread_ts(c_id, posted_text):
    try:
        x = (history(channels.channels_id[c_id]))
        thread_id = ''
        for message in x:
            # prints the names of the threads copy Paste them
            # print(message.get('text'))
            if message.get('text') == posted_text:
                thread_id = message.get('ts')
        # quit()
        return thread_id
    except Exception as e:
        print("Slack Thread TS Exception")
        logger.error(f"Error posting message: {e}")
        return get_thread_ts(c_id, posted_text)


def send_text_on_specific_thread(text, channel, posted_text, c_id, blocks=None):
    try:
        ts = get_thread_ts(c_id, posted_text)
        # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=channel,
            text=text,
            thread_ts=ts,
            blocks=json.dumps(blocks) if blocks else None
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}")
        print("Slack Text on Thread Exception")
        return send_text_on_specific_thread(text, channel, posted_text, c_id, blocks=None)


def send_files_on_specific_thread(file_name, file_path, file_type, channel, c_id, posted_text):
    try:
        ts = get_thread_ts(c_id, posted_text)
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        result = client.files_upload(
            channels=channel,
            initial_comment='',
            file=file_name,
            thread_ts=ts
        )
        # Log the result
        logger.info(result)

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))
        print("Slack File on Thread Exception")
        return send_files_on_specific_thread(file_name, file_path, file_type, channel, c_id, posted_text)


def replies(channel, thread_ts):
    try:
        result = client.conversations_replies(
            channel=channel,
            ts=thread_ts
        )
        logger.info(result)
        return result

    except SlackApiError as e:
        logger.error("Error on replies {}".format(e))
        print("Slack Replies Exception")
        return replies(channel, thread_ts)


def remove_from_specific_thread(c_id, posted_text):
    try:
        thread_id = get_thread_ts(c_id, posted_text)
        x = replies(channels.channels_id[c_id], thread_id)
        try:
            for message in x['messages']:
                if message.get('ts') != thread_id and message.get('user') == os.getenv('SLACK_BOT'):
                    # and not message.get('text').startswith('&gt; :appleinc:'):
                    # print(message.get('ts'))
                    timer = message.get('ts')
                    delete(channels.channels_id[c_id], timer)
        except SlackApiError as e:
            print('error occured')
    except SlackApiError as e:
        print("Slack Remove from Thread Exception")
        return remove_from_specific_thread(c_id, posted_text)
