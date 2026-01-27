# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from customer_database import DBConnection, CustomerDatabase
import os
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Enterprise AI Analytics",
    page_icon="📈",
    layout="wide"
)

# --- PREMIUM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="ViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }

    .main {
        background-color: #0f172a;
    }

    /* Metric Cards */
    [data-testid="stMetricValue"] {
        color: #3b82f6;
        font-weight: 700;
        font-size: 2.5rem !important;
    }

    .card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
    }

    h1, h2, h3 {
        color: white !important;
        font-weight: 700 !important;
    }

    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LAYER ---
db = CustomerDatabase()

def load_analytics_data():
    with DBConnection(db.db_url) as conn:
        query = "SELECT * FROM conversations"
        df = pd.read_sql_query(query, conn)
        
        # Data Cleanup
        if not df.empty:
            df['start_time'] = pd.to_datetime(df['start_time'])
            # Mock some data if DB is small for demonstration
            if len(df) < 5:
                mock_data = {
                    'conversation_id': [f'MOCK-{i}' for i in range(20)],
                    'customer_id': ['C1', 'C2', 'C1', 'GUEST', 'C2'] * 4,
                    'start_time': [datetime.now() - timedelta(hours=i) for i in range(20)],
                    'resolved_status': [1, 1, 0, 1, 1] * 4,
                    'final_sentiment': ['positive', 'neutral', 'negative', 'positive', 'neutral'] * 4,
                    'final_priority': ['low', 'medium', 'high', 'urgent', 'medium'] * 4,
                    'total_tokens': [450, 320, 890, 120, 540] * 4,
                    'cost_estimate': [0.0001, 0.00008, 0.0004, 0.00002, 0.00012] * 4
                }
                df = pd.concat([df, pd.DataFrame(mock_data)])
        return df

df = load_analytics_data()

# --- HEADER ---
st.title("🚀 AI Agent Enterprise Insights")
st.markdown("Real-time monitoring and ROI tracking for your LangGraph Workforce")
st.markdown("---")

if df.empty:
    st.warning("No conversation data available yet. Start some chats to see analytics!")
    st.stop()

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_convs = len(df)
    st.metric("Total Conversations", f"{total_convs}", "+12%")

with col2:
    success_rate = (df['resolved_status'].sum() / total_convs) * 100
    st.metric("Resolution Rate", f"{success_rate:.1f}%", "+5%")

with col3:
    avg_tokens = df['total_tokens'].mean()
    st.metric("Avg Utility / Session", f"{int(avg_tokens)} tkn", "-2%")

with col4:
    total_cost = df['cost_estimate'].sum()
    st.metric("LCO (Total Cost)", f"${total_cost:.4f}", "-$0.02", delta_color="inverse")

st.markdown("---")

# --- INTERACTIVE CHARTS ---
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.subheader("📈 Conversation Volume (Hourly)")
    fig_volume = px.line(
        df.sort_values('start_time'), 
        x='start_time', 
        y='total_tokens',
        title="Token Utilization Over Time",
        template="plotly_dark",
        color_discrete_sequence=['#3b82f6']
    )
    st.plotly_chart(fig_volume, use_container_width=True)

with row1_col2:
    st.subheader("🎭 Sentiment Distribution")
    fig_sentiment = px.pie(
        df, 
        names='final_sentiment', 
        hole=0.6,
        color='final_sentiment',
        color_discrete_map={'positive': '#10b981', 'neutral': '#64748b', 'negative': '#ef4444'},
        template="plotly_dark"
    )
    st.plotly_chart(fig_sentiment, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("🎯 Specialist Workload")
    # Using 'final_priority' as a proxy for specialist complexity for demo
    fig_priority = px.bar(
        df, 
        x='final_priority', 
        color='final_priority',
        template="plotly_dark",
        labels={'count': 'Conversations'},
        title="Inquiry Intensity by Priority"
    )
    st.plotly_chart(fig_priority, use_container_width=True)

with row2_col2:
    st.subheader("📋 Recent High-Value activity")
    st.dataframe(
        df[['conversation_id', 'customer_id', 'final_sentiment', 'final_priority', 'cost_estimate']]
        .sort_values('cost_estimate', ascending=False)
        .head(10),
        use_container_width=True
    )

# --- FOOTER ---
st.markdown("---")
st.caption("AI Enterprise Dashboard | Optimized for LangGraph | Connection: WAL-Active")
