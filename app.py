import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Airbnb Dashboard", layout="wide")

# ================= GREEN + WHITE THEME =================
st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#f8fff8,#e6f4ea);
}

/* Title */
h1{
text-align:center;
color:#14532d;
}

/* KPI cards */
div[data-testid="metric-container"]{
background-color: white;
padding:15px;
border-radius:15px;
box-shadow:0px 5px 15px rgba(0,0,0,0.08);
border-left:6px solid #14532d;
}

/* Charts */
.stPlotlyChart{
background-color:white;
padding:15px;
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("🌿 Airbnb NYC Analytics Dashboard")

# ================= LOAD DATA =================
df = pd.read_csv("AB_NYC_2019.csv")

# ================= KPI =================
c1, c2, c3 = st.columns(3)

c1.metric("💰 Avg Price", f"${int(df['price'].mean())}")
c2.metric("🏠 Total Listings", df.shape[0])
c3.metric("⭐ Avg Reviews", int(df['number_of_reviews'].mean()))

st.markdown("---")

# ================= CHART 1 =================
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        df,
        x="price",
        nbins=50,
        title="Price Distribution",
        color_discrete_sequence=["#14532d"]
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    avg_price = df.groupby("neighbourhood_group")["price"].mean().reset_index()

    fig = px.bar(
        avg_price,
        x="neighbourhood_group",
        y="price",
        color="neighbourhood_group",
        title="Average Price by Location"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= CHART 2 =================
col3, col4 = st.columns(2)

with col3:
    fig = px.box(
        df,
        x="room_type",
        y="price",
        color="room_type",
        title="Price vs Room Type"
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.scatter(
        df,
        x="number_of_reviews",
        y="price",
        size="availability_365",
        color="neighbourhood_group",
        title="Reviews vs Price"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= MAP =================
st.subheader("📍 Location Map")

fig = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="neighbourhood_group",
    size="price",
    zoom=10,
    mapbox_style="carto-positron"
)

st.plotly_chart(fig, use_container_width=True)

# ================= ANALYSIS TABLES (NEW 🔥) =================

st.subheader("📊 Detailed Analysis Tables")

col5, col6 = st.columns(2)

with col5:
    st.write("### Top 10 Expensive Listings")
    top_price = df[['name','price','neighbourhood_group']].sort_values(by='price', ascending=False).head(10)
    st.dataframe(top_price)

with col6:
    st.write("### Most Reviewed Listings")
    top_reviews = df[['name','number_of_reviews','neighbourhood_group']].sort_values(by='number_of_reviews', ascending=False).head(10)
    st.dataframe(top_reviews)

# ================= EXTRA TABLE =================
st.write("### Average Price by Room Type")

room_table = df.groupby("room_type")["price"].mean().reset_index()
st.dataframe(room_table)

# ================= CORRELATION =================
st.subheader("🔥 Correlation Analysis")

corr = df.select_dtypes(include=['int64','float64']).corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Greens"
)

st.plotly_chart(fig, use_container_width=True)

# ================= INSIGHTS =================
st.subheader("📌 Key Insights")

st.markdown("""
- Manhattan listings have the highest prices 💰  
- Entire homes are significantly more expensive 🏠  
- Listings with more reviews indicate higher demand ⭐  
- Location strongly influences pricing 📍  
""")

st.success("Dashboard Ready 🚀")