import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
order_items_df = pd.read_csv('../data/order_items_dataset.csv')
orders_df = pd.read_csv('../data/orders_dataset.csv')
products_df = pd.read_csv('../data/products_dataset.csv')
reviews_df = pd.read_csv('../data/order_reviews_dataset.csv')

st.title('Analisis Penjualan dan Review Produk')

# Pertanyaan 1: Performa Penjualan Produk
st.header('Performa Penjualan Produk Berdasarkan Kategori')

# Merge order_items with products to get category details
order_items_with_category = pd.merge(order_items_df, products_df, on='product_id', how='left')

# Calculate total revenue per product category
revenue_by_category = order_items_with_category.groupby('product_category_name')['price'].sum().reset_index()

# Sort by total revenue in descending order
revenue_by_category = revenue_by_category.sort_values(by='price', ascending=False)

# Display the top 10 product categories by revenue
st.subheader("Top 10 Kategori Produk Berdasarkan Total Pendapatan")
st.dataframe(revenue_by_category.head(10))

# Visualization of revenue by product category
st.subheader('Visualisasi: Top 10 Kategori Produk Berdasarkan Pendapatan')
plt.figure(figsize=(12, 6))
plt.bar(revenue_by_category['product_category_name'][:10], revenue_by_category['price'][:10])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Kategori Produk')
plt.ylabel('Total Pendapatan')
plt.title('Top 10 Kategori Produk Berdasarkan Total Pendapatan')
st.pyplot(plt)

# Pertanyaan 2: Hubungan antara Review Score dengan Waktu Pengiriman
st.header('Hubungan Review Score dengan Waktu Pengiriman')

# Merge orders dataset with reviews on 'order_id'
orders_with_reviews = pd.merge(orders_df, reviews_df, on='order_id', how='left')

# Convert to datetime format
orders_with_reviews['order_purchase_timestamp'] = pd.to_datetime(orders_with_reviews['order_purchase_timestamp'], errors='coerce')
orders_with_reviews['order_delivered_customer_date'] = pd.to_datetime(orders_with_reviews['order_delivered_customer_date'], errors='coerce')

# Calculate delivery time in days
orders_with_reviews['delivery_time'] = (orders_with_reviews['order_delivered_customer_date'] - orders_with_reviews['order_purchase_timestamp']).dt.days

# Remove rows with NaT in 'delivery_time' (representing undelivered orders)
orders_with_reviews_clean = orders_with_reviews.dropna(subset=['delivery_time'])

# Calculate the average review score by delivery time
average_review_by_delivery = orders_with_reviews_clean.groupby('delivery_time')['review_score'].mean().reset_index()

# Display average review score by delivery time
st.subheader("Rata-Rata Skor Review Berdasarkan Waktu Pengiriman")
st.dataframe(average_review_by_delivery.head())

# Visualization of average review score by delivery time
st.subheader('Visualisasi: Rata-Rata Skor Review Berdasarkan Waktu Pengiriman')
plt.figure(figsize=(12, 6))
plt.plot(average_review_by_delivery['delivery_time'], average_review_by_delivery['review_score'], marker='o')
plt.xlabel('Waktu Pengiriman (Hari)')
plt.ylabel('Rata-Rata Skor Review')
plt.title('Rata-Rata Skor Review Berdasarkan Waktu Pengiriman')
st.pyplot(plt)

st.write("Dari visualisasi di atas, kita dapat melihat bahwa semakin lama waktu pengiriman, semakin rendah rata-rata skor ulasan, yang menunjukkan dampak negatif keterlambatan pengiriman pada kepuasan pelanggan.")
