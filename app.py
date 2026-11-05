"""Indian Karigar Studio — demo sales dashboard (sample data only)."""
import pandas as pd, plotly.express as px, streamlit as st
st.set_page_config(page_title="Shop Sales Dashboard (demo)", layout="wide")
st.title("Shop Sales Dashboard")
st.caption("Demo built by Indian Karigar Studio. All numbers are synthetic sample data.")
up = st.sidebar.file_uploader("Upload your orders CSV (date, product, channel, city, qty, revenue)", type="csv")
df = pd.read_csv(up if up else "sample_orders.csv", parse_dates=["date"])
lo, hi = df.date.min().date(), df.date.max().date()
rng = st.sidebar.date_input("Date range", (lo, hi), min_value=lo, max_value=hi)
ch = st.sidebar.multiselect("Channel", sorted(df.channel.unique()), default=sorted(df.channel.unique()))
if isinstance(rng, tuple) and len(rng)==2:
    df = df[(df.date.dt.date>=rng[0]) & (df.date.dt.date<=rng[1])]
df = df[df.channel.isin(ch)]
orders = len(df); rev = df.revenue.sum()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Revenue", f"₹{rev:,.0f}"); c2.metric("Orders", f"{orders:,}")
c3.metric("Avg order value", f"₹{(rev/orders if orders else 0):,.0f}")
c4.metric("Units sold", f"{df.qty.sum():,}")
m = df.set_index("date").resample("W").revenue.sum().reset_index()
st.plotly_chart(px.line(m, x="date", y="revenue", title="Weekly revenue"), width="stretch")
a,b = st.columns(2)
a.plotly_chart(px.bar(df.groupby("product",as_index=False).revenue.sum().sort_values("revenue"),
               x="revenue", y="product", orientation="h", title="Revenue by product"), width="stretch")
b.plotly_chart(px.pie(df, names="channel", values="revenue", title="Revenue by channel"), width="stretch")
st.plotly_chart(px.bar(df.groupby("city",as_index=False).revenue.sum(), x="city", y="revenue", title="Revenue by city"), width="stretch")
with st.expander("Raw data"):
    st.dataframe(df, width="stretch")
    st.download_button("Download filtered CSV", df.to_csv(index=False), "filtered_orders.csv")
