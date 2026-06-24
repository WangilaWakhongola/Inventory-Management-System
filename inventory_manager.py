"""
Inventory Management System
A pure Python CLI application using SQLite for data storage.
No web server or external libraries required.
"""

import sqlite3
import os
from datetime import datetime


# ─── Database Setup ───────────────────────────────────────────────────────────

DB_FILE = "inventory.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                description TEXT,
                category    TEXT    NOT NULL,
                quantity    INTEGER DEFAULT 0,
                price       REAL    NOT NULL,
                reorder_level INTEGER DEFAULT 10,
                created_at  TEXT    DEFAULT (datetime('now')),
                updated_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


# ─── CRUD Operations ──────────────────────────────────────────────────────────

def add_product(name, category, quantity, price, description="", reorder_level=10):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO products (name, description, category, quantity, price, reorder_level)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, category, quantity, price, reorder_level))
        conn.commit()
    print(f"\n  Product '{name}' added successfully.")


def get_all_products():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()


def get_product_by_id(product_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()


def update_product(product_id, name, category, quantity, price, description, reorder_level):
    with get_connection() as conn:
        conn.execute("""
            UPDATE products
            SET name=?, description=?, category=?, quantity=?, price=?, reorder_level=?,
                updated_at=datetime('now')
            WHERE id=?
        """, (name, description, category, quantity, price, reorder_level, product_id))
        conn.commit()
    print(f"\n  Product ID {product_id} updated successfully.")


def delete_product(product_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
    print(f"\n  Product ID {product_id} deleted.")


def search_products(query="", category=""):
    with get_connection() as conn:
        sql = "SELECT * FROM products WHERE 1=1"
        params = []
        if query:
            sql += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
            params += [f"%{query.lower()}%", f"%{query.lower()}%"]
        if category:
            sql += " AND LOWER(category) = ?"
            params.append(category.lower())
        return conn.execute(sql, params).fetchall()


def get_stats():
    products = get_all_products()
    total_products = len(products)
    total_value = sum(p["quantity"] * p["price"] for p in products)
    low_stock = [p for p in products if p["quantity"] <= p["reorder_level"]]
    categories = list(set(p["category"] for p in products))
    return total_products, total_value, low_stock, categories


# ─── Display Helpers ──────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def separator(char="─", width=65):
    print(char * width)


def print_header(title):
    separator("═")
    print(f"  {title}")
    separator("═")


def status_label(quantity, reorder_level):
    return "⚠ Low Stock" if quantity <= reorder_level else "✔ In Stock"


def print_product_table(products):
    if not products:
        print("\n  No products found.\n")
        return

    separator()
    print(f"  {'ID':<5} {'Name':<22} {'Category':<14} {'Qty':>5} {'Price':>9} {'Status':<12}")
    separator()
    for p in products:
        status = status_label(p["quantity"], p["reorder_level"])
        print(f"  {p['id']:<5} {p['name']:<22} {p['category']:<14} {p['quantity']:>5} ${p['price']:>8.2f} {status}")
    separator()
    print(f"  Total items: {len(products)}\n")


def print_product_detail(p):
    separator()
    print(f"  ID          : {p['id']}")
    print(f"  Name        : {p['name']}")
    print(f"  Description : {p['description'] or '—'}")
    print(f"  Category    : {p['category']}")
    print(f"  Quantity    : {p['quantity']}")
    print(f"  Price       : ${p['price']:.2f}")
    print(f"  Reorder At  : {p['reorder_level']} units")
    print(f"  Total Value : ${p['quantity'] * p['price']:.2f}")
    print(f"  Status      : {status_label(p['quantity'], p['reorder_level'])}")
    print(f"  Created     : {p['created_at']}")
    print(f"  Updated     : {p['updated_at']}")
    separator()


# ─── Input Helpers ────────────────────────────────────────────────────────────

def prompt(label, default=None):
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"  {label}{suffix}: ").strip()
    return value if value else (str(default) if default is not None else "")


def prompt_int(label, default=None):
    while True:
        val = prompt(label, default)
        try:
            return int(val)
        except ValueError:
            print("  Please enter a whole number.")


def prompt_float(label, default=None):
    while True:
        val = prompt(label, default)
        try:
            return float(val)
        except ValueError:
            print("  Please enter a valid number.")


def confirm(message):
    return input(f"  {message} (y/n): ").strip().lower() == "y"


# ─── Menu Actions ─────────────────────────────────────────────────────────────

def view_dashboard():
    clear()
    print_header("DASHBOARD")
    total_products, total_value, low_stock, categories = get_stats()
    print(f"  Total Products  : {total_products}")
    print(f"  Total Value     : ${total_value:,.2f}")
    print(f"  Low Stock Items : {len(low_stock)}")
    print(f"  Categories      : {', '.join(categories) if categories else 'None'}")
    separator()

    if low_stock:
        print("\n  ⚠  LOW STOCK ALERTS:")
        separator("-")
        for p in low_stock:
            print(f"  • {p['name']} ({p['category']}) — {p['quantity']} left (reorder at {p['reorder_level']})")
        separator("-")

    input("\n  Press Enter to return to menu...")


def view_all_products():
    clear()
    print_header("ALL PRODUCTS")
    products = get_all_products()
    print_product_table(products)
    input("  Press Enter to return to menu...")


def view_product():
    clear()
    print_header("VIEW PRODUCT DETAILS")
    product_id = prompt_int("Enter Product ID")
    p = get_product_by_id(product_id)
    if p:
        print_product_detail(p)
    else:
        print(f"\n  No product found with ID {product_id}.")
    input("\n  Press Enter to return to menu...")


def add_product_menu():
    clear()
    print_header("ADD NEW PRODUCT")
    name = prompt("Product Name")
    if not name:
        print("  Name cannot be empty.")
        input("  Press Enter to return...")
        return
    category = prompt("Category")
    if not category:
        print("  Category cannot be empty.")
        input("  Press Enter to return...")
        return
    description = prompt("Description (optional)")
    quantity = prompt_int("Quantity", default=0)
    price = prompt_float("Price ($)", default=0.0)
    reorder_level = prompt_int("Reorder Level (alert when below this)", default=10)

    print()
    separator()
    print(f"  Name     : {name}")
    print(f"  Category : {category}")
    print(f"  Qty      : {quantity}")
    print(f"  Price    : ${price:.2f}")
    print(f"  Reorder  : {reorder_level}")
    separator()

    if confirm("Save this product?"):
        add_product(name, category, quantity, price, description, reorder_level)
    else:
        print("  Cancelled.")
    input("  Press Enter to return to menu...")


def update_product_menu():
    clear()
    print_header("UPDATE PRODUCT")
    product_id = prompt_int("Enter Product ID to update")
    p = get_product_by_id(product_id)
    if not p:
        print(f"\n  No product found with ID {product_id}.")
        input("  Press Enter to return...")
        return

    print(f"\n  Editing: {p['name']} (leave blank to keep current value)\n")
    name = prompt("Name", p["name"]) or p["name"]
    category = prompt("Category", p["category"]) or p["category"]
    description = prompt("Description", p["description"] or "")
    quantity = prompt_int("Quantity", p["quantity"])
    price = prompt_float("Price ($)", p["price"])
    reorder_level = prompt_int("Reorder Level", p["reorder_level"])

    if confirm("\n  Save changes?"):
        update_product(product_id, name, category, quantity, price, description, reorder_level)
    else:
        print("  Cancelled.")
    input("  Press Enter to return to menu...")


def delete_product_menu():
    clear()
    print_header("DELETE PRODUCT")
    product_id = prompt_int("Enter Product ID to delete")
    p = get_product_by_id(product_id)
    if not p:
        print(f"\n  No product found with ID {product_id}.")
        input("  Press Enter to return...")
        return

    print(f"\n  You are about to delete: {p['name']} (Category: {p['category']})")
    if confirm("Are you sure?"):
        delete_product(product_id)
    else:
        print("  Deletion cancelled.")
    input("  Press Enter to return to menu...")


def search_menu():
    clear()
    print_header("SEARCH PRODUCTS")
    query = prompt("Search by name/description (or leave blank)")
    category = prompt("Filter by category (or leave blank)")
    results = search_products(query, category)
    print()
    print_product_table(results)
    input("  Press Enter to return to menu...")


# ─── Main Menu ────────────────────────────────────────────────────────────────

def main_menu():
    initialize_db()
    while True:
        clear()
        print_header("INVENTORY MANAGEMENT SYSTEM")
        print("  1. Dashboard & Alerts")
        print("  2. View All Products")
        print("  3. View Product Details")
        print("  4. Add Product")
        print("  5. Update Product")
        print("  6. Delete Product")
        print("  7. Search / Filter Products")
        print("  0. Exit")
        separator()
        choice = input("  Select option: ").strip()

        if choice == "1":
            view_dashboard()
        elif choice == "2":
            view_all_products()
        elif choice == "3":
            view_product()
        elif choice == "4":
            add_product_menu()
        elif choice == "5":
            update_product_menu()
        elif choice == "6":
            delete_product_menu()
        elif choice == "7":
            search_menu()
        elif choice == "0":
            print("\n  Goodbye!\n")
            break
        else:
            print("\n  Invalid option. Please try again.")
            input("  Press Enter to continue...")


if __name__ == "__main__":
    main_menu()
