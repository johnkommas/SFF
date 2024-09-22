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
    """
    Deletes a specified message from a specific Slack channel.

    This function uses the built-in WebClient to call Slack's chat.delete method
    to delete a message specified by its timestamp from the provided channel.

    Parameters:
    channel_id (str): The ID of the channel from which the message is to be deleted.
    message_id (str): The timestamp of the message to be deleted.

    Exceptions:
    SlackApiError: If there is any error in deleting the message, a SlackApiError is raised which is then caught and logged.
    """

    try:
        # Call the chat.chatDelete method using the built-in WebClient
        result = client.chat_delete(
            channel=channel_id,
            ts=message_id
        )
        logger.info(result)


    except SlackApiError as e:

        if e.response['error'] == 'ratelimited':
            logger.error('Rate limit hit')
        else:
            logger.error(f"Error deleting message: {e}")


def get_from_text_history(channel_id, text):
    """
    Fetches the timestamp of a message starting with a specific text from the channel's history.

    This function goes through the messages in a channel's history and returns the timestamp
    (Thread ID) of the first message starting with the given text.

    Parameters:
    channel_id (str): The ID of the channel from which the history is to be fetched.
    text (str): The beginning text of the message whose Thread ID is to be returned.

    Returns:
    str: The timestamp (Thread ID) of the message. Empty string if such message is not found.

    Raises:
    SlackApiError: If an error occurs while fetching the history, a SlackApiError is raised
    and the error info is logged.
    """

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
    """
    Deletes a message starting with a specific text from a given channel.

    This function uses the helper functions 'get_from_text_history' to get the timestamp
    of a message starting with the given text from a channel's history, and 'delete' to
    delete that message using its timestamp.

    Parameters:
    channel_id (str): The ID of the channel from which the message is to be deleted.
    text (str): The beginning text of the message to be deleted.

    Note:
    This function deletes the first occurrence of a message starting with the specified text from the channel's history. It doesn't affect any subsequent messages in the channel that start with the same text.
    """

    delete(channel_id, get_from_text_history(channel_id, text))


def history(channel_id):
    """
    Fetches the history of messages from a given Slack channel.

    This function uses the method 'conversations_history' from the Slack client to get a
    conversation's history and logs the number of messages it found.

    Parameters:
    channel_id (str): The ID of the channel from which the history is fetched.

    Returns:
    list: A list of messages found in the conversation's history.

    Raises:
    SlackApiError: If any error occurs while fetching the conversation's history, a
    SlackApiError is raised and the error info is logged.
    """

    try:
        result = client.conversations_history(channel=channel_id)
        conversation_history = result["messages"]
        logger.info("{} messages found in {}".format(len(conversation_history), id))
        return conversation_history
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))


