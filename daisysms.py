import requests
import telebot
import config  # Import the config.py file

# Initialize Telegram Bot
bot = telebot.TeleBot(config.TELEGRAM_API_TOKEN)

# Function to request a temporary number from DaisySMS for a specific service
def request_temporary_number(service_name):
    url = f"https://daisysms.com/api/v1/number?service={service_name}"
    headers = {
        "Authorization": "Bearer " + config.DAISYSMS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('number')
    else:
        return None

# Function to get DaisySMS service list and prices
def get_service_list_and_prices():
    url = "https://daisysms.com/api/v1/services"
    headers = {
        "Authorization": "Bearer " + config.DAISYSMS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        services = data.get('services')
        return services
    else:
        return None

# Handler for the /get_number command
@bot.message_handler(commands=['get_number'])
def get_temporary_number(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in config.AUTHORIZED_USER_IDS:
        command_parts = message.text.split(' ')
        if len(command_parts) == 2:
            service_name = command_parts[1]
            temporary_number = request_temporary_number(service_name)
            if temporary_number:
                bot.send_message(chat_id, f"Your temporary number for {service_name} is: {temporary_number}")
            else:
                bot.send_message(chat_id, f"Failed to retrieve a temporary number for {service_name}. Please try again later.")
        else:
            bot.send_message(chat_id, "Please use the command in the format /number {service_name}.")
    else:
        bot.send_message(chat_id, "You are not authorized to use this command.")

# Handler for the /servicelist command
@bot.message_handler(commands=['servicelist'])
def get_services_list(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in config.AUTHORIZED_USER_IDS:
        services = get_service_list_and_prices()
        if services:
            response_message = "DaisySMS Services and Prices:\n"
            for service in services:
                response_message += f"- {service['name']}: ${service['price']}\n"
            bot.send_message(chat_id, response_message)
        else:
            bot.send_message(chat_id, "Failed to retrieve service list. Please try again later.")
    else:
        bot.send_message(chat_id, "You are not authorized to use this command.")

# Start the bot
bot.polling()
