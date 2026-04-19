import os
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# -----------------------------
# Optional OpenAI import
# -----------------------------
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Business Operations System",
    page_icon="💼",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    .main {
        background-color: #f6f8fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        color: #16213e;
        font-weight: 700;
    }

    .section-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #16213e;
        margin-bottom: 0.35rem;
    }

    .section-subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.25rem;
    }

    .soft-panel-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #16213e;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }

    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        min-height: 130px;
        margin-bottom: 12px;
    }

    .kpi-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 0.65rem;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #16213e;
        line-height: 1.1;
        word-break: break-word;
    }

    .kpi-positive {
        color: #0f9d58;
    }

    .kpi-negative {
        color: #c62828;
    }

    .soft-panel {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        margin-bottom: 20px;
    }

    .chat-user-wrap {
        text-align: right;
        margin-bottom: 10px;
    }

    .chat-user {
        display: inline-block;
        background: #16213e;
        color: white;
        padding: 12px 16px;
        border-radius: 16px 16px 4px 16px;
        max-width: 82%;
        font-size: 0.98rem;
    }

    .chat-bot-wrap {
        text-align: left;
        margin-bottom: 10px;
    }

    .chat-bot {
        display: inline-block;
        background: #e9eef7;
        color: #16213e;
        padding: 12px 16px;
        border-radius: 16px 16px 16px 4px;
        max-width: 82%;
        font-size: 0.98rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #16213e 0%, #1f4068 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1.2rem;
        font-weight: 700;
    }

    .stButton > button:hover {
        color: white;
        opacity: 0.95;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213e 0%, #1f4068 100%);
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# FILES
# =========================================================
SALES_FILE = "sales.csv"
EXPENSES_FILE = "expenses.csv"
PAYROLL_FILE = "payroll.csv"

# =========================================================
# OPENAI SETUP
# =========================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

client = None
if OpenAI is not None and OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        client = None

# =========================================================
# HELPERS
# =========================================================
def load_csv_safely(file_path: str, columns: list[str]) -> pd.DataFrame:
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return df
    try:
        return pd.read_csv(file_path)
    except Exception:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return df


def save_df(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def render_kpi_card(title: str, value: str, value_class: str = "") -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value {value_class}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def build_business_context(
    total_sales: float,
    total_expenses: float,
    total_payroll: float,
    profit_loss: float,
    selected_month: str,
    sales_filtered: pd.DataFrame,
    expenses_filtered: pd.DataFrame,
    payroll_df: pd.DataFrame
) -> str:
    sales_count = len(sales_filtered)
    expense_count = len(expenses_filtered)
    payroll_count = len(payroll_df)

    top_expense = 0.0
    top_expense_category = "N/A"
    if not expenses_filtered.empty:
        idx = expenses_filtered["Amount"].astype(float).idxmax()
        top_expense = float(expenses_filtered.loc[idx, "Amount"])
        top_expense_category = str(expenses_filtered.loc[idx, "Category"])

    top_sale = 0.0
    top_sale_item = "N/A"
    if not sales_filtered.empty:
        idx = sales_filtered["Amount"].astype(float).idxmax()
        top_sale = float(sales_filtered.loc[idx, "Amount"])
        top_sale_item = str(sales_filtered.loc[idx, "Item"])

    return f"""
Business reporting month: {selected_month}
Total sales: £{total_sales:,.2f}
Total expenses: £{total_expenses:,.2f}
Total payroll: £{total_payroll:,.2f}
Profit/loss: £{profit_loss:,.2f}

Number of sales records: {sales_count}
Number of expense records: {expense_count}
Number of payroll records: {payroll_count}

Top sale item: {top_sale_item} (£{top_sale:,.2f})
Top expense category: {top_expense_category} (£{top_expense:,.2f})
""".strip()


def get_fallback_response(
    question: str,
    total_sales: float,
    total_expenses: float,
    total_payroll: float,
    profit_loss: float
) -> str:
    q = question.lower().strip()

    if "profit" in q or "loss" in q:
        if profit_loss < 0:
            return (
                f"Your business is running at a loss of £{abs(profit_loss):,.2f}. "
                f"This is because expenses (£{total_expenses:,.2f}) and payroll (£{total_payroll:,.2f}) "
                f"are too high compared to sales (£{total_sales:,.2f})."
            )
        return f"Your business is profitable with £{profit_loss:,.2f} profit."

    if "sales" in q or "revenue" in q:
        return (
            f"Your total sales are £{total_sales:,.2f}. "
            f"To improve sales, focus on better offers, repeat customers, and stronger promotion."
        )

    if "expense" in q or "expenses" in q or "cost" in q:
        return (
            f"Your total expenses are £{total_expenses:,.2f}. "
            f"Review high-cost areas and cut unnecessary spending."
        )

    if "payroll" in q or "salary" in q or "staff" in q:
        return (
            f"Your total payroll cost is £{total_payroll:,.2f}. "
            f"If payroll is too high relative to sales, profit will stay under pressure."
        )

    if "summary" in q or "overview" in q or "status" in q:
        return (
            f"Summary: Sales £{total_sales:,.2f}, Expenses £{total_expenses:,.2f}, "
            f"Payroll £{total_payroll:,.2f}, Profit/Loss £{profit_loss:,.2f}."
        )

    if "improve" in q or "advice" in q or "recommend" in q or "tips" in q:
        advice = []
        if total_expenses > total_sales and total_sales > 0:
            advice.append("reduce unnecessary expenses")
        if total_sales > 0 and total_payroll > total_sales * 0.5:
            advice.append("review payroll costs")
        if profit_loss < 0:
            advice.append("increase sales and improve margin")
        if total_sales <= 0:
            advice.append("focus on getting more sales first")

        if advice:
            return "To improve the business, you should " + ", ".join(advice) + "."
        return "Your business looks stable. Keep monitoring sales, expenses, and payroll."

    return "I can help with questions about sales, expenses, payroll, profit, and business performance."


def ask_gpt_business_assistant(question: str, context: str) -> str:
    if not client:
        return "GPT is unavailable right now. The app will use the built-in business assistant instead."

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions="""
You are a senior business consultant.

Your job:
- Analyze business data
- Give clear, structured answers
- Be practical and actionable
- Explain why performance is strong or weak
- Suggest step-by-step improvements
- Keep answers concise but helpful
""",
            input=f"""
Business Data:
{context}

User Question:
{question}

Give a structured and practical answer.
"""
        )
        return response.output_text.strip()

    except Exception as e:
        error_text = str(e).lower()

        if "insufficient_quota" in error_text or "429" in error_text:
            return (
                "GPT is temporarily unavailable because the API account has no quota left. "
                "Please check OpenAI billing and usage. For now, the built-in business assistant can still help."
            )

        if "invalid_api_key" in error_text or "incorrect api key" in error_text or "401" in error_text:
            return "The OpenAI API key is invalid. Please check your API key and try again."

        return f"GPT is currently unavailable. Error: {e}"


def generate_gpt_insight(context: str) -> str:
    if not client:
        return "GPT insight is unavailable right now. Add a valid API key to use this feature."

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions="""
You are a senior business analyst.
Give one short insight paragraph based on the business data.
Explain the main issue first, then suggest one or two actions.
""",
            input=f"Business context:\n{context}"
        )
        return response.output_text.strip()

    except Exception as e:
        error_text = str(e).lower()

        if "insufficient_quota" in error_text or "429" in error_text:
            return "GPT insight is unavailable because the API account has no quota left. Please check billing and usage."

        if "invalid_api_key" in error_text or "incorrect api key" in error_text or "401" in error_text:
            return "GPT insight is unavailable because the API key is invalid."

        return f"GPT insight is currently unavailable. Error: {e}"


