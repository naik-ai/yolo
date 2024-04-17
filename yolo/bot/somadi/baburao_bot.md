# Telegram Chatbot

## Chatar Patar
[<u>Deploy intial functionality</u>](https://linear.app/jovita/issue/JOV-21/telgram-bot-deployment-to-gcp)

## Scope: Functionality/Commands 

**What output to see when raising this commands**

- `/start`

    ```mermaid
    
    sequenceDiagram
        participant User
        participant Bot
        participant DB
        User->>Bot: /start
        Bot->>DB: Fetch user details
        DB-->>Bot: User details
        Bot->>User: Hi!
    
    end
    ```


- `/show_ipl_schedule`
- `/show_leatherboard`
- `/show_current_match_stats`
- `/create_next_match_poll`
- `/poll_results`
- `/game_pitch_analysis`

### Non-Command Functionality