import streamlit as st
from supabase import create_client

# Supabase connection
url = "https://YOUR-PROJECT-URL.supabase.co"
key = "YOUR-ANON-PUBLIC-KEY"
supabase = create_client(url, key)

st.title("💰 Expense Tracker")

# Form to add new data
with st.form("add_expense"):
    date = st.date_input("Date")
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0)
    type_ = st.selectbox("Type", ["Income", "Expense"])
    submitted = st.form_submit_button("Add")

    if submitted:
        res = supabase.table("expenses").insert({
            "date": str(date),
            "category": category,
            "amount": amount,
            "type": type_
        }).execute()
        st.success("✅ Entry added!")

# Show dashboard
rows = supabase.table("expenses").select("*").execute()
df = rows.data

if df:
    import pandas as pd
    import plotly.express as px

    df = pd.DataFrame(df)
    st.dataframe(df)

    total_income = df[df["type"]=="Income"]["amount"].sum()
    total_expense = df[df["type"]=="Expense"]["amount"].sum()
    st.metric("💵 Total Income", total_income)
    st.metric("💸 Total Expense", total_expense)
    st.metric("📊 Balance", total_income - total_expense)

    fig = px.pie(df[df["type"]=="Expense"], names="category", values="amount",
                 title="Expenses by Category")
    st.plotly_chart(fig)
