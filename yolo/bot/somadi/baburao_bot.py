import os
import json
from datetime import datetime
import logging
import asyncio
from datetime import timedelta
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Poll
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    ApplicationBuilder,
    CallbackContext,
)
from yolo.integrations.crickbuzz import IPLMatchDetailsScraper
from yolo.db.api import create_user
from yolo.db.models import User


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("telegram_bot_token_somadi")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hello! Welcome to the group.")


async def save_group_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save group ID and usernames when the bot is added to a group."""
    group_id = update.effective_chat.id
    members = await context.bot.get_chat_members_count(chat_id=group_id)
    usernames = []

    for member_id in range(members):
        try:
            member_info = await context.bot.get_chat_member(
                chat_id=group_id, user_id=member_id
            )

            # save info from gr. to database

            user_id = member_info.user.id
            usernames.append(member_info.user.username)

            user = User(username=member_info.user.username, join_date="2023-01-01")

        except Exception as e:
            logger.error(f"Failed to get member info: {str(e)}")

    logger.info(f"Group ID: {group_id}, Usernames: {usernames}")


async def get_telegram_group_id(update: Update) -> int:
    """Returns the ID of the Telegram group where the bot is running."""
    return update.effective_chat.id


# return list of match names and short form names yet to start by timestamp
async def get_future_matchs_info():
    """
    Returns a list of match names and short form names yet to start by timestamp
    """
    scraper = IPLMatchDetailsScraper()
    raw_data = await scraper.main()
    now = datetime.now()

    return [
        match
        for match in raw_data
        # ms to datetime
        if datetime.fromtimestamp(match["timestamp_sec"]) >= now
    ]


# create a telegram poll for each match that is yet to start, create a poll and in concecative message provide match metadata
async def ask_user_to_poll_match(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Asks the user to select one match from the upcoming matches, then shows only that selected match's poll and metadata.
    """
    upcoming_matches = await get_future_matchs_info()
    # show in options display datetime as it is in [] along side match name
    options = [
        f"{match['short_names']} - {match['datetime']}" for match in upcoming_matches
    ]
    keyboard = [[option] for option in options]
    #
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Please select a match to vote on:",
        reply_markup=reply_markup,
    )
    return CHOOSING_MATCH


async def show_selected_match_poll_and_metadata(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Attempting to send a poll for the selected match.")
    # remove timestamp from update.message.text
    selected_match_text = update.message.text.split(" -")[0]
    upcoming_matches = await get_future_matchs_info()
    for match in upcoming_matches:
        if match["short_names"] == selected_match_text:
            question = f"Who will win? {match['short_names']}"
            options = [match["team1"], match["team2"]]
            # Send poll
            await context.bot.send_poll(
                chat_id=update.effective_chat.id,
                question=question,
                options=options,
                is_anonymous=False,
                allows_multiple_answers=False,
            )
            await asyncio.sleep(3)
            # Combine match summary with metadata and format it properly to highlight in the telegram message
            match_summary_and_metadata = f"""
                **Match # {match['match_number']}: {match['team1']} vs {match['team2']}**
                _Location_: {match['location']}, _Date & Time_: {match['datetime']}

                **Match Summary:**
                1. **Pitch Analysis**: The newly inaugurated stadium in Mullanpur favors pace-friendly surfaces, with quicks being more successful than spinners. Chasing has been the preferred choice, indicating a potential advantage for the team batting second.
                2. **Injuries and Player Availability**: Updates on the match-fitness of key players like Nandre Burger and Sandeep Sharma from the Rajasthan Royals' medical team are awaited. Liam Livingstone's potential return for Punjab Kings could bolster their batting lineup.
                3. **Team Form**: Rajasthan Royals are currently the table-toppers, but their last-ball defeat to GT indicates a possible dip in form. On the other hand, Punjab Kings, placed eighth, are more desperate for a win to resuscitate their campaign after losing three of their first five games.
                4. **Player Form**: While Rajasthan Royals' middle-order has been rescued by Sanju Samson and Riyan Parag's consistent performances, Punjab Kings' top order, including Shikhar Dhawan and Jonny Bairstow, needs to step up, especially after minimal returns in recent matches.
                5. **Weather Conditions**: No information is provided regarding weather conditions, which could play a crucial role, particularly if there are factors like rain or dew affecting the pitch and outfield.
                6. **Odds of Winning**: Rajasthan Royals have historically had the upper hand over Punjab Kings, winning five of the seven games since IPL 2020. However, current form and conditions could significantly impact the outcome of this match.
                7. **Impact Players**: Yuzvendra Chahal's potential inclusion in Rajasthan Royals' lineup and Liam Livingstone's return for Punjab Kings could influence the game with their bowling and batting prowess, respectively.
                8. **Tactical Decisions**: Both teams might make strategic changes to their playing XI based on pitch conditions and player availability, which could shift the balance of the match.
                9. **Key Match-ups**: The battle between Rajasthan Royals' opening bowler Yuzvendra Chahal and Punjab Kings' top-order batsmen, especially Shikhar Dhawan and Jonny Bairstow, could be pivotal, given Chahal's historical success against them.
                10. **Mental Resilience**: With Rajasthan Royals embarking on a long away leg and Punjab Kings seeking to turn their campaign around, mental resilience and the ability to handle pressure situations could be crucial factors in determining the outcome of the match.
            """
            # Send match summary and metadata
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=match_summary_and_metadata,
                parse_mode="Markdown",
            )
            break
        else:
            await update.message.reply_text("Please select a valid match.")
    return ConversationHandler.END


# You need to add CHOOSING_MATCH to your states and update the ConversationHandler accordingly.
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # on non-command i.e message - save group info when bot is added to a group
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, save_group_info)
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("poll_match", ask_user_to_poll_match),
        ],
        states={
            CHOOSING_MATCH: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    show_selected_match_poll_and_metadata,
                )
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    main()
    # print(get_future_matchs_info())
