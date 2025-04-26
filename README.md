# SkillDiary 📝

SkillDiary is a simple application designed to help you track your skills and learning progress through a convenient Telegram bot interface. Think of it as a personal diary for your abilities!

This is currently a basic version, focusing on core functionality. Future updates will introduce more advanced analytical tools to provide deeper insights into your skillset development. 🚀

## Why Telegram? 💬

Using Telegram makes logging your activities incredibly easy. Whether at the end of the day or right after completing a task, you can quickly send a message to the bot. It's always accessible through a simple chat interface.

## Architecture 🏗️

The Telegram bot currently runs as a separate process. This design choice anticipates the future addition of other processes and potentially different user interfaces (like a web app) that will interact with the same core skill database.

## Practice Project 🌱

This project was created as a learning exercise and a way to practice various technologies, including Python, Telegram bots, database management with Tortoise ORM, and interaction with Large Language Models (LLMs).

## Setup ⚙️

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lukaszkli/SkillDiary.git
    cd SkillDiary
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up the database:** Ensure you have a PostgreSQL server running.
5.  **Create a `.env` file:** In the root directory of the project, create a file named `.env` and add the following variables, replacing the placeholder values with your actual credentials and IDs:

    ```dotenv
    # .env file contents

    # Your unique Telegram User ID (you can get this from bots like @userinfobot)
    allowed_user_id=YOUR_TELEGRAM_USER_ID

    # Your Telegram Bot Token (get this from BotFather on Telegram)
    telegram_token=YOUR_TELEGRAM_BOT_TOKEN

    # PostgreSQL Database Credentials
    db_login=YOUR_DB_USER
    db_password=YOUR_DB_PASSWORD
    db_host=localhost # Or your DB host
    db_port=PORT      # Or your DB port
    db_name=YOUR_DB_NAME

    # Google Gemini API Key (for skill analysis and summaries)
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    ```

6.  **Run the application:**
    ```bash
    python run.py
    ```
    This will initialize the database (if needed) and start the Telegram bot process.

## Usage 🧑‍💻

1.  Start a chat with your bot on Telegram.
2.  Send the `/start` command.
3.  Simply send messages describing what you learned or practiced (e.g., "Spent 2 hours learning advanced SQL joins", "Practiced knitting a new stitch", "Fixed a bug in the authentication module").
4.  Use `/skillset` to see a detailed breakdown of your recorded skills and points.
5.  Use `/skillset_summary` to get an AI-generated summary of your strengths.

Enjoy tracking your skills!