# =========================================================
# LOAD DATA
# =========================================================
sales_df = load_csv_safely(SALES_FILE, ["Date", "Item", "Amount"])
expenses_df = load_csv_safely(EXPENSES_FILE, ["Date", "Category", "Amount"])
payroll_df = load_csv_safely(PAYROLL_FILE, ["Name", "Days Worked", "Pay Per Day", "Salary"])

if not sales_df.empty and "Date" in sales_df.columns:
    sales_df["Date"] = pd.to_datetime(sales_df["Date"], format="mixed", errors="coerce")

if not expenses_df.empty and "Date" in expenses_df.columns:
    expenses_df["Date"] = pd.to_datetime(expenses_df["Date"], format="mixed", errors="coerce")

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## Business Suite")
st.sidebar.markdown("Manage your business with smart analytics")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Sale", "Add Expense", "Payroll", "View Data"]
)

# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":
    st.markdown('<div class="section-title">Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Track sales, expenses, payroll, profit, and AI guidance in one place.</div>',
        unsafe_allow_html=True
    )

    all_months = []

    if not sales_df.empty and "Date" in sales_df.columns and sales_df["Date"].notna().any():
        all_months.extend(sales_df["Date"].dt.to_period("M").astype(str).unique().tolist())

    if not expenses_df.empty and "Date" in expenses_df.columns and expenses_df["Date"].notna().any():
        all_months.extend(expenses_df["Date"].dt.to_period("M").astype(str).unique().tolist())

    unique_months = sorted(list(set(all_months)))
    month_options = ["All Months"] + unique_months

    st.markdown('<div class="soft-panel-title">Select Reporting Month</div>', unsafe_allow_html=True)
    selected_month = st.selectbox("Choose Month", month_options)

    if selected_month == "All Months":
        sales_filtered = sales_df.copy()
        expenses_filtered = expenses_df.copy()
    else:
        sales_filtered = (
            sales_df[sales_df["Date"].dt.to_period("M").astype(str) == selected_month].copy()
            if not sales_df.empty and "Date" in sales_df.columns else sales_df.copy()
        )
        expenses_filtered = (
            expenses_df[expenses_df["Date"].dt.to_period("M").astype(str) == selected_month].copy()
            if not expenses_df.empty and "Date" in expenses_df.columns else expenses_df.copy()
        )

    total_sales = float(sales_filtered["Amount"].sum()) if not sales_filtered.empty else 0.0
    total_expenses = float(expenses_filtered["Amount"].sum()) if not expenses_filtered.empty else 0.0
    total_payroll = float(payroll_df["Salary"].sum()) if not payroll_df.empty else 0.0
    profit_loss = total_sales - total_expenses - total_payroll

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Total Sales", f"£{total_sales:,.2f}")
    with c2:
        render_kpi_card("Total Expenses", f"£{total_expenses:,.2f}")
    with c3:
        render_kpi_card("Total Payroll", f"£{total_payroll:,.2f}")
    with c4:
        profit_class = "kpi-negative" if profit_loss < 0 else "kpi-positive"
        render_kpi_card("Profit / Loss", f"£{profit_loss:,.2f}", profit_class)

    # Alerts
    st.markdown('<div class="soft-panel-title">Smart Business Alerts</div>', unsafe_allow_html=True)

    alerts = []
    if total_sales == 0:
        alerts.append("No sales recorded. Business is not generating revenue.")
    if profit_loss < 0:
        alerts.append("Business is running at a loss. Check expenses and payroll.")
    if total_sales > 0 and total_expenses > total_sales * 0.7:
        alerts.append("Expenses are very high compared to sales.")
    if total_sales > 0 and total_payroll > total_sales * 0.5:
        alerts.append("Payroll cost is too high compared to sales.")
    if not expenses_filtered.empty:
        max_expense = float(expenses_filtered["Amount"].max())
        if max_expense > 500:
            alerts.append(f"High single expense detected: £{max_expense:,.2f}")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("All business metrics look healthy.")

    # AI Insight
    st.markdown('<div class="soft-panel-title">AI Business Insight</div>', unsafe_allow_html=True)

    business_context = build_business_context(
        total_sales=total_sales,
        total_expenses=total_expenses,
        total_payroll=total_payroll,
        profit_loss=profit_loss,
        selected_month=selected_month,
        sales_filtered=sales_filtered,
        expenses_filtered=expenses_filtered,
        payroll_df=payroll_df
    )

    if "latest_gpt_insight" not in st.session_state:
        st.session_state.latest_gpt_insight = ""

    if st.button("Generate GPT Insight"):
        st.session_state.latest_gpt_insight = generate_gpt_insight(business_context)

    if st.session_state.latest_gpt_insight:
        st.info(st.session_state.latest_gpt_insight)

    # GPT Chat Assistant
    st.markdown('<div class="soft-panel-title">GPT Business Chat Assistant</div>', unsafe_allow_html=True)
    st.write("Ask questions about sales, expenses, payroll, profit, or how to improve the business.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input(
        "Ask your question",
        placeholder="Example: How can I improve profit?",
        key="chat_input"
    )

    b1, b2 = st.columns([1, 1])

    with b1:
        if st.button("Send to GPT"):
            if user_input.strip():
                st.session_state.chat_history.append(("user", user_input))

                if client:
                    reply = ask_gpt_business_assistant(user_input, business_context)
                else:
                    reply = get_fallback_response(
                        question=user_input,
                        total_sales=total_sales,
                        total_expenses=total_expenses,
                        total_payroll=total_payroll,
                        profit_loss=profit_loss
                    )

                st.session_state.chat_history.append(("bot", reply))

    with b2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []

    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(
                f'<div class="chat-user-wrap"><div class="chat-user">{message}</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-bot-wrap"><div class="chat-bot">{message}</div></div>',
                unsafe_allow_html=True
            )

    # Charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="soft-panel-title">Sales Trend</div>', unsafe_allow_html=True)
        if not sales_filtered.empty and sales_filtered["Date"].notna().any():
            sales_chart_data = sales_filtered.groupby(sales_filtered["Date"].dt.date)["Amount"].sum()
            fig, ax = plt.subplots()
            sales_chart_data.plot(kind="line", marker="o", ax=ax)
            ax.set_xlabel("Date")
            ax.set_ylabel("Sales Amount")
            ax.set_title("Daily Sales")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No sales data available for the selected month.")

    with col_right:
        st.markdown('<div class="soft-panel-title">Expense Trend</div>', unsafe_allow_html=True)
        if not expenses_filtered.empty and expenses_filtered["Date"].notna().any():
            expense_chart_data = expenses_filtered.groupby(expenses_filtered["Date"].dt.date)["Amount"].sum()
            fig, ax = plt.subplots()
            expense_chart_data.plot(kind="line", marker="o", ax=ax)
            ax.set_xlabel("Date")
            ax.set_ylabel("Expense Amount")
            ax.set_title("Daily Expenses")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No expense data available for the selected month.")

    # Recent tables
    r1, r2 = st.columns(2)

    with r1:
        st.markdown('<div class="soft-panel-title">Recent Sales</div>', unsafe_allow_html=True)
        if not sales_filtered.empty:
            display_sales = sales_filtered.copy()
            display_sales["Date"] = display_sales["Date"].dt.date
            st.dataframe(
                display_sales.sort_values("Date", ascending=False).head(5),
                use_container_width=True
            )
        else:
            st.write("No sales records for the selected month.")

    with r2:
        st.markdown('<div class="soft-panel-title">Recent Expenses</div>', unsafe_allow_html=True)
        if not expenses_filtered.empty:
            display_expenses = expenses_filtered.copy()
            display_expenses["Date"] = display_expenses["Date"].dt.date
            st.dataframe(
                display_expenses.sort_values("Date", ascending=False).head(5),
                use_container_width=True
            )
        else:
            st.write("No expense records for the selected month.")

