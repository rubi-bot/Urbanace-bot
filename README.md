# UrbanAce Bot - India's Smartest Shopping Assistant

UrbanAce Bot is a sophisticated Telegram shopping assistant built specifically for the Indian market. It helps users discover products through natural language search without relying on external AI services, using only the local product database.

## Features

- 🛍️ Natural language product search
- 🔥 Special offers and deals
- 📂 Category browsing
- 🆕 New arrivals section
- 🏆 Bestsellers showcase
- 💰 Price-based filtering ("handbag under 1000")
- 🎨 Color-specific searches ("red wallet")
- 📷 Rich product cards with images
- 🛒 Direct purchase links
- 💡 Similar product recommendations

## Installation

### Prerequisites

- Python 3.12+
- pip package manager
- A Telegram bot token (get one from [@BotFather](https://t.me/BotFather))

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/urbanace-bot.git
cd urbanace-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your bot token:
```env
BOT_TOKEN=your_telegram_bot_token_here
```

4. Prepare your `products.csv` file with the required columns (see below)

5. Run the bot:
```bash
python bot.py
```

## Required CSV Columns

Your `products.csv` file must contain the following columns:

- `product_id`: Unique identifier for each product
- `product_name`: Name of the product
- `price`: Current selling price
- `original_price`: Original price (for discount calculation)
- `description`: Product description
- `main_category`: Main category of the product
- `sub_category`: Sub-category of the product
- `rating`: Product rating (out of 5)
- `stock`: Available stock quantity
- `badge`: Special badges (e.g., "Best Seller", "New")
- `offers`: Special offers/discounts
- `size_options`: Available sizes (comma-separated)
- `color_options`: Available colors (comma-separated)
- `image_urls`: URL to product image
- `product_url`: Direct link to purchase the product

## Deployment

### Local Development

For local development, follow the installation steps above. The bot will run continuously until stopped with `Ctrl+C`.

### Render Deployment

1. Create a new Web Service on [Render](https://render.com)
2. Connect to your GitHub repository
3. Set the runtime to Python
4. Add the environment variable:
   - Key: `BOT_TOKEN`, Value: Your Telegram bot token
5. Set the build command to: `pip install -r requirements.txt`
6. Set the start command to: `python bot.py`
7. Make sure your `products.csv` file is in the root directory

### Environment Variables

- `BOT_TOKEN`: Your Telegram bot token (required)
- `CSV_PATH`: Path to your products CSV file (default: `products.csv`)
- `MAX_SEARCH_RESULTS`: Maximum number of search results to consider (default: 20)
- `MAX_DISPLAY_RESULTS`: Maximum number of results to display (default: 5)
- `DEBUG`: Enable debug mode (default: false)

## Updating Product Database

To update your product database:

1. Modify your `products.csv` file ensuring all required columns are present
2. Restart the bot service
3. The bot will automatically load the updated data

For large databases, consider implementing incremental updates or scheduled reloads.

## Error Handling

The bot includes comprehensive error handling:

- Invalid image URLs are handled gracefully
- Missing product information is filled with defaults
- Empty search results provide helpful feedback
- System errors are logged for debugging
- CSV validation prevents startup with invalid data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter issues, please check:

1. That your `.env` file contains the correct `BOT_TOKEN`
2. That your `products.csv` file has all required columns
3. That all image URLs and product URLs are valid
4. That your bot has sufficient permissions in groups/channels

For additional support, create an issue in the GitHub repository.
