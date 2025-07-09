import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("supermarket_sales.csv")
df.columns = df.columns.str.strip()
df['Total'] = df['Unit price'] * df['Quantity']
df['Date'] = pd.to_datetime(df['Date'])

# Judul Dashboard
st.title("📊 Dashboard Interaktif Supermarket Sales")
st.markdown("Laporan ini menyajikan visualisasi interaktif dari penjualan supermarket berdasarkan cabang, gender, " \
"dan metode pembayaran.")

# Sidebar filter
st.sidebar.header("🔍 Filter Data")
selected_branch = st.sidebar.multiselect("Pilih Cabang", options=df['Branch'].unique(), default=df['Branch'].unique())
selected_gender = st.sidebar.multiselect("Pilih Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_payment = st.sidebar.multiselect("Metode Pembayaran", options=df['Payment'].unique(), 
                                          default=df['Payment'].unique())

# Filter DataFrame
filtered_df = df[
    (df['Branch'].isin(selected_branch)) &
    (df['Gender'].isin(selected_gender)) &
    (df['Payment'].isin(selected_payment))
]

#Statistik Umum
st.subheader("📈 Ringkasan Statistik")
col1, col2, col3 = st.columns(3)
col1.metric("Total Pendapatan", f"${filtered_df['Total'].sum():,.2f}")
col2.metric("Rata-rata Pembelian", f"${filtered_df['Total'].mean():.2f}")
col3.metric("Rata-rata Rating", f"{filtered_df['Rating'].mean():.2f} / 10")

#Grafik 1: Total Penjualan per Product Line
st.subheader("🛒 Total Penjualan per Jenis Produk")
fig1, ax1 = plt.subplots()
sales_by_product = filtered_df.groupby("Product line")['Total'].sum().sort_values()
sales_by_product.plot(kind='barh', ax=ax1, color='skyblue')
ax1.set_xlabel("Total Penjualan")
ax1.set_ylabel("Produk")
st.pyplot(fig1)

#Grafik 2: Jumlah Transaksi per Cabang 
st.subheader("🏪 Jumlah Transaksi per Cabang")
fig2, ax2 = plt.subplots()
df['Branch'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax2)
ax2.set_ylabel("")
ax2.set_title("Distribusi Transaksi")
st.pyplot(fig2)

# Grafik 3: Tren Penjualan Harian
st.subheader("📅 Tren Penjualan Harian")
daily = filtered_df.groupby('Date')['Total'].sum()
fig3, ax3 = plt.subplots()
daily.plot(ax=ax3)
ax3.set_ylabel("Total Penjualan")
ax3.set_xlabel("Tanggal")
ax3.set_title("Total Penjualan Harian")
st.pyplot(fig3)

# Insight akhir
st.markdown("### 🔍 Insight")
st.markdown("""
- Produk dengan penjualan tertinggi dapat berubah tergantung filter cabang/gender.
- Metode pembayaran dominan bisa dilihat dengan memfilter payment method.
- Rating rata-rata cukup tinggi menandakan kepuasan pelanggan.
""")
