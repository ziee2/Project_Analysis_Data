import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime



# Merge orders, order items, customers, and reviews to create a comprehensive main dataset

# Load datasets
customers_df = pd.read_csv('E:/KULIAHAHAHAH/Studi Independet Bersertifikat (Bangkit)/Dicoding/submission/data/customers_dataset.csv')
reviews_df = pd.read_csv('E:/KULIAHAHAHAH/Studi Independet Bersertifikat (Bangkit)/Dicoding/submission/data/order_reviews_dataset.csv')
products_df = pd.read_csv('E:/KULIAHAHAHAH/Studi Independet Bersertifikat (Bangkit)/Dicoding/submission/data/products_dataset.csv')

# Merge orders with customers
orders_with_customers = pd.merge(orders_df_clean, customers_df, on='customer_id', how='inner')

# Merge with order items to add product and order details
orders_items_customers = pd.merge(orders_with_customers, order_items_df_clean, on='order_id', how='inner')

# Merge with reviews to add review details
main_data = pd.merge(orders_items_customers, reviews_df, on='order_id', how='left')

# Merge with products to get product categories
main_data = pd.merge(main_data, products_df, on='product_id', how='left')

# Calculate additional metrics
main_data['order_purchase_timestamp'] = pd.to_datetime(main_data['order_purchase_timestamp'])
main_data['order_delivered_customer_date'] = pd.to_datetime(main_data['order_delivered_customer_date'], errors='coerce')

# Calculate delivery time in days
main_data['delivery_time'] = (main_data['order_delivered_customer_date'] - main_data['order_purchase_timestamp']).dt.days

# Add RFM data (recency, frequency, monetary) for each customer
rfm_df = rfm_df[['customer_unique_id', 'Recency', 'Frequency', 'Monetary']]
main_data = pd.merge(main_data, rfm_df, on='customer_unique_id', how='left')

# Save to CSV file for use in Streamlit
main_data.to_csv('main_data.csv', index=False)
