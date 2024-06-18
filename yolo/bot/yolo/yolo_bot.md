# YOLO Telegram Bot

## Scope: Functionality/Commands

**What output to see when raising this commands**

- `/start`

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
        Bot->>DB: Save user **name**
        DB-->>Bot: Confirmation
        Bot-->>User: Responed Thank you
        Bot-->>User: Message1: Show all commands + info on it
    ```

    Footnote:
    - Greeting1: Hello, This is YOLO Telegram Bot, specialized in Financial analysis of Listed companies- related to Travel. 
    - Message1: Show all commands te\he user can use along with some basic info of what to expect. Select a Sector to proceed

- `select_category`: `Which category would you like to analyze?`

    - Provide overview of the selected category
    - List most important KPIs
    - List most important Companies and cross compare between them
    - show option to `select_ticker` OR `compare_ticker` to dive deep
    - Flow:
    

        ```mermaid
        sequenceDiagram
            
            participant Command
            participant Bot
            participant User
            participant Message
            participant DB
            

            User->>Command: selected: /select_category
            Bot->>DB: Query for category list
            DB-->>Bot: Provide list of categories
            Bot-->>User: Show In-line Keyboard Options: single Input option
            User->>Bot: Selected Category
            Bot->>DB: Query for category
            DB-->>Bot: Provide General info and related commands to dive deeper
            Bot-->>User: Message1: Show all commands realted to category + more_info
            User->>Command: selected: /more_info
            User->>Message: Custom Questions
        ```
        - Notes:
            - Message1: 
                - Show all commands realted to category:
                [`select_ticker`, `compare_ticker`, `conversation`, `email_current_report`, `generate_knowledge_graph_for_current_session`, `sector_news`, `market_sentiments`]
            - more_info: speficy pre-defined question that can be picked
                - ask general question that go directly to LLM can also be used

- `select_ticker`: 
    - OUTPUT: `List all Tickers avaiable`
    - providing overview
    - provide KPIs and cross compare between them
    - Flow:
        ```mermaid
        sequenceDiagram
            
            participant Command
            participant Bot
            participant User
            participant Message
            participant DB
            

            User->>Command: selected: `/select_category`
            Bot->>DB: Query for category list
            DB-->>Bot: Provide list of categories
            Bot-->>User: Show In-line Keyboard Options: single Input option
            User->>Bot: Selected Category
            Bot->>DB: Query for category
            DB-->>Bot: Provide General info and related commands to dive deeper
            Bot-->>User: Message1: Show all commands realted to category + more_info
            User->>Command: selected: /more_info
            User->>Message: Custom Questions
        ```

- `compare_ticker`:
    - Compare 2 tickers
    - provide KPIs and cross compare between them
- `conversation`:
- `more_info` -> dive deeep into a specific category/previsuly selected command: 
    - Provide more info on the selected category
    - List most important KPIs
    - List most important Companies and cross compare between them
    - show option to `select_ticker` OR `compare_ticker` to dive deep
- `email_current_report`: `Would you like to receive the analysis via email or download a report?`
    - capture email in send me report and analysis
        ```mermaid
        sequenceDiagram
        Bot->>User: Ask for user's email
        User->>Bot: User's email
        Bot->>DB: Save user email
        DB-->>Bot: Confirmation
        Bot->>User: Responed Thank you
        ```
- `generate_knowledge_graph_for_current_session`: 
    - Generate a Knowledge Graph for the current session
    - Send the Knowledge Graph to the user via download

- `sector_news`: 
    - Provide latest news on the selected sector
- `market_sentiments`: 
    - Provide latest news on the selected sector


### Technical Implementation Flow
- UI: Telegram Bot
- Database: Postgres- GCP instance
- LangChain: Use for Vector Embedding and RAG Application building
- Evidence: Reporting and Analysis


### Bot User Journey
```mermaid

timeline
        title YOLO Telegram Bot User Journey Timeline
        section Interaction `/start`
            2023-01-01 00:00 : User sends `/start`
            2023-01-01 00:01 : Bot asks for user's name
            2023-01-01 00:02 : User provides name
            2023-01-01 00:03 : Bot saves name and thanks user
        
        section Category Selection
            2023-01-01 00:04 : User selects category
            2023-01-01 00:05 : Bot provides category overview and KPIs
        section Ticker Interaction
            2023-01-01 00:06 : User selects ticker
            2023-01-01 00:07 : Bot provides ticker overview and KPIs
        section Comparison and Reports
            2023-01-01 00:08 : User requests comparison
            2023-01-01 00:09 : Bot provides comparison results
            2023-01-01 00:10 : User requests email report
            2023-01-01 00:11 : Bot asks for and saves user's email
            2023-01-01 00:12 : Bot sends report and thanks user
        section Knowledge Graph
            2023-01-01 00:13 : User requests knowledge graph
            2023-01-01 00:14 : Bot generates and sends knowledge graph

```

### Non-Command Functionality