# =========================================================
# ADD SALE
# =========================================================
elif page == "Add Sale":
    st.markdown('<div class="section-title">Add Sale</div>', unsafe_allow_html=True)

    sale_date = st.date_input("Sale Date", value=date.today())
    sale_item = st.text_input("Item Name")
    sale_amount = st.number_input("Sale Amount", min_value=0.0, step=1.0)

    if st.button("Add Sale"):
        if sale_item.strip() == "":
            st.warning("Please enter an item name.")
        else:
            new_sale = pd.DataFrame([{
                "Date": sale_date,
                "Item": sale_item,
                "Amount": sale_amount
            }])
            sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
            save_df(sales_df, SALES_FILE)
            st.success("Sale added successfully.")

# =========================================================
# ADD EXPENSE
# =========================================================
elif page == "Add Expense":
    st.markdown('<div class="section-title">Add Expense</div>', unsafe_allow_html=True)

    expense_date = st.date_input("Expense Date", value=date.today())
    expense_category = st.text_input("Expense Category")
    expense_amount = st.number_input("Expense Amount", min_value=0.0, step=1.0)

    if st.button("Add Expense"):
        if expense_category.strip() == "":
            st.warning("Please enter an expense category.")
        else:
            new_expense = pd.DataFrame([{
                "Date": expense_date,
                "Category": expense_category,
                "Amount": expense_amount
            }])
            expenses_df = pd.concat([expenses_df, new_expense], ignore_index=True)
            save_df(expenses_df, EXPENSES_FILE)
            st.success("Expense added successfully.")

