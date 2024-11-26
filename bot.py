import random
import time
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Initialize logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for game state
game_active = False
current_multiplier = 1.0
crash_point = 0.0
players = {}
house_fee = 0.05  # 5% house fee

# Game state management: reset after each round
def reset_game():
    global game_active, current_multiplier, crash_point, players
    game_active = False
    current_multiplier = 1.0
    crash_point = random.uniform(1.1, 10.0)  # Random crash point between 1.1x and 10x
    players = {}

# Command: /start
def start(update: Update, context: CallbackContext):
    welcome_message = (
        "Welcome to the Crash Game! Here's how to play:\n"
        "/bet <amount> - Place a bet\n"
        "/cashout - Cash out during the round\n"
        "/startgame - Start a new game round (only if at least one bet is placed)\n"
        "/leaderboard - View the leaderboard of top players"
    )
    update.message.reply_text(welcome_message)

# Command: /bet
def bet(update: Update, context: CallbackContext):
    global game_active

    if game_active:
        update.message.reply_text("Test bet placed! You can now try /cashout.")
    else:
        update.message.reply_text("The game is not active. Please wait for the next round.")

# Command: /cashout
def cashout(update: Update, context: CallbackContext):
    global game_active

    if game_active:
        # Simulate a cashout
        player_name = update.message.from_user.first_name
        if player_name in players:
            winnings = players[player_name] * current_multiplier * (1 - house_fee)
            update.message.reply_text(f"Cashout successful! You earned {winnings} virtual coins.")
            del players[player_name]  # Remove player after cashout
        else:
            update.message.reply_text("You haven't placed a bet yet!")
    else:
        update.message.reply_text("The game is not active.")

# Command: /startgame
def start_game(update: Update, context: CallbackContext):
    global game_active

    if len(players) == 0:
        update.message.reply_text("At least one player needs to place a bet before starting the game.")
    else:
        game_active = True
        update.message.reply_text("Game has started! Place your bets using /bet <amount> or use /cashout.")
        # Optionally start the game logic here, such as the multiplier increasing
        run_game()

# Command: /leaderboard
def leaderboard(update: Update, context: CallbackContext):
    if players:
        leaderboard = "\n".join([f"{name}: {bet}" for name, bet in players.items()])
        update.message.reply_text(f"Leaderboard:\n{leaderboard}")
    else:
        update.message.reply_text("No bets placed yet!")

# Helper function to simulate the multiplier increasing
def run_game():
    global current_multiplier, crash_point
    while game_active and current_multiplier < crash_point:
        time.sleep(1)
        current_multiplier += random.uniform(0.1, 0.5)  # Increase multiplier randomly
        # If you want to show this in the bot, you can send a message periodically
        # update.message.reply_text(f"Current multiplier: {current_multiplier:.2f}x")
    
    # Simulate crash and stop the game
    if game_active:
        game_active = False
        crash_message = f"The game has crashed at {current_multiplier:.2f}x! Players who didn't cash out lose their bets."
        # Handle players who didn't cash out
        for player, bet in players.items():
            if bet * current_multiplier <= 0:
                continue  # Players who cashed out already are excluded
            update.message.reply_text(f"{player} lost their bet.")
        reset_game()

# Command to manually reset the game
def reset(update: Update, context: CallbackContext):
    reset_game()
    update.message.reply_text("The game has been reset.")

def main():
    # Set up the Updater and Dispatcher
    updater = Updater("7589441909:AAF-G5l8I6SZyD-4_whRN6W3pBsXcQLMpnk", use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bet", bet))
    dispatcher.add_handler(CommandHandler("cashout", cashout))
    dispatcher.add_handler(CommandHandler("startgame", start_game))
    dispatcher.add_handler(CommandHandler("leaderboard", leaderboard))
    dispatcher.add_handler(CommandHandler("reset", reset))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
