#  Copyright (c) Ioannis E. Kommas 2024. All Rights Reserved

from dev_slack import slack_todo


def remove_data_from_specific_channel(id, lenght=0):
    """
        Function to remove all Api (BoT) data from a specific Slack channel.

        Parameters:
        id (int): Identifier for the Slack channel.
        length (int, optional): Specifies the amount of data to remove. Default is 0 (removes no data).

        Returns:
        None
        """
    slack_todo.remove(id, lenght)


# remove_data_from_specific_channel(1)
