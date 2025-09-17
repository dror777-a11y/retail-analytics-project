import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# הגדרת random seed לתוצאות עקביות
np.random.seed(42)
random.seed(42)

# פרמטרים לנתונים
num_orders = 9000
start_date = datetime(2019, 1, 1)
end_date = datetime(2022, 12, 31)

print("יוצר נתוני Superstore...")

# רשימות נתונים
categories = ['Office Supplies', 'Furniture', 'Technology']
sub_categories = {
    'Office Supplies': ['Paper', 'Binders', 'Pens & Art Supplies', 'Storage', 'Labels'],
    'Furniture': ['Chairs', 'Tables', 'Bookcases', 'Furnishings'],
    'Technology': ['Phones', 'Computers', 'Machines', 'Accessories']
}

segments = ['Consumer', 'Corporate', 'Home Office']
regions = ['Central', 'East', 'South', 'West']
states = ['California', 'New York', 'Texas', 'Florida', 'Illinois']
cities = ['New York City', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia']
ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']

# פונקציה ליצירת תאריך רנדומלי
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# יצירת הנתונים
data = []
order_id_counter = 1000

print("מייצר נתונים...")

for i in range(num_orders):
    if i % 1000 == 0:
        print(f"עיבדתי {i} הזמנות...")
    
    # פרטי הזמנה
    order_id = f"CA-{2019 + random.randint(0, 3)}-{order_id_counter}"
    order_date = random_date(start_date, end_date)
    ship_date = order_date + timedelta(days=random.randint(1, 10))
    
    # בחירת מוצר
    category = random.choice(categories)
    sub_category = random.choice(sub_categories[category])
    product_name = f"{sub_category} Product {random.randint(1, 100)}"
    
    # נתוני מכירה
    quantity = random.randint(1, 20)
    discount = random.choice([0, 0.05, 0.1, 0.15, 0.2])
    
    # מחירים לפי קטגוריה
    if category == 'Office Supplies':
        unit_price = round(random.uniform(5, 100), 2)
    elif category == 'Furniture':
        unit_price = round(random.uniform(50, 800), 2)
    else:  # Technology
        unit_price = round(random.uniform(100, 2000), 2)
    
    sales = round(quantity * unit_price * (1 - discount), 2)
    profit = round(sales * random.uniform(0.05, 0.4), 2)
    
    # במקרים נדירים - הפסד
    if random.random() < 0.05:
        profit = -abs(profit)
    
    # נתוני לקוח וגיאוגרפיה
    customer_name = f"Customer_{random.randint(1000, 9999)}"
    
    # הוספת השורה
    data.append({
        'Row ID': i + 1,
        'Order ID': order_id,
        'Order Date': order_date.strftime('%m/%d/%Y'),
        'Ship Date': ship_date.strftime('%m/%d/%Y'),
        'Ship Mode': random.choice(ship_modes),
        'Customer ID': f"CG-{random.randint(10000, 99999)}",
        'Customer Name': customer_name,
        'Segment': random.choice(segments),
        'Country': 'United States',
        'City': random.choice(cities),
        'State': random.choice(states),
        'Postal Code': random.randint(10000, 99999),
        'Region': random.choice(regions),
        'Product ID': f"OFF-{random.randint(1000, 9999)}",
        'Category': category,
        'Sub-Category': sub_category,
        'Product Name': product_name,
        'Sales': sales,
        'Quantity': quantity,
        'Discount': discount,
        'Profit': profit
    })
    
    order_id_counter += 1

print("יוצר DataFrame...")

# יצירת DataFrame
df = pd.DataFrame(data)

# יצירת תיקיות אם לא קיימות
import os
os.makedirs('data', exist_ok=True)
os.makedirs('data/raw', exist_ok=True)

# שמירת הקובץ
df.to_csv('data/raw/superstore_sample.csv', index=False)

print(f"\n✅ הצלחה! נוצר dataset עם {len(df)} שורות ו-{len(df.columns)} עמודות")
print(f"📁 הקובץ נשמר ב: data/raw/superstore_sample.csv")

print("\n📊 5 השורות הראשונות:")
print(df.head().to_string())

print(f"\n📈 סטטיסטיקות בסיסיות:")
print(f"סך המכירות: ${df['Sales'].sum():,.2f}")
print(f"סך הרווחים: ${df['Profit'].sum():,.2f}")
print(f"מספר קטגוריות: {df['Category'].nunique()}")
print(f"מספר אזורים: {df['Region'].nunique()}")
print(f"טווח תאריכים: {df['Order Date'].min()} עד {df['Order Date'].max()}")