def remove(channel_id, lenght=0):
    """
    Deletes certain messages from a specified Slack channel based on particular criteria.

    This function retrieves the message history from a channel based on the channel ID
    and filters for messages sent by a particular bot that have no replies or reactions.
    It deletes any such messages found and repeats the process until no such messages remain.

    Parameters:
    channel_id (str): The ID of the channel from which the messages are to be deleted.
    lenght (int, optional): A placeholder parameter with no apparent usage in the current function context.
                            Defaults to 0.

    Raises:
    Exception: If any exception occurs during the process, a recursive call is made to
               try the deletion process again.

    Note:
    The function aims to delete bot messages only if they have no replies or reactions.
    If a non-bot message or a bot message with replies/reactions is encountered, the function breaks the deletion phase
    and repeats the fetching and filtering process.

    Environment Variables:
    SLACK_BOT: This should contain the user id of the bot whose messages are to be deleted.
               This id is used to filter out the messages in the channel's history.
    """

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
    """
    Sends a message with optional blocks to a specified Slack channel.

    This function uses the 'chat.postMessage' method from the Slack client to post a message
    to a given channel. The 'blocks' parameter, if provided, is included in the message as
    structured elements like sections, dividers, or image blocks.

    Parameters:
    txt (str): The main text of the message to be sent.
    channel_id (str): The ID of the channel to which the message is to be sent.
    blocks (list, optional): A list of block structures to include in the message. Defaults to None.

    Raises:
    SlackApiError: If any error occurs while posting the message, a SlackApiError is raised
    and the error info is logged.
    """

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
    """
    Sends a message with optional blocks to a specified Slack channel as the authenticated user.

    This function uses the 'chat.postMessage' method from the Slack client to post a message
    to a given channel as the authenticated user. The 'blocks' parameter, if provided, is included
    in the message as structured elements like sections, dividers, or image blocks.

    Parameters:
    txt (str): The main text of the message to be sent.
    channel_id (str): The ID of the channel to which the message is to be sent.
    blocks (list, optional): A list of block structures to include in the message. Defaults to None.

    Raises:
    SlackApiError: If an error occurs while posting the message, a SlackApiError is raised
    and the error info is logged.
    """

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
    """
    Sends a file to a specified Slack channel with an initial comment.

    This function uses the 'files.upload' method from the Slack client to upload a file
    to a given channel. An initial comment can be added to the file upon upload.

    Parameters:
    txt (str): Initial comment to add to the file.
    file_name (str): The name of the file to be uploaded.
    channel_id (str): The ID of the channel to which the file is to be uploaded.

    Raises:
    SlackApiError: If an error occurs while uploading the file, a SlackApiError is raised
    and the error info is logged.

    Note:
    Uploading files requires the `files:write` scope for the bot/user token.
    """

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
    """
    Updates a message in a specified Slack channel, optionally with blocks.

    This function uses the 'chat.update' method from the Slack client to update a message
    in a given channel that starts with a specific text. The 'blocks' parameter, if provided,
    is included in the updated message as structured elements like sections, dividers, or image blocks.

    Parameters:
    txt (str): The updated text of the message.
    channel_id (str): The ID of the channel where the message is located.
    posted_text (str): The starting text of the original message that needs to be updated.
    blocks (list, optional): A list of block structures to include in the updated message. Defaults to None.

    Raises:
    SlackApiError: If any error occurs while updating the message, a SlackApiError is raised
    and the error info is logged.

    Note:
    The function retrieves the history of the channel and updates the first message it finds
    which starts with the 'posted_text'. If no such message is found, it may throw an error due
    to undefined 'timestamp' variable.
    """

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
    """
    Updates a message in a specified Slack channel, potentially with block structures.

    This function uses the 'chat.update' method from the Slack client to update a particular
    message in a given channel. The specific message to be updated is the one that starts with
    a specific text. If the 'blocks' parameter is provided, it is included in the updated message
    as structured elements.

    Parameters:
    txt (str): The updated text for the message.
    channel_id (str): The ID of the channel where the message to be updated is located.
    posted_text (str): The starting text of the message that will be updated.
    blocks (list, optional): A list of block structures that will be included in the updated
                             message, if provided. Defaults to None.

    Raises:
    SlackApiError: If an error occurs while updating the message, a SlackApiError is raised
                   and the error message is logged.

    Note:
    The function retrieves the history of the channel and identifies the first message it
    finds that starts with the 'posted_text'. This is the message that will be updated.
    If no such message is found, it may produce an error due to the 'timestamp' variable
    being undefined.
    """

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
    """
    Retrieves the thread timestamp for a specific message in a given Slack channel.

    This function pulls the history of a provided channel and searches for a message
    that matches the 'posted_text'. It then retrieves the timestamp of that message,
    which is used as identifiers for threads in Slack.

    Parameters:
    c_id (str): The consumer key of the channel where the message is located.
    posted_text (str): The exact text of the message whose thread timestamp is to be retrieved.

    Returns:
    str: The timestamp of the thread corresponding to the 'posted_text' message. If no such
    message is found, it recursively calls itself until a message is found.

    Raises:
    Exception: If an error occurs while fetching the thread timestamp, an Exception is raised
    and the error message is logged.

    Note:
    In this context, 'consumer key' is assumed to be a unique identifier for the channel.
    """

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
    """
    Sends a message to a specific thread in a given Slack channel, optionally with blocks.

    This function uses the 'chat.postMessage' method from the Slack client to post a message
    to a specific thread in a given channel. The specific thread is identified by a message
    that matches the 'posted_text'. If the 'blocks' parameter is provided, it is included in
    the message as structured elements.

    Parameters:
    text (str): The text of the message to be sent.
    channel (str): The ID of the channel where the thread is located.
    posted_text (str): The text of the message that identifies the thread.
    c_id (str): The consumer key of the channel.
    blocks (list, optional): A list of block structures to include in the message. Defaults to None.

    Returns:
    Same function: If an error occurs while posting the message, the function recursively
    calls itself to try posting the message again.

    Raises:
    SlackApiError: If an error occurs while posting the message, a SlackApiError is raised
    and the error message is logged.

    Note:
    In this context, 'consumer key' is assumed to be a unique identifier for the channel.
    """

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
    """
    Uploads a file to a specific thread in a specified Slack channel.

    This function uses the 'files.upload' method from the Slack client to upload a file
    to a particular thread in a given channel. The particular thread is identified by a
    message that matches the 'posted_text'.

    Parameters:
    file_name (str): The name of the file to be uploaded.
    file_path (str): The local path of the file to be uploaded.
    file_type (str): The type of the file being uploaded.
    channel (str): The ID of the channel where the thread is located.
    c_id (str): The consumer key of the channel.
    posted_text (str): The text of the message that identifies the thread.

    Returns:
    Same function: If an error occurs while uploading the file, the function recursively
    calls itself to try uploading the file again.

    Raises:
    SlackApiError: If an error occurs while uploading the file, a SlackApiError is raised
    and the error message is logged.

    Note:
    In this context, 'consumer key' is assumed to be a unique identifier for the channel.
    Also, to upload files, the `files:write` scope must be enabled.
    """

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
    """
    Fetches the replies to a message in a specific thread in a given Slack channel.

    This function uses the 'conversations.replies' method from the Slack client to retrieve
    the replies to a particular message in a thread in a given channel. The specific message
    is identified by its thread timestamp.

    Parameters:
    channel (str): The ID of the channel where the thread is located.
    thread_ts (str): The thread timestamp of the message whose replies are to be retrieved.

    Returns:
    result: The result of the API call, which contains the replies to the message in the thread.
            If an error occurs while fetching the replies, the function recursively
            calls itself to try fetching the replies again.

    Raises:
    SlackApiError: If an error occurs while fetching the replies, a SlackApiError is raised
                   and the error message is logged.
    """

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
    """
    Removes messages sent by a specific bot from a given thread in a Slack channel.

    This function retrieves the messages in a given thread, identified by 'posted_text',
    in a specific channel indicated by 'c_id'. If a message is from a specified bot
    (given by the environment variable 'SLACK_BOT') and does not contain the original
    posted text (not the start of the thread), it is removed from the thread.

    Parameters:
    c_id (str): The consumer key of the channel.
    posted_text (str): The text of the message that identifies the thread.

    Returns:
    Same function: If an error occurs while retrieving the messages or removing the
    messages, the function recursively calls itself to try the operation again.

    Raises:
    SlackApiError: If an error occurs while retrieving the messages or removing the
    messages, a SlackApiError is raised, the error message is logged, and the error
    message is printed.

    Note:
    In this context, 'consumer key' is assumed to be a unique identifier for the channel.
    """

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
