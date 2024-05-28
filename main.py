import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import calendar
from datetime import datetime


incomes = ["Salary","Blog","Other Income"]
expenses = ["Rent","Utilities","Groceries","Car","Other Expenses","Savings"]
currency = "usd"

pageTitle = "Census Data Standardisation"
pageIcon= ":money_with_wings:"
layout = "centered"


st.set_page_config(page_title=pageTitle, page_icon=pageIcon, layout=layout)
st.title(pageTitle +"  "+pageIcon)

years = [datetime.today().year,datetime.today().year +1, datetime.today().year -1]
months=list(calendar.month_name[1:])

hide_st_style = """
                <style>
                #MainMenu {visibility:hidden;}
                header {visibility:hidden;}
                footer {visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)

# with st.sidebar:
selected = option_menu(
    menu_title=None,
    options = ["Data Entry", "Data Visualization"],
    icons = ["pencil-fill","bar-chart-fill"],
    orientation = "horizontal"
)

if selected =="Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month:",months, key="month")
        col1.selectbox("Select Year:",years, key="year")

        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value= 0, step= 10, format="%i", key=income)

        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0,step=10, format="%i",key = expense)

        with st.expander("Comments"):
            comment = st.text_area("",placeholder="Enter comments here.......")



        submitted = st.form_submit_button("Save Data")
        if submitted:
            period= str(st.session_state["year"]) + " _ "+str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}

            st.write(f"Your Income: {incomes}")
            st.write(f"Your Expense: {expenses}")
            st.write("Data Saved !")

if selected =="Data Visualization":
    st.header("Data Visualization")
    with st.form("saved periods"):
        period = st.selectbox("Selected Period:", ["2024_January"])
        submitted = st.form_submit_button("Plot Period")

        if submitted:
            comments = "Hi ..........."
            incomes = {'Salary': 40, 'Blog': 50, 'Other Income': 60}
            expenses = {'Rent': 90, 'Utilities': 60, 'Groceries': 50, 'Car': 0, 'Other Expenses': 0, 'Savings': 70}

            total_incomes = sum(incomes.values())
            total_expenses = sum(expenses.values())
            remaining_budget = total_incomes - total_expenses
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income",f"{total_incomes} {currency}")
            col2.metric("Total Expense", f"{total_expenses} {currency}")
            col3.metric("Comments:",f" {comments}")

            label = list(incomes.keys()) +["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes) *len(incomes)] + [label.index(expense) for expense in expenses]
            value =list(incomes.values()) + list(expenses.values())


            link = dict(source = source, target = target, value = value)
            node = dict(label = label , pad = 20, thickness= 30, color="#E694FF")
            data = go.Sankey(link = link, node=node)


            fig = go.Figure(data)
            fig.update_layout(margin = dict(l=0,r=0,t=5,b=5))
            st.plotly_chart(fig, use_container_width= True)





