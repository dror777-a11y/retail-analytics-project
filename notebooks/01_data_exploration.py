import pandas as pd
import numpy as np

# קריאת הנתונים
print("=== טוען נתוני Superstore ===")
df = pd.read_csv('../data/raw/superstore_sample.csv')

# בדיקה בסיסית
print(f"\n📊 גודל הנתונים: {df.shape[0]:,} שורות, {df.shape[1]} עמודות")

print(f"\n💰 סיכומים כספיים:")
print(f"סך המכירות: ${df['Sales'].sum():,.2f}")
print(f"סך הרווחים: ${df['Profit'].sum():,.2f}")
print(f"שיעור רווחיות: {(df['Profit'].sum() / df['Sales'].sum() * 100):.1f}%")

print(f"\n📈 בחינת רווחיות:")
profitable_orders = df[df['Profit'] > 0].shape[0]
loss_orders = df[df['Profit'] < 0].shape[0]
print(f"הזמנות רווחיות: {profitable_orders:,} ({profitable_orders/len(df)*100:.1f}%)")
print(f"הזמנות בהפסד: {loss_orders:,} ({loss_orders/len(df)*100:.1f}%)")

print(f"\n🏪 פילוח לפי קטגוריות:")
category_summary = df.groupby('Category').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)
category_summary['Profit_Margin'] = (category_summary['Profit'] / category_summary['Sales'] * 100).round(1)
print(category_summary)

print(f"\n🌍 פילוח לפי אזורים:")
region_summary = df.groupby('Region').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
region_summary.columns = ['Sales', 'Profit', 'Orders']
region_summary['Avg_Order_Value'] = (region_summary['Sales'] / region_summary['Orders']).round(2)
print(region_summary)

print(f"\n👥 פילוח לפי סגמנט לקוחות:")
segment_summary = df.groupby('Segment').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Customer ID': 'nunique'
}).round(2)
segment_summary.columns = ['Sales', 'Profit', 'Customers']
print(segment_summary)

print(f"\n🚚 פילוח לפי אופן משלוח:")
shipping_summary = df.groupby('Ship Mode').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'count'
}).round(2)
shipping_summary.columns = ['Sales', 'Profit', 'Orders']
print(shipping_summary)

print(f"\n📅 ניתוח זמני:")
# המרת תאריכים
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

yearly_summary = df.groupby('Year').agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).round(2)
yearly_summary.columns = ['Sales', 'Profit', 'Orders']
print("פילוח שנתי:")
print(yearly_summary)

print(f"\n🔍 בדיקת איכות נתונים:")
print("בדיקת ערכים חסרים:")
missing_data = df.isnull().sum()
if missing_data.sum() > 0:
    print(missing_data[missing_data > 0])
else:
    print("✅ אין ערכים חסרים!")

print(f"\nבדיקת ערכים קיצוניים:")
print(f"מכירה מקסימלית: ${df['Sales'].max():,.2f}")
print(f"מכירה מינימלית: ${df['Sales'].min():,.2f}")
print(f"רווח מקסימלי: ${df['Profit'].max():,.2f}")
print(f"הפסד מקסימלי: ${df['Profit'].min():,.2f}")

print(f"\n📋 מוצרים מובילים (ללא רווח):")
top_loss_products = df[df['Profit'] < 0].groupby(['Category', 'Sub-Category']).agg({
    'Profit': 'sum',
    'Sales': 'sum'
}).sort_values('Profit').head(5)
if len(top_loss_products) > 0:
    print("מוצרים עם ההפסדים הגבוהים ביותר:")
    print(top_loss_products)

print(f"\n✅ סיכום: הנתונים נראים תקינים ומוכנים לניתוח מתקדם!")