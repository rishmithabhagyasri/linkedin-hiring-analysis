import streamlit as st
import pandas as pd
import plotly.express as px
import re
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LinkedIn Hiring Trends",
    page_icon="💼",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 38px;
    font-weight: 700;
    color: #0A66C2;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 18px;
    color: #555555;
    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 650;
    color: #222222;
    margin-top: 20px;
    margin-bottom: 10px;
}

div[data-testid="stMetric"] {
    background-color: white;
    border-radius: 12px;
    padding: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

div[data-testid="stMetricLabel"] {
    color: #555555;
}

div[data-testid="stMetricValue"] {
    color: #0A66C2;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/linkdin_Job_data.csv")

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Remove duplicate records
    df = df.drop_duplicates()

    return df


df = load_data()

# =========================================================
# CLEAN DATA
# =========================================================

df["work_type"] = df["work_type"].fillna("Unknown").astype(str)

df["company_name"] = (
    df["company_name"]
    .fillna("Unknown")
    .astype(str)
)

df["location"] = (
    df["location"]
    .fillna("Unknown")
    .astype(str)
)

df["job"] = (
    df["job"]
    .fillna("Unknown")
    .astype(str)
)

df["full_time_remote"] = (
    df["full_time_remote"]
    .fillna("Unknown")
    .astype(str)
)

df["applications_numeric"] = pd.to_numeric(
    df["no_of_application"],
    errors="coerce"
)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="dashboard-title">💼 LinkedIn Hiring Trends Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive Dashboard for LinkedIn Job Market Analysis'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# SIDEBAR - DYNAMIC FILTERS
# =========================================================

st.sidebar.title("🔍 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore hiring trends."
)

# ---------------------------------------------------------
# 1. JOB ROLE
# ---------------------------------------------------------

job_options = sorted(
    df["job"].dropna().unique()
)

selected_job = st.sidebar.selectbox(
    "👨‍💻 Job Role",
    ["All Job Roles"] + job_options
)

# Create temporary dataframe based on Job Role
sidebar_df = df.copy()

if selected_job != "All Job Roles":
    sidebar_df = sidebar_df[
        sidebar_df["job"] == selected_job
    ]


# ---------------------------------------------------------
# 2. LOCATION
# ---------------------------------------------------------

location_options = sorted(
    sidebar_df["location"].dropna().unique()
)

selected_location = st.sidebar.selectbox(
    "📍 Location",
    ["All Locations"] + location_options
)

# Apply selected location temporarily
if selected_location != "All Locations":
    sidebar_df = sidebar_df[
        sidebar_df["location"] == selected_location
    ]


# ---------------------------------------------------------
# 3. WORK TYPE
# ---------------------------------------------------------

work_options = sorted(
    sidebar_df["work_type"].dropna().unique()
)

selected_work = st.sidebar.selectbox(
    "💼 Work Type",
    ["All Work Types"] + work_options
)

# Apply selected work type temporarily
if selected_work != "All Work Types":
    sidebar_df = sidebar_df[
        sidebar_df["work_type"] == selected_work
    ]


# ---------------------------------------------------------
# 4. COMPANY
# ---------------------------------------------------------

company_options = sorted(
    sidebar_df["company_name"].dropna().unique()
)

selected_company = st.sidebar.selectbox(
    "🏢 Company",
    ["All Companies"] + company_options
)


# ---------------------------------------------------------
# SIDEBAR INFORMATION
# ---------------------------------------------------------

st.sidebar.divider()

st.sidebar.info(
    "Select filters to dynamically explore the dataset."
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if selected_location != "All Locations":

    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]

if selected_work != "All Work Types":

    filtered_df = filtered_df[
        filtered_df["work_type"] == selected_work
    ]

if selected_company != "All Companies":

    filtered_df = filtered_df[
        filtered_df["company_name"] == selected_company
    ]
if selected_job != "All Job Roles":

    filtered_df = filtered_df[
        filtered_df["job"] == selected_job
    ]

# =========================================================
# HIRING OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📊 Hiring Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Job Records",
        f"{len(filtered_df):,}"
    )

with col2:

    st.metric(
        "Total Companies",
        f"{filtered_df['company_name'].nunique():,}"
    )

with col3:

    st.metric(
        "Total Locations",
        f"{filtered_df['location'].nunique():,}"
    )

with col4:

    st.metric(
        "Total Job Roles",
        f"{filtered_df['job'].nunique():,}"
    )

# =========================================================
# APPLICATION STATISTICS
# =========================================================

st.markdown(
    '<div class="section-title">📈 Application Statistics</div>',
    unsafe_allow_html=True
)

app_col1, app_col2, app_col3 = st.columns(3)

total_applications = filtered_df[
    "applications_numeric"
].sum()

average_applications = filtered_df[
    "applications_numeric"
].mean()

maximum_applications = filtered_df[
    "applications_numeric"
].max()

with app_col1:

    st.metric(
        "Total Applications",
        f"{total_applications:,.0f}"
        if pd.notna(total_applications)
        else "N/A"
    )

with app_col2:

    st.metric(
        "Average Applications",
        f"{average_applications:,.1f}"
        if pd.notna(average_applications)
        else "N/A"
    )

with app_col3:

    st.metric(
        "Maximum Applications",
        f"{maximum_applications:,.0f}"
        if pd.notna(maximum_applications)
        else "N/A"
    )

# =========================================================
# TOP JOB ROLES + TOP COMPANIES
# =========================================================

st.divider()

left_col, right_col = st.columns(2)

# ---------------- TOP JOB ROLES ----------------

with left_col:

    st.subheader("👨‍💻 Top 10 Job Roles")

    top_jobs = (
        filtered_df["job"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_jobs.columns = [
        "Job Role",
        "Job Postings"
    ]

    fig_jobs = px.bar(
        top_jobs,
        x="Job Postings",
        y="Job Role",
        orientation="h",
        text="Job Postings"
    )

    fig_jobs.update_layout(
        height=450,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(
        fig_jobs,
        width="stretch"
    )

# ---------------- TOP COMPANIES ----------------

with right_col:

    st.subheader("🏢 Top 10 Companies")

    top_companies = (
        filtered_df["company_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_companies.columns = [
        "Company",
        "Job Postings"
    ]

    fig_companies = px.bar(
        top_companies,
        x="Company",
        y="Job Postings",
        text="Job Postings"
    )

    fig_companies.update_layout(
        height=450,
        xaxis_tickangle=-45,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(
        fig_companies,
        width="stretch"
    )

# =========================================================
# TOP LOCATIONS + WORK TYPE
# =========================================================

left_col, right_col = st.columns(2)

# ---------------- TOP LOCATIONS ----------------

with left_col:

    st.subheader("📍 Top 10 Job Locations")

    top_locations = (
        filtered_df["location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_locations.columns = [
        "Location",
        "Job Postings"
    ]

    fig_locations = px.bar(
        top_locations,
        x="Job Postings",
        y="Location",
        orientation="h",
        text="Job Postings"
    )

    fig_locations.update_layout(
        height=450,
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(
        fig_locations,
        width="stretch"
    )

# ---------------- WORK TYPE ----------------

with right_col:

    st.subheader("🏠 Work Type Distribution")

    work_distribution = (
        filtered_df["work_type"]
        .value_counts()
        .reset_index()
    )

    work_distribution.columns = [
        "Work Type",
        "Job Postings"
    ]

    fig_work = px.pie(
        work_distribution,
        names="Work Type",
        values="Job Postings",
        hole=0.4
    )

    fig_work.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(
        fig_work,
        width="stretch"
    )

# =========================================================
# EMPLOYMENT / EXPERIENCE
# =========================================================

st.divider()

st.subheader("🎓 Employment / Experience Categories")

experience_distribution = (
    filtered_df["full_time_remote"]
    .value_counts()
    .head(10)
    .reset_index()
)

experience_distribution.columns = [
    "Category",
    "Job Postings"
]

fig_experience = px.bar(
    experience_distribution,
    x="Job Postings",
    y="Category",
    orientation="h",
    text="Job Postings"
)

fig_experience.update_layout(
    height=450,
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(
    fig_experience,
    width="stretch"
)

# =========================================================
# APPLICATION DISTRIBUTION
# =========================================================

st.subheader("📝 Job Application Distribution")

application_data = filtered_df[
    "applications_numeric"
].dropna()

if len(application_data) > 0:

    fig_applications = px.histogram(
        application_data,
        x="applications_numeric",
        nbins=20
    )

    fig_applications.update_layout(
        height=400,
        xaxis_title="Number of Applications",
        yaxis_title="Number of Job Posts"
    )

    st.plotly_chart(
        fig_applications,
        width="stretch"
    )

else:

    st.info(
        "Application data is not available."
    )

# =========================================================
# LINKEDIN FOLLOWERS ANALYSIS
# =========================================================

st.divider()

st.subheader("👥 LinkedIn Followers Analysis")

# Convert LinkedIn follower values into numeric format
def convert_followers(value):

    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    # Remove the word "followers"
    value = value.replace("followers", "").strip()

    # Remove commas
    value = value.replace(",", "")

    try:
        if value.endswith("m"):
            return float(value[:-1]) * 1_000_000

        elif value.endswith("k"):
            return float(value[:-1]) * 1_000

        elif value.endswith("b"):
            return float(value[:-1]) * 1_000_000_000

        else:
            return float(value)

    except:
        return None


followers_data = (
    filtered_df["linkedin_followers"]
    .apply(convert_followers)
    .dropna()
)

if len(followers_data) > 0:

    # Calculate follower statistics
    average_followers = followers_data.mean()
    maximum_followers = followers_data.max()
    minimum_followers = followers_data.min()

    # Display statistics
    follower_col1, follower_col2, follower_col3 = st.columns(3)

    with follower_col1:
        st.metric(
            "Average Followers",
            f"{average_followers:,.0f}"
        )

    with follower_col2:
        st.metric(
            "Maximum Followers",
            f"{maximum_followers:,.0f}"
        )

    with follower_col3:
        st.metric(
            "Minimum Followers",
            f"{minimum_followers:,.0f}"
        )

    # Followers distribution
    fig_followers = px.histogram(
        followers_data,
        nbins=20,
        title="Distribution of LinkedIn Followers"
    )

    fig_followers.update_layout(
        height=400,
        xaxis_title="LinkedIn Followers",
        yaxis_title="Number of Job Posts"
    )

    st.plotly_chart(
        fig_followers,
        width="stretch"
    )

else:

    st.info(
        "LinkedIn follower data is not available "
        "for the selected filters."
    )
    
    
# =========================================================
# JOB DATA TABLE
# =========================================================

st.divider()

st.subheader("📋 Job Data Table with Filters")

# Prepare table data
table_df = filtered_df.copy()

# Create Applications column
if "applications_numeric" in table_df.columns:
    table_df["Applies"] = table_df["applications_numeric"]

# Select and rename columns
table_columns = [
    "job",
    "company_name",
    "location",
    "work_type",
    "full_time_remote",
    "Applies"
]

table_df = table_df[
    [col for col in table_columns if col in table_df.columns]
].copy()

table_df = table_df.rename(
    columns={
        "job": "Job Title",
        "company_name": "Company",
        "location": "Location",
        "work_type": "Work Type",
        "full_time_remote": "Employment / Experience"
    }
)

st.caption(
    f"Showing {min(10, len(table_df))} of "
    f"{len(table_df):,} matching job postings"
)

st.dataframe(
    table_df.head(10),
    use_container_width=True,
    hide_index=True
)
# =========================================================
# DOWNLOAD FILTERED DATA
# =========================================================

st.divider()

st.subheader("📥 Download Filtered Data")

# Create a clean copy for download
download_df = filtered_df.copy()

# Remove technical analysis column
if "applications_numeric" in download_df.columns:
    download_df = download_df.drop(
        columns=["applications_numeric"]
    )

csv_data = download_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download CSV",
    data=csv_data,
    file_name="filtered_linkedin_hiring_data.csv",
    mime="text/csv"
)

st.caption(
    f"Download contains {len(download_df):,} filtered job records."
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "LinkedIn Hiring Trends Analysis | "
    "Python • Pandas • Plotly • Streamlit"
)