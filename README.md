# Telegram RSS Feed Bot

This is a Telegram bot that fetches news articles from an RSS feed and posts them to a Telegram channel. It uses the Telegraph API to create a simplified version of the news articles and sends the links to the channel.

## Prerequisites

Before running the code, make sure you have the following prerequisites:

- Python 3.x installed
- Required Python packages installed (you can install them using `pip`):
  - feedparser
  - telegram
  - telegraph
  - requests
  - beautifulsoup4
  - googletrans

## Getting Started

1. Clone the repository or download the source code.
2. Install the required Python packages (mentioned in the prerequisites section).
3. Replace the placeholders in the code with your own tokens and channel ID:
   - `TOKEN`: Your Telegram bot token.
   - `CHANNEL_ID`: The ID of your Telegram channel where you want to post the news articles.
   - `RSS_FEED_URL`: The URL of the RSS feed you want to fetch news articles from.
   - `telegraph_api_token`: Your Telegraph API token.
4. Save the modified code.
5. Open a terminal or command prompt and navigate to the directory where the code is saved.
6. Run the code using the command: `python your_code_file.py`.
7. The bot will start running and fetching news articles from the RSS feed, and posting them to the specified Telegram channel.

## Bot Commands

The bot supports the following commands:

- `/start`: Start the bot and receive a greeting message.
- `/graph <link>`: Fetches the content of the specified webpage and creates a simplified version using Telegraph API. The bot will reply with a link to the simplified version.

## Customization

You can customize the bot by modifying the code to fit your specific requirements. For example, you can change the command handlers, add more functionality, or modify the content formatting.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegraph API](https://telegra.ph/api)
- [Feedparser](https://pypi.org/project/feedparser/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Googletrans](https://pypi.org/project/googletrans/)
