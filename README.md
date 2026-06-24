# Inventory Management System

A beginner-friendly, pure Python CLI application for managing and tracking inventory items. No web server or external libraries required — just Python and a terminal.

## Features

- **Dashboard** — View total products, inventory value, and live low-stock alerts
- **Add Products** — Enter name, category, quantity, price, description, and reorder level
- **View Products** — Browse the full inventory in a formatted table
- **Product Details** — Inspect every field of a specific product
- **Update Products** — Edit any field; existing values shown as defaults
- **Delete Products** — Remove items with a confirmation step
- **Search & Filter** — Find products by name/description and filter by category
- **SQLite Storage** — Data is persisted locally in `inventory.db` (auto-created)

## Requirements

- Python 3.6 or higher
- No external packages needed (uses only the Python standard library)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Inventory-Management-System.git
cd Inventory-Management-System
```

### 2. Run the application

```bash
python inventory_manager.py
```

The database file `inventory.db` is created automatically in the same directory on first run.

## Usage

On launch you will see the main menu:

```
═════════════════════════════════════════════════════════════════
  INVENTORY MANAGEMENT SYSTEM
═════════════════════════════════════════════════════════════════
  1. Dashboard & Alerts
  2. View All Products
  3. View Product Details
  4. Add Product
  5. Update Product
  6. Delete Product
  7. Search / Filter Products
  0. Exit
─────────────────────────────────────────────────────────────────
  Select option:
```

Type the number of the option you want and press **Enter**.

### Adding a Product

1. Select option `4`
2. Enter the product name, category, description (optional), quantity, price, and reorder level
3. Confirm to save

### Updating a Product

1. Select option `5`
2. Enter the ID of the product to edit (visible in the product table)
3. For each field, press Enter to keep the current value or type a new one
4. Confirm to save

### Searching Products

1. Select option `7`
2. Enter a keyword to search by name or description (or leave blank)
3. Enter a category to filter by (or leave blank)

## Project Structure

```
Inventory-Management-System/
├── inventory_manager.py   # Main application (all logic in one file)
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
└── inventory.db           # SQLite database (auto-generated, not committed)
```

## How It Works

The application is built entirely on Python's standard library:

- **`sqlite3`** — built-in database engine for storing products
- **`os`** — used for clearing the terminal screen
- **`datetime`** — used to timestamp created/updated records

All data is stored in a local `inventory.db` file. Deleting this file resets the inventory.

## Comparison with Original Version

| Feature | Original (Flask) | This Version (CLI) |
|---|---|---|
| Interface | Web browser | Terminal |
| Backend | Flask + SQLAlchemy | Pure Python + sqlite3 |
| Dependencies | flask, flask-sqlalchemy | None |
| Database | SQLite via ORM | SQLite via built-in driver |
| API | REST (JSON) | Not applicable |
| Setup | pip install required | Run directly |

## Roadmap

- CSV export of inventory data
- User authentication (multi-user support)
- Inventory change history log
- Barcode / SKU field
- Low-stock email notifications

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please follow [PEP 8](https://pep8.org/) style guidelines.

## Author

**Emmanuel Wakhongola**
- GitHub: [@WangilaWakhongola](https://github.com/WangilaWakhongola)
- Email: wangilaemmanuel06@gmail.com

## License

This project is licensed under the MIT License.
