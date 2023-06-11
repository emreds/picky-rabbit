# Picky Rabbit

LLM Powered Food Content Information Chatbot

![chat_image](./images/chat_image.png)

## What does Picky Rabbit do?

Picky Rabbit is an OpenAI LLM-powered chatbot that provides information about the contents of packaged food products. It helps users make informed choices by offering details on ingredients, nutritional values, allergens, and more.

## How to run locally?

To run Picky Rabbit locally, follow these steps:

1. If you don't have Poetry installed, you can install it from [here](https://python-poetry.org/docs/).

2. After installing Poetry, clone the repository and run the following command to install the dependencies:

`poetry install`

3. Once the dependencies are installed, run the following command to start the project:

`poetry run streamlit run ./picky-rabbit/app.py`

4. The project will start running on `localhost:8501` by default.

That's it! You can now access Picky Rabbit on your local machine.

## Adding a Permanent Key for Local Usage

If you want to add a permanent key for local usage, follow these steps:

1. Create a file named `secrets.toml` under the `.streamlit` folder.

2. Add the following line to `secrets.toml`, replacing `YOUR_KEY` with your actual key:

`openai_key = "YOUR_KEY"`
