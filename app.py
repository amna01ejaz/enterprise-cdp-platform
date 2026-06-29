import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sqlite3
import streamlit_authenticator as stauth
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =====================================================================
# 1. SYSTEM INTERFACE CONFIGURATION
# =====================================================================
st.set_page_config(page_title="Enterprise Predictive CDP", layout="wide")

# Custom UI Styling Blocks
st.markdown("""
<style>
    .main-title { font-size:38px !important; font-weight: 800; color: #1E293B; margin-bottom: 5px; }
    .subtitle { font-size:16px !important; color: #64748B; margin-bottom: 25px; }
    .crud-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)
# =====================================================================
# 2. USER SECURITY & CONFIGURATION LAYER
# =====================================================================
names = ['Amna Ejaz', 'Technical Recruiter']
usernames = ['amnaeiaz', 'recruiter']
passwords = ['admin123', 'hireme2026']

# Security Framework: Hashing passwords using secure cryptographic bcrypt logic
hashed_passwords = stauth.Hasher(passwords).generate()

# Explicit mapping structured specifically to match the library's internal models
config_credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0],
            "email": "amna@enterprise.com"
        },
        usernames[1]: {
            "name": names[1],
            "password": hashed_passwords[1],
            "email": "recruiter@enterprise.com"
        }
    }
}

# Instantiating the authentication state module with explicit parameter assignments
authenticator = stauth.Authenticate(
    credentials=config_credentials,
    cookie_name="cdp_cookie_session",
    cookie_key="auth_key_secure_string",
    cookie_expiry_days=1
)

# Render login window interface frame component (Note: updated signature pattern)
name, authentication_status, username = authenticator.login(location='main')
    # =====================================================================
    # 3. RELATIONAL DATABASE LAYER (SQLITE CONFIG)
    # =====================================================================
def get_db_connection():
        # Establishing an active binary connection to our relational SQLite ledger file
        conn = sqlite3.connect('enterprise_cdp.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_database_schema():
        # Schema Design: Creating our table structure with strict structural constraints
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id TEXT PRIMARY KEY,
                    age INTEGER,
                    annual_spend REAL,
                    purchase_frequency INTEGER
                )
            ''')
            # Seed Pipeline: If the file is completely fresh, inject 100 base records automatically
            cursor = conn.execute('SELECT COUNT(*) FROM customers')
            if cursor.fetchone()[0] == 0:
                np.random.seed(42)
                for i in range(100):
                    conn.execute(
                        'INSERT INTO customers VALUES (?, ?, ?, ?)',
                        (f"CUST-{1000+i}", int(np.random.randint(18, 65)), float(np.random.uniform(500, 8000)), int(np.random.randint(1, 40)))
                    )
                conn.commit()

    # Run DB configuration routine
init_database_schema()

    # =====================================================================
    # 4. PLATFORM HEADER DISPLAY
    # =====================================================================
st.markdown("<div class='main-title'>🚀 Enterprise Customer Data Platform (CDP)</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Production Dashboard with Relational SQL CRUD, Secure User Access Gates, and Live ML Groupings.</div>", unsafe_allow_html=True)
st.markdown("---")

    # App Domain Selector Menu
app_mode = st.sidebar.selectbox("Application Domain Viewport", ["📊 Data Hub & ML Engine", "⚙️ Database Matrix Management (CRUD)"])

    # Automated ETL Routine: Extracting data from SQL and loading cleanly into memory
def load_clean_etl_dataframe():
        with get_db_connection() as conn:
            return pd.read_sql_query("SELECT * FROM customers", conn)

    # =====================================================================
    # VIEWPORT 1: DATA ANALYTICS & INTERACTIVE AI MODELLING
    # =====================================================================
if app_mode == "📊 Data Hub & ML Engine":
        df = load_clean_etl_dataframe()
        
        if df.empty:
            st.info("The relational enterprise database is currently empty. Head over to the CRUD panel to generate data records.")
        else:
            st.subheader("🤖 Live Machine Learning Segmentation Cluster Control")
            st.markdown("Adjust the slider to change the mathematical **k-value** of the active Scikit-Learn K-Means algorithm:")
            
            k_value = st.slider("Target Clusters (k Centroids):", 2, 5, 3)
            
            # Feature Selection Matrix
            features = ['age', 'annual_spend', 'purchase_frequency']
            X = df[features]
            
            # Crucial ML step: Normalizing feature scales so spend range doesn't break distance math
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Compute Unsupervised Clusters live on user interaction
            kmeans_engine = KMeans(n_clusters=k_value, random_state=42, n_init=10)
            df['Cluster_Profile'] = kmeans_engine.fit_predict(X_scaled)
            df['Cluster_Profile'] = df['Cluster_Profile'].apply(lambda x: f"Behavioral Cluster Segment {x+1}")
            
            # Interactive Chart Display
            fig = px.scatter(df, x='annual_spend', y='purchase_frequency', color='Cluster_Profile',
                             size='age', hover_name='customer_id', 
                             labels={'annual_spend': 'Annual Revenue Generation ($)', 'purchase_frequency': 'Purchase Iterations'},
                             title="Dynamic Customer Vector Placement Space")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📋 Core Relational Database Registry View")
            st.dataframe(df, use_container_width=True)

    # =====================================================================
    # VIEWPORT 2: DATA REGISTRY STRUCTURAL CRUD MANAGER
    # =====================================================================
elif app_mode == "⚙️ Database Matrix Management (CRUD)":
        st.subheader("✏️ Live Relational Database Control Console")
        st.markdown("Execute safe Create, Read, Update, and Delete commands against your production SQLite transaction ledger.")
        st.markdown("")
        
        col_c, col_d = st.columns(2)
        
        with col_c:
            st.markdown("<div class='crud-box'>", unsafe_allow_html=True)
            st.markdown("### 📥 Create / Update Profile Record")
            input_id = st.text_input("Customer Database Reference ID (Primary Key):", value="CUST-1500")
            input_age = st.number_input("Profile Age Value:", min_value=18, max_value=90, value=28)
            input_spend = st.number_input("Recorded Net Annual Spend ($):", min_value=0.0, value=2450.0)
            input_freq = st.number_input("Total Transacted Invoices Counter:", min_value=1, value=15)
            
            if st.button("Commit Record Entry to Database"):
                with get_db_connection() as conn:
                    # SQL logic handles inserting a fresh record or replacing an old record gracefully
                    conn.execute("""
                        INSERT OR REPLACE INTO customers (customer_id, age, annual_spend, purchase_frequency) 
                        VALUES (?, ?, ?, ?)
                    """, (input_id, input_age, input_spend, input_freq))
                    conn.commit()
                st.success(f"Database sync successful! Processed structural record entity for UUID: {input_id}")
                st.markdown("</div>", unsafe_allow_html=True)

        with col_d:
            st.markdown("<div class='crud-box'>", unsafe_allow_html=True)
            st.markdown("### 🗑️ Terminate Profile Record (Delete)")
            
            # Fetch active keys to display cleanly inside our selection dropdown
            df_current = load_clean_etl_dataframe()
            
            if df_current.empty:
                st.info("No records are currently present within the SQL system schema storage channels.")
            else:
                delete_target = st.selectbox("Choose Target Profile ID for Permanent Deletion:", df_current['customer_id'].tolist())
                
                if st.button("Execute Record Purge Command", type="primary"):
                    with get_db_connection() as conn:
                        conn.execute("DELETE FROM customers WHERE customer_id = ?", (delete_target,))
                        conn.commit()
                    st.warning(f"Permanently dropped profile row reference node: {delete_target}")
                    # Re-trigger viewport refresh to synchronize UI display immediately
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)