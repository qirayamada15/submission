import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
all_data = pd.read_csv('all.csv')

# Set Judul
st.title('Brazilian E-commerce Sales Dashboard')

# Metrik Utama

# Total Penjualan
total_sales = all_data['price'].sum()
st.metric("Total Penjualan", f"R${total_sales:,.2f}")

# Jumlah Pesanan
total_orders = all_data['order_id'].nunique()
st.metric("Jumlah Pesanan", total_orders)

# Pelanggan Aktif
active_customers = all_data['customer_id'].nunique()
st.metric("Pelanggan Aktif", active_customers)

# Rata-rata Nilai Pesanan
average_order_value = total_sales / total_orders
st.metric("Rata-rata Nilai Pesanan", f"R${average_order_value:,.2f}")

# TREN PENJUALAN

# Penjualan Harian/Mingguan/Bulanan
st.header("Tren Penjualan")
sales_time_period = st.selectbox("Pilih Periode Waktu", ["Harian", "Mingguan", "Bulanan"])

if sales_time_period == "Harian":
    # Agregasi penjualan harian
    daily_sales = all_data.groupby(pd.to_datetime(all_data['order_purchase_timestamp']).dt.date)['price'].sum().reset_index()
    daily_sales.columns = ['Tanggal', 'Penjualan']
    st.line_chart(daily_sales.set_index('Tanggal'))

elif sales_time_period == "Mingguan":
    # Agregasi penjualan mingguan
    weekly_sales = all_data.groupby(pd.to_datetime(all_data['order_purchase_timestamp']).dt.totimestamp().astype('datetime64[W]'))['price'].sum().reset_index()
    weekly_sales.columns = ['Minggu', 'Penjualan']
    st.line_chart(weekly_sales.set_index('Minggu'))

elif sales_time_period == "Bulanan":
    # Agregasi penjualan bulanan
    monthly_sales = all_data.groupby(pd.to_datetime(all_data['order_purchase_timestamp']).dt.to_period('M'))['price'].sum().reset_index()
    monthly_sales.columns = ['Bulan', 'Penjualan']
    monthly_sales['Bulan'] = monthly_sales['Bulan'].dt.to_timestamp()
    st.line_chart(monthly_sales.set_index('Bulan'))

# PERFORMA PRODUK

st.header("Performa Produk")

# Produk Terlaris
top_selling_products = all_data.groupby('product_id')['price'].sum().sort_values(ascending=False).head(10)
st.subheader("Produk Terlaris (Berdasarkan Pendapatan)")
st.bar_chart(top_selling_products)

# PERILAKU PELANGGAN

st.header("Perilaku Pelanggan")

# Metode Pembayaran Terpopuler
payment_methods = all_data['payment_type'].value_counts()
st.subheader("Metode Pembayaran Terpopuler")
fig, ax = plt.subplots()
ax.pie(payment_methods, labels=payment_methods.index, autopct='%1.1f%%')
st.pyplot(fig)

# ANALISIS DEMOGRAFIS

st.header("Analisis Demografis")

# Distribusi Pelanggan berdasarkan Lokasi
customer_locations = all_data['customer_state'].value_counts()
st.subheader("Distribusi Pelanggan berdasarkan Lokasi")
st.bar_chart(customer_locations)

# WAWASAN DAN REKOMENDASI

st.header("Wawasan dan Rekomendasi")

# Contoh wawasan dan rekomendasi
st.write("- Penjualan menunjukkan tren positif selama setahun terakhir.")
st.write("- Produk terlaris adalah [masukkan nama produk terlaris]. Pertimbangkan untuk menjalankan promosi untuk produk ini.")
st.write("- Sebagian besar pelanggan menggunakan [masukkan metode pembayaran terpopuler]. Pastikan untuk mendukung metode pembayaran ini.")
