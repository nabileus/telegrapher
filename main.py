import feedparser
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import time
import telegraph
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from telegram.utils.request import Request
from telegram import ParseMode


# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
# Channel ID (e.g., @your_channel)
CHANNEL_ID = 'YOUR_CHANNEL_ID'
# RSS feed URL
RSS_FEED_URL = 'https://prod-qt-images.s3.amazonaws.com/production/prothomalo-bangla/feed.xml'

telegraph_api_token = 'YOUR_TELEGRAPH_API_TOKEN'

# Initialize the Telegraph API
telegraph_api = telegraph.Telegraph(telegraph_api_token)

def translate_bengali_to_english(text):
    translator = Translator(service_urls=['translate.google.com'])

    # Translate the text to English
    translation = translator.translate(text, src='bn', dest='en')

    return translation.text

def send_news_to_channel(bot):
    feed = feedparser.parse(RSS_FEED_URL)
    entries = feed.entries
    last_entry_id = entries[5].id

    while True:

        print(f'laste_entry_id:{last_entry_id}')

        feed = feedparser.parse(RSS_FEED_URL)
        entries = feed.entries

        # Get the ID of the latest entry
        latest_entry_id = entries[0].id
        print(f'latest_entry_id:{latest_entry_id}')

        for i in range(100):
            ongoing_entry_id = entries[i].id
            print(f'ongoi_entry_id:{ongoing_entry_id}')

            if last_entry_id == ongoing_entry_id:
                last_entry_id = latest_entry_id
                break
            else:
                # New entry found, send it to the channel

                news_title = entries[i].title
                news_link = entries[i].link

                webpage_url = news_link

                # Retrieve the webpage HTML
                response = requests.get(webpage_url)
                webpage_html = response.text

                # Create a BeautifulSoup object for parsing the HTML
                soup = BeautifulSoup(webpage_html, 'html.parser')

                # Retrieve the webpage title
                webpage_title = soup.title.text if soup.title else 'শিরোনাম খুঁজে পাওয়া যায়নি'

                # Retrieve the webpage content
                webpage_content = '\n'.join([p.text for p in soup.find_all('p')])

                # Retrieve the image link from meta tag
                image_link = None
                meta_tags = soup.find_all('meta', {'name': 'twitter:image'})
                if meta_tags:
                    image_link = meta_tags[0].get('content')

                # Prepare the content in the required format
                # {'tag': 'h4', 'children': [webpage_title]}
                content = []

                # Add the image to the content if available
                if image_link:
                    content.append({'tag': 'figure', 'children': [
                        {'tag': 'img', 'attrs': {'src': image_link}},
                        {'tag': 'figcaption', 'children': [webpage_title]}
                    ]})

                content.append({'tag': 'p', 'children': [webpage_content]})
                content.append({'tag': 'p', 'children': [{'tag': 'a', 'attrs': {'href': f'{webpage_url}'}, 'children': [f'Reference:\n{webpage_url}']}]})

                english_translation = translate_bengali_to_english(webpage_title)


                # Create a new Telegraph page
                try:
                    page = telegraph_api.create_page(title=english_translation, content=content)
                    telegraph_url = 'https://telegra.ph/{}'.format(page['path'])
                except telegraph.exceptions.TelegraphException as error:
                    raise telegraph.exceptions.TelegraphException(error)


                # Compose the message
                message = f'<a href="{telegraph_url}">{news_title}</a>'

                # Send the message to the channel
                bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode = ParseMode.HTML)

        # Delay between each iteration (e.g., 1 minute)
        time.sleep(15)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your Telegram bot. How can I assist you?")
    print('Someone started your bot :3')

def graph(update, context):
    message = update.message.text
    link = message.split(' ')[1]  # Extract the link from the message
    webpage_url = link

    # Retrieve the webpage HTML
    response = requests.get(webpage_url)
    webpage_html = response.text

    # Create a BeautifulSoup object for parsing the HTML
    soup = BeautifulSoup(webpage_html, 'html.parser')

    # Retrieve the webpage title
    webpage_title = soup.title.text if soup.title else 'শিরোনাম খুঁজে পাওয়া যায়নি'

    # Retrieve the webpage content
    webpage_content = '\n'.join([p.text for p in soup.find_all('p')])

    # Retrieve the image link from meta tag
    image_link = None
    meta_tags = soup.find_all('meta', {'name': 'twitter:image'})
    if meta_tags:
        image_link = meta_tags[0].get('content')

    # Prepare the content in the required format
    # {'tag': 'h4', 'children': [webpage_title]}
    content = []

    # Add the image to the content if available
    if image_link:
        content.append({'tag': 'figure', 'children': [
            {'tag': 'img', 'attrs': {'src': image_link}},
            {'tag': 'figcaption', 'children': [webpage_title]}
        ]})

    content.append({'tag': 'p', 'children': [webpage_content]})
    content.append({'tag': 'p', 'children': [{'tag': 'a', 'attrs': {'href': f'{webpage_url}'}, 'children': [f'Reference:\n{webpage_url}']}]})

    english_translation = translate_bengali_to_english(webpage_title)


    # Create a new Telegraph page
    try:
        page = telegraph_api.create_page(title=english_translation, content=content)
        telegraph_url = 'https://telegra.ph/{}'.format(page['path'])
    except telegraph.exceptions.TelegraphException as error:
        raise telegraph.exceptions.TelegraphException(error)


    user = update.message.from_user

    # Compose the message
    message = f'<a href="{telegraph_url}">{webpage_title}</a>'
    # Create the personalized link with username and first name
    personalized_link = f"{user.first_name} - @{user.username}\n"+f'<a href="{telegraph_url}">{webpage_title}</a>'


    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode = ParseMode.HTML)
    CHANNEL_ID= 'YOUR_LOG_CHANNEL_ID'
    context.bot.send_message(chat_id=CHANNEL_ID, text=personalized_link, parse_mode = ParseMode.HTML)



def main():
    request = Request(con_pool_size=8)
    bot = Bot(token=TOKEN, request=request)

    # Create an instance of the Updater class
    updater = Updater(bot=bot, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the command handlers
    start_handler = CommandHandler('start', start)
    graph_handler = CommandHandler('graph', graph)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(graph_handler)

    # Start the bot
    updater.start_polling()

    # Start sending news to the channel
    send_news_to_channel(bot)

if __name__ == '__main__':
    main()
