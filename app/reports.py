from app import db
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import os

from app import THRESHOLD
from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ReportForm(FlaskForm):
    days = StringField('Days', [validators.DataRequired()])


def generate_sales_report(days: int = 30):
    end_date = datetime.now()
    # days = days from request
    start_date = end_date - timedelta(days=days)
        
    sales_data = db.orders.find({"order_date": {"$gte": start_date, "$lt": end_date}})
    sales_summary = defaultdict(int)
    for order in sales_data:
        if order['status'] == 'completed':
            sales_summary[order['item_name']] += order['quantity']
    sales_summary = [{"item_name": k, "total_sales": v} for k, v in sales_summary.items()]

    item_names = [item['item_name'] for item in sales_summary]
    total_sales = [item['total_sales'] for item in sales_summary]

    plt.figure(figsize=(10, 5))
    plt.bar(item_names, total_sales, color='blue')
    plt.xlabel('Product')
    plt.ylabel('Total Sales')
    plt.title('Sales Report')
    
    # Ensure the directory exists
    output_dir = os.path.join('InventoryManagement', 'app', 'static', 'images')
    os.makedirs(output_dir, exist_ok=True)
    
    plt.savefig(os.path.join(output_dir, 'sales_report.png'))
    plt.close()

def generate_inventory_report(category='All'):
    if category == 'All':
        inventory_data = db.items.find()
    else:
        inventory_data = db.items.find({'category': category})
    
    inventory_summary = []
    for item in inventory_data:
        item_name = item['item_name']
        count = item['count']
        
        if count < THRESHOLD:
            color = 'red'
        else:
            color = 'green'
        
        inventory_summary.append({"item_name": item_name, "count": count, "color": color})
    
    if not inventory_summary:
        return None  # No data to generate report

    item_names = [item['item_name'] for item in inventory_summary]
    counts = [item['count'] for item in inventory_summary]
    colors = [item['color'] for item in inventory_summary]
    
    plt.figure(figsize=(10, 5))
    bars = plt.bar(item_names, counts, color=colors)
    plt.xlabel('Product')
    plt.ylabel('Inventory Count')
    plt.title(f'Inventory Report - {category}')

    output_dir = os.path.join('InventoryManagement', 'app', 'static', 'images')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, f'inventory_report_{category.lower()}.png'))
    plt.close()
