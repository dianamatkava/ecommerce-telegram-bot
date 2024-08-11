# VPGifts

A Telegram Ecommerce bot for listing and purchasing gifts, uncludes translation feature and cart, leveraging various technologies:

- **Scraping Cron Job**: Automates data extraction with Beautifulsoup
- **Telegram Ecommerce Bot**: Manages user interactions and gift purchases.
- **Binance Listener**: Monitors cryptocurrency transactions.
- **PostgresDB**: Stores user and transaction data.
- **Django Admin**: Provides a third-party admin interface for management.
- **QR Code Generator**: Generate a QR code with a gift code to use.

All components are orchestrated within a single **Docker Compose** setup for seamless operation and deployed to **DigitalOcean VPC**.