# =========================================================
# PAYROLL
# =========================================================
elif page == "Payroll":
    st.markdown('<div class="section-title">Payroll Management</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 1.2])

    with left:
        st.markdown('<div class="soft-panel-title">Add Employee Salary</div>', unsafe_allow_html=True)
        name = st.text_input("Employee Name")
        days_worked = st.number_input("Days Worked", min_value=0, step=1)
        pay_per_day = st.number_input("Pay Per Day (£)", min_value=0.0, step=1.0)

        salary = days_worked * pay_per_day
        st.info(f"Calculated Salary: £{salary:,.2f}")

        if st.button("Add Payroll"):
            if name.strip() == "":
                st.warning("Please enter employee name.")
            else:
                new_payroll = pd.DataFrame([{
                    "Name": name,
                    "Days Worked": days_worked,
                    "Pay Per Day": pay_per_day,
                    "Salary": salary
                }])
                payroll_df = pd.concat([payroll_df, new_payroll], ignore_index=True)
                save_df(payroll_df, PAYROLL_FILE)
                st.success("Employee salary added successfully.")

    with right:
        st.markdown('<div class="soft-panel-title">Payroll Records</div>', unsafe_allow_html=True)
        if not payroll_df.empty:
            st.dataframe(payroll_df, use_container_width=True)
            st.success(f"Total Payroll Cost: £{payroll_df['Salary'].sum():,.2f}")
        else:
            st.write("No payroll records yet.")

# =========================================================
# VIEW DATA
# =========================================================
elif page == "View Data":
    st.markdown('<div class="section-title">Data Records</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Sales Data", "Expense Data", "Payroll Data"])

    with tab1:
        if not sales_df.empty:
            display_sales = sales_df.copy()
            display_sales["Date"] = display_sales["Date"].dt.date
            st.dataframe(display_sales, use_container_width=True)
        else:
            st.write("No sales data available.")

    with tab2:
        if not expenses_df.empty:
            display_expenses = expenses_df.copy()
            display_expenses["Date"] = display_expenses["Date"].dt.date
            st.dataframe(display_expenses, use_container_width=True)
        else:
            st.write("No expense data available.")

    with tab3:
        if not payroll_df.empty:
            st.dataframe(payroll_df, use_container_width=True)
        else:
            st.write("No payroll data available.")