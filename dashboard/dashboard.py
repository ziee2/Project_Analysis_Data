import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Dapatkan direktori di mana 'dashboard.py' berada
current_directory = os.path.dirname(__file__)

# Buat path untuk folder 'data'
data_directory = os.path.join(current_directory, '..', 'data')

# Buat path lengkap untuk file CSV di folder 'data'
order_items_file = os.path.join(data_directory, 'order_items_dataset.csv')
orders_file = os.path.join(data_directory, 'orders_dataset.csv')
products_file = os.path.join(data_directory, 'products_dataset.csv')
reviews_file = os.path.join(data_directory, 'order_reviews_dataset.csv')

# Load dataset dari folder 'data'
order_items_df = pd.read_csv(order_items_file)
orders_df = pd.read_csv(orders_file)
products_df = pd.read_csv(products_file)
reviews_df = pd.read_csv(reviews_file)

st.title('Analisis Penjualan dan Review Produk')

# Pertanyaan 1: Performa Penjualan Produk
st.header('Performa Penjualan Produk Berdasarkan Kategori')

# Merge order_items dengan products untuk mendapatkan detail kategori
order_items_with_category = pd.merge(order_items_df, products_df, on='product_id', how='left')

# Hitung total pendapatan per kategori produk
revenue_by_category = order_items_with_category.groupby('product_category_name')['price'].sum().reset_index()

# Urutkan berdasarkan total pendapatan secara descending
revenue_by_category = revenue_by_category.sort_values(by='price', ascending=False)

# Tampilkan 10 kategori produk teratas berdasarkan pendapatan
st.subheader("Top 10 Kategori Produk Berdasarkan Total Pendapatan")
st.dataframe(revenue_by_category.head(10))

# Visualisasi pendapatan berdasarkan kategori produk
st.subheader('Visualisasi: Top 10 Kategori Produk Berdasarkan Pendapatan')
plt.figure(figsize=(12, 6))
plt.bar(revenue_by_category['product_category_name'][:10], revenue_by_category['price'][:10])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Kategori Produk')
plt.ylabel('Total Pendapatan')
plt.title('Top 10 Kategori Produk Berdasarkan Total Pendapatan')
st.pyplot(plt)

st.write("""
Dari hasil analisis penjualan, berikut adalah kesimpulan dari 10 kategori produk dengan pendapatan tertinggi:

1. **beleza_saude** total pendapatan **1.258.681,34**.
2. **relogios_presentes** total pendapatan **1.205.005,68**. 
3. **cama_mesa_banho** total pendapatan **1.036.988,68**.
4. **esporte_lazer** total pendapatan **988.048,97**
5. **informatica_acessorios** Total Pendapatan **911.954,32**
6. **moveis_decoracao** total pendapatan **729.762,49**
7. **cool_stuff** total pendapatan **635290.85**
8. **utilidades_domesticas** total pendapatan **632248.66**
9. **automotivo** total pendapatan **592720.11**
10. **ferramentas_jardim** total pendapatan **485256.46**

Secara keseluruhan, data ini menunjukkan kontributor utama terhadap pendapatan. Kategori diatas ini dapat menjadi fokus utama untuk alokasi sumber daya dan strategi pemasaran di masa mendatang.
""")

st.write("Dari visualisasi di atas, kita dapat melihat Top 10 kategori produk berdasarkan total pendapatan. yan pertama teradapat 1. belezza_saude")

# Pertanyaan 2: Hubungan antara Review Score dengan Waktu Pengiriman
st.header('Hubungan Review Score dengan Waktu Pengiriman')

# Merge orders dataset dengan reviews berdasarkan 'order_id'
orders_with_reviews = pd.merge(orders_df, reviews_df, on='order_id', how='left')

# Konversi ke format datetime
orders_with_reviews['order_purchase_timestamp'] = pd.to_datetime(orders_with_reviews['order_purchase_timestamp'], errors='coerce')
orders_with_reviews['order_delivered_customer_date'] = pd.to_datetime(orders_with_reviews['order_delivered_customer_date'], errors='coerce')

# Hitung waktu pengiriman dalam hari
orders_with_reviews['delivery_time'] = (orders_with_reviews['order_delivered_customer_date'] - orders_with_reviews['order_purchase_timestamp']).dt.days

# Hapus baris dengan NaT di 'delivery_time' (mewakili pesanan yang tidak terkirim)
orders_with_reviews_clean = orders_with_reviews.dropna(subset=['delivery_time'])

# Hitung rata-rata review score berdasarkan waktu pengiriman
average_review_by_delivery = orders_with_reviews_clean.groupby('delivery_time')['review_score'].mean().reset_index()

# Tampilkan rata-rata review score berdasarkan waktu pengiriman
st.subheader("Rata-Rata Skor Review Berdasarkan Waktu Pengiriman")
st.dataframe(average_review_by_delivery.head())

# Visualisasi rata-rata review score berdasarkan waktu pengiriman
st.subheader('Visualisasi: Rata-Rata Skor Review Berdasarkan Waktu Pengiriman')
plt.figure(figsize=(12, 6))
plt.plot(average_review_by_delivery['delivery_time'], average_review_by_delivery['review_score'], marker='o')
plt.xlabel('Waktu Pengiriman (Hari)')
plt.ylabel('Rata-Rata Skor Review')
plt.title('Rata-Rata Skor Review Berdasarkan Waktu Pengiriman')
st.pyplot(plt)

st.write("Dari visualisasi di atas, kita dapat melihat bahwa semakin lama waktu pengiriman, semakin rendah rata-rata skor ulasan, yang menunjukkan dampak negatif keterlambatan pengiriman pada kepuasan pelanggan.")
