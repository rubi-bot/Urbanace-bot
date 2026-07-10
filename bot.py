import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from search_engine import SearchEngine
from config import BOT_TOKEN
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class UrbanAceBot:
    def __init__(self):
        self.search_engine = SearchEngine()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = (
            "🛍️ Welcome to UrbanAce - India's Smartest Shopping Assistant!\n\n"
            "I can help you find the perfect products with:\n"
            "• Smart search in thousands of products\n"
            "• Latest offers and deals\n"
            "• Category browsing\n"
            "• Bestsellers and new arrivals\n\n"
            "Try searching for:\n"
            "- 'handbags under 1000'\n"
            "- 'red wallet'\n"
            "- 'office bags'\n"
            "- 'gift for wife'\n\n"
            "Use /help for more commands!"
        )
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "📚 Available Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/offers - View all special offers\n"
            "/categories - Browse products by category\n"
            "/new - View new arrivals\n"
            "/bestsellers - View best selling products\n\n"
            "🔍 Search Tips:\n"
            "- Type any product name or description\n"
            "- Add price limits like 'bag under 500'\n"
            "- Specify colors like 'red shoes'\n"
            "- Look for specific features like 'waterproof jacket'\n"
        )
        await update.message.reply_text(help_text)

    async def offers(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /offers command"""
        try:
            products = self.search_engine.get_products_with_offers()
            if not products.empty:
                await self.send_product_list(update, products.head(5), "🔥 Products with Offers")
            else:
                await update.message.reply_text("No products with offers available at the moment.")
        except Exception as e:
            logger.error(f"Error in offers command: {e}")
            await update.message.reply_text("Error retrieving products with offers.")

    async def categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /categories command"""
        try:
            categories = self.search_engine.get_main_categories()
            if categories:
                keyboard = []
                for cat in categories:
                    keyboard.append([InlineKeyboardButton(cat, callback_data=f"cat_{cat}")])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text("Select a category:", reply_markup=reply_markup)
            else:
                await update.message.reply_text("No categories available at the moment.")
        except Exception as e:
            logger.error(f"Error in categories command: {e}")
            await update.message.reply_text("Error retrieving categories.")

    async def new_arrivals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /new command"""
        try:
            products = self.search_engine.get_new_arrivals()
            if not products.empty:
                await self.send_product_list(update, products.head(8), "🆕 New Arrivals")
            else:
                await update.message.reply_text("No new arrivals available at the moment.")
        except Exception as e:
            logger.error(f"Error in new command: {e}")
            await update.message.reply_text("Error retrieving new arrivals.")

    async def bestsellers(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bestsellers command"""
        try:
            products = self.search_engine.get_bestsellers()
            if not products.empty:
                await self.send_product_list(update, products.head(8), "🏆 Bestsellers")
            else:
                await update.message.reply_text("No bestsellers available at the moment.")
        except Exception as e:
            logger.error(f"Error in bestsellers command: {e}")
            await update.message.reply_text("Error retrieving bestsellers.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages (product search)"""
        query = update.message.text.strip()
        if not query:
            return
        
        try:
            # Search for products based on user query
            results = self.search_engine.search(query)
            
            if results.empty:
                await update.message.reply_text("❌ No products found matching your search. Try different keywords!")
                return
            
            # Send top 5 results
            await self.send_product_list(update, results.head(5), f"🔍 Results for '{query}'")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text("An error occurred while processing your request. Please try again.")

    async def send_product_list(self, update: Update, products_df, title: str):
        """Send a list of products as messages"""
        if products_df.empty:
            await update.message.reply_text("No products found.")
            return
        
        await update.message.reply_text(title)
        
        for index, row in products_df.iterrows():
            await self.send_single_product(update, row)
    
    async def send_single_product(self, update: Update, product_row):
        """Send a single product as a formatted message with image and buttons"""
        try:
            # Prepare product information
            product_name = product_row['product_name'] or "N/A"
            price = product_row['price']
            original_price = product_row['original_price']
            rating = product_row['rating']
            stock = product_row['stock']
            offer = product_row['offers']
            description = product_row['description'] or "No description available"
            image_url = product_row['image_urls'] if product_row['image_urls'] else None
            product_url = product_row['product_url']
            
            # Format prices
            if price:
                price_str = f"₹{int(price):,}"
            else:
                price_str = "Price not available"
            
            original_price_str = f"₹{int(original_price):,}" if original_price and original_price != price else ""
            
            # Format rating
            rating_str = f"⭐ {rating}/5" if rating else "⭐ N/A"
            
            # Format stock status
            stock_str = f"📦 {stock} in stock" if stock and stock > 0 else "📦 Out of stock"
            
            # Format offer
            offer_str = f"🎁 {offer}" if offer else ""
            
            # Create product details message
            product_details = f"🛍️ *{product_name}*\n\n"
            
            if original_price_str:
                product_details += f"*Price:* ~~{original_price_str}~~ **{price_str}**\n"
            else:
                product_details += f"*Price:* **{price_str}**\n"
            
            product_details += f"*Rating:* {rating_str}\n"
            product_details += f"*Stock:* {stock_str}\n"
            
            if offer_str:
                product_details += f"*Offer:* {offer_str}\n\n"
            else:
                product_details += "\n"
            
            product_details += f"*Description:* {description}"
            
            # Create inline keyboard with buy now button
            keyboard = [[InlineKeyboardButton("🛒 Buy Now", url=product_url)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send message with image if available
            if image_url:
                try:
                    await update.message.reply_photo(
                        photo=image_url,
                        caption=product_details,
                        parse_mode='Markdown',
                        reply_markup=reply_markup
                    )
                except:
                    # If image fails, send text version
                    await update.message.reply_text(
                        product_details,
                        parse_mode='Markdown',
                        reply_markup=reply_markup
                    )
            else:
                await update.message.reply_text(
                    product_details,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            
            # Get and send similar products
            try:
                similar_products = self.search_engine.get_similar_products(product_row['product_id'])
                if not similar_products.empty:
                    await update.message.reply_text("You may also like:")
                    for idx, sim_row in similar_products.head(3).iterrows():
                        await self.send_single_product(update, sim_row)
            except Exception as e:
                logger.error(f"Error getting similar products: {e}")
                
        except Exception as e:
            logger.error(f"Error sending product: {e}")
            await update.message.reply_text("An error occurred while displaying the product.")

def main():
    """Run the bot"""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Create bot instance
    bot_instance = UrbanAceBot()

    # Register command handlers
    application.add_handler(CommandHandler("start", bot_instance.start))
    application.add_handler(CommandHandler("help", bot_instance.help_command))
    application.add_handler(CommandHandler("offers", bot_instance.offers))
    application.add_handler(CommandHandler("categories", bot_instance.categories))
    application.add_handler(CommandHandler("new", bot_instance.new_arrivals))
    application.add_handler(CommandHandler("bestsellers", bot_instance.bestsellers))

    # Register message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_instance.handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
