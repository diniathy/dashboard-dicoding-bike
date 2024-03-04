import pandas as pd
import streamlit as st

day_path = "Bike-sharing-dataset\day.csv"
day_df = pd.read_csv(day_path)
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("Bike sharing.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

st.header("Bike Sharing Dashboard 🚴🚴‍♀️")
st.subheader("Penyewaan Harian")
 
col1, col2 = st.columns(2)
 
with col1:
    total_casual = day_df.casual.sum()
    st.metric("Total Casual", value=total_casual)
 
with col2:
    total_registered = day_df.registered.sum()
    st.metric("Total Registered", value=total_registered)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["dteday"],
    day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#333A73"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Tren Peminjaman Sepeda")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])  
day_df = day_df.sort_values(by="dteday")  
recent_data = day_df[day_df["dteday"] >= day_df["dteday"].max() - pd.DateOffset(months=6)]
monthly_rentals = recent_data.groupby(pd.Grouper(key="dteday", freq="M"))["cnt"].sum()
monthly_rentals1 = monthly_rentals.reset_index()

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_rentals1["dteday"],
    monthly_rentals1["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Jumlah Peminjam Sepeda")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#265073", "#2D9596", "#211951", "#836FFF"]

working_comp = day_df.groupby("workingday").agg({
    "cnt":"sum"
})
working_comp.rename(index={0:"otherwise", 1:"weekend or holiday"}, inplace=True)
working_comp.reset_index(inplace=True)

sns.barplot(
    y="cnt",
    x="workingday",
    data=working_comp,
    palette=colors,
    ax=ax[1]
)
ax[1].set_title("Jumlah Peminjam Sepeda berdasarkan Hari Kerja", loc="center", fontsize=40)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].grid(axis="y", linestyle="--", alpha=1)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=35)

season_day = day_df.groupby("season").agg({
    "casual":"sum",
    "registered":"sum"
})
season_day["Total"] = season_day["casual"] + season_day["registered"]
season_day.rename(index={1:"springer",2:"summer", 3:"fall",4:"winter"}, inplace=True)
season_day.reset_index(inplace=True)

sns.barplot(
    y ="Total",
    x = "season",
    data = season_day.sort_values(by="Total", ascending=False),
    palette = colors,
    ax=ax[0]
)
ax[0].set_title("Jumlah Peminjam Sepeda Berdasarkan Cuaca", loc="center", fontsize=40)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].grid(axis="y", linestyle="--", alpha=1)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=35)

st.pyplot(fig)
