
# Python FastAPI Project

A project that starts a FastAPI server to run various functions and handle specific events.

![promote](https://github.com/user-attachments/assets/84f21cab-4cd0-4597-94fa-7e8fca8f4696)



## Project Description

This project is implemented using FastAPI. It provides a range of functions from handling message events, submissions, to managing action clicks and more. This project will automatically detect the local IP address of the host machine and start the server on this IP.

## Main Features

- `handle_message_events`: This function handles incoming message events
- `action_button_click`: A function to handle clicks on action buttons
- `handle_submission`: A function to handle submissions
- `handle_some_action`: A function designed to handle a specific action
- `publish_home_view`: A function that publishes a view in the home tab
- `endpoint`: A generic endpoint function
- `get_status`: A function to retrieve the current status 
- `root`: This function manages the root endpoint and returns a greeting message
- `get_ip_address`: Use this function to get the local IP address of the host machine

## Getting Started

### Dependencies

You will need Python version 3.12.3 installed on your machine. You'll also be using the FastAPI, Uvicorn, and Socket libraries. All of these can be installed via pip.

### Running The App

Simply run the main script file provided in the repository. This will kickstart the Uvicorn server at the local machine's IP address on port 3200. Logs will be recorded at the "info" level and with the reload option set to "True", the server will restart whenever you save changes to your code.

### Using The App

Once the server is up and running, you can send HTTP requests to the designed endpoints from any HTTP client.

## Support

If any issues arise or you have any questions, feedback, or requests, please open an issue on the repository.
