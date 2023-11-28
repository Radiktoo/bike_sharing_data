import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')




all_df = pd.read_csv('dashboard/bike_all_data.csv')

st.header('Bike Sharing Dashboard :bike:')
st.subheader('Daily & Hourly Orders')

col1, col2 = st.columns(2)



with col1:
    total_orders_dy = all_df.cnt_daily.count()
    st.metric("Total orders daily", value=total_orders_dy)
 
with col2:
    total_orders_hr = all_df.cnt_hourly.count()
    st.metric("Total orders hourly", value=total_orders_hr)

all_df['mnth_daily'] = pd.to_datetime(all_df['mnth_daily'], format='%b').dt.strftime('%b')

st.subheader("Pola Jumlah Sewa Sepeda Harian Berdasarkan Bulan")
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="mnth_daily", y="cnt_daily", data=all_df, ci=None, color="#D0A2F7", markers='o', linewidth=5)
ax.set_xlabel("Bulan", fontsize=20)
ax.set_ylabel("Jumlah Sewa Sepeda Harian", fontsize=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Pengaruh Musim Terhadap Jumlah Sewa Sepeda Harian ")



byseason_df = all_df.groupby(by="season",).cnt_daily.nunique().sort_values(ascending=False).reset_index()



fig, ax = plt.subplots(figsize=(20, 10))

colors = ["#D0A2F7", "#DCBFFF", "#DCBFFF", "#DCBFFF"]
sns.barplot(
        x="cnt_daily",
        y="season",
        data=byseason_df.sort_values(by="cnt_daily", ascending=False),
        palette=colors
    )

ax.set_xlabel('Jumlah Sewa Harian', fontsize=35)
ax.set_ylabel('Musim', fontsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)
    


st.subheader("Regresi Linier Sederhana")

import numpy as np
from sklearn.linear_model import LinearRegression 
    
    
y = all_df["cnt_daily"] # variabel dependen: jumlah penyewa sepeda harian
X = all_df[["temp_daily"]] # variabel independen: suhu rata-rata harian

# Membuat objek regresi linier
reg = LinearRegression()

# Melakukan estimasi parameter
reg.fit(X, y)

# Mendapatkan nilai intercept dan slope
b0 = reg.intercept_
b1 = reg.coef_[0]

# Membuat fungsi regresi linier
def reg_func(x):
  return b0 + b1 * x

# Membuat vektor x untuk plot garis
x_plot = np.linspace(X.min(), X.max(), 100)

y_plot = reg_func(x_plot)

fig, ax = plt.subplots(figsize=(20, 10))
# Membuat plot scatter
ax.scatter(X, y, color="#D0A2F7", label="Data")

# Membuat plot garis regresi
ax.plot(x_plot, y_plot, color="red", label="Regresi")

# Memberi judul dan label

ax.set_xlabel("Suhu Rata-Rata Harian", fontsize=20)
ax.set_ylabel("Jumlah Penyewa Sepeda Harian", fontsize=20)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

# Menampilkan legenda
ax.legend(fontsize='large')

    # Menampilkan plot
st.pyplot(fig)
