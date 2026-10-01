import telebot
import requests

# Replace with your actual tokens
BOT_TOKEN = "8952860968:AAEyrTuOSuQ9xLqC_4EYuVvlsc7rk34ASc8"
OMDB_API_KEY = "c49feb8b"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! To search for a movie, type /movie followed by the title.\nExample: /movie Avatar")

@bot.message_handler(commands=['movie'])
def search_movie(message):
    movie_title = message.text.replace('/movie', '').strip()
    
    if not movie_title:
        bot.reply_to(message, "Please provide a movie title! Example: /movie Interstellar")
        return

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        title = response.get("Title")
        year = response.get("Year")
        rating = response.get("imdbRating")
        plot = response.get("Plot")

        reply = f"🎬 *{title}* ({year})\n⭐ *IMDb Rating:* {rating}/10\n\n📝 *Plot:* {plot}"
        bot.reply_to(message, reply, parse_mode="Markdown")
    else:
        bot.reply_to(message, "Movie not found. Please check the spelling and try again.")

print("Bot is running...")
bot.infinity_polling()
