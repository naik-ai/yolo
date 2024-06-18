# Telegram Chatbot

## Chatar Patar
[<u>Deploy intial functionality</u>](https://linear.app/jovita/issue/JOV-21/telgram-bot-deployment-to-gcp)

## Scope: Functionality/Commands 

**What output to see when raising this commands**

- [ ] `/today`

    ```mermaid
    
    sequenceDiagram
        
        participant User
        participant Command
        participant Bot
        participant DB

        User->>Command: selected: /start
        Bot-->>User: Greeting1
        Bot-->>User: Ask for user's name
        User->>Bot: User's name
        Bot->>DB: Save user name
        DB-->>Bot: Confirmation
        Bot-->>User: Responed Thank you
        Bot-->>User: Message1: Show all commands + info on it
    ```

    Footnote:
    - 
    - Message1: Show all commands the user can use along with some basic info of current date.


- [ ] `/show_ipl_schedule`
- [ ] `/show_leatherboard`
- [ ] `/show_current_match_stats`
- [ ] `/create_next_match_poll`
- [ ] `/poll_results`
- [ ] `/game_pitch_analysis`

### Non-Command Functionality

- When a new User joins the telegram group- Save the data to postgres database under user table.
- When a new User joins the telegram group- Send a welcome message to the user.

