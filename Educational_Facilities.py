#import libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64

st.set_page_config(
    page_title=" Nigeria Educational Facilities Dashboard",
    page_icon="🏫",
    layout="wide"
)

def format_number(num):
        if num >= 1_000_000_000:
          return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
          return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
          return f"{num / 1_000:.1f}K"
        else:
          return str(num)

#load_dataset
@st.cache_data
def load_data():
    education = pd.read_csv("cleaned_educational-facilities-in-nigeria.csv")

    return education

education = load_data()

def main():

    st.sidebar.header("🏫 Nigeria Educational Facilities Dashboard")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter Options")

    facility_type_filter = st.sidebar.selectbox(
        "Select Facility Type:",
        options=["All Facility Type"] + sorted(education["facility_type_display"].unique().tolist())
    )

    management_filter = st.sidebar.selectbox(
        "Select Management:",
        options=["All Management"] + sorted(education["management"].unique().tolist())
    )

    state_filter = st.sidebar.selectbox(
        "Select State:",
        options=["All State"] + sorted(education["state"].unique().tolist())
    )


    #Filter Data
    
    filtered_data = education.copy()

    if facility_type_filter != "All Facility Type":
        filtered_data = filtered_data[
            filtered_data["facility_type_display"] == facility_type_filter
        ]

    if management_filter != "All Management":
        filtered_data = filtered_data[
            filtered_data["management"] == management_filter
        ]

    if state_filter != "All State":
        filtered_data = filtered_data[
            filtered_data["state"] == state_filter
        ]

    
    #Main Content
    
    st.title("🏫 Nigeria Educational Facilities Dashboard")
    st.markdown("---")

    if filtered_data.empty:
        st.warning("No data available for selected filters.")
    else:
        # KPI Calculations
        total_schools = len(filtered_data)
        total_students = filtered_data["total_students"].sum()
        avg_students = filtered_data["total_students"].mean()
        pct_electricity = filtered_data["phcn_electricity"].mean() * 100
        pct_water = filtered_data["improved_water_supply"].mean() * 100


        # KPI Display
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Schools 🏫", f"{total_schools:,}")
        col2.metric("Total Students 🧑‍🎓", format_number(total_students))
        col3.metric("Avg Students per School 🧑‍🎓", f"{avg_students:.2f}")
        col4.metric("% Of Schools with Electricity ⚡", f"{pct_electricity:.2f}%")
        col5.metric("% Of Schools with Improved Water Supply 🚰", f"{pct_water:.2f}%")


    st.markdown("---")

    st.subheader("School Type Distribution 🏫")
    school_counts = (
    filtered_data["facility_type_display"]
    .value_counts()
        .reset_index(name="count")
    )

    fig1 = px.bar(
        school_counts,
        x="facility_type_display",
        y="count",
        labels={"facility_type_display": "School Type", "count": "Number of Schools"},
        color="facility_type_display",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    st.subheader("Student Population Distribution 🧑‍🎓")
    fig2 = px.histogram(
                filtered_data,
                x="total_students",
                nbins=50,
                color_discrete_sequence=px.colors.sequential.Viridis
            )

    fig2.update_layout(height=450)
    st.plotly_chart(fig2, use_container_width=True)


    st.markdown("---")
    
    st.subheader("Public vs Private School Comparison 🏫")

    management_stats = (
        filtered_data.groupby("management")["total_students"]
        .mean()
        .reset_index()
    )

    fig3 = px.bar(
        management_stats,
        x="management",
        y="total_students",
        labels={"total_students": "Average Students"},
        color="management",
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    fig3.update_layout(height=450)
    st.plotly_chart(fig3, use_container_width=True)


    st.markdown("---")
    #chart visual
    st.subheader("Electricity availability ⚡")

    electricity_counts = (
        filtered_data["phcn_electricity"]
        .value_counts()
        .reset_index(name="count")
    )

    fig4 = px.pie(
        electricity_counts,
        names="phcn_electricity",
        values="count",
        color_discrete_sequence=px.colors.qualitative.Prism,
        hole=0.4
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Water and sanitation access 🚰")

    water_counts = (
        filtered_data["improved_water_supply"]
        .value_counts()
        .reset_index(name="count")
    )

    fig5 = px.pie(
        water_counts,
        names="improved_water_supply",
        values="count",
        color_discrete_sequence=px.colors.qualitative.Safe,
        hole=0.4
    )

    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.subheader("School Locations Map 🗺️")

    fig6 = px.scatter_mapbox(
    filtered_data,
    lat="latitude",
    lon="longitude",
    hover_name="facility_name",
    hover_data=["facility_type_display", "management"],
    zoom=5,
    height=600
)

    fig6.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig6, use_container_width=True)

    

    st.markdown("---")
    st.header("📊 Insights & Recommendations")
    

    st.markdown("### 🔍 Major Problems Identified")

    with st.expander("View Major Infrastructure Challenges"):
        st.markdown("""
    <div style="
        background-color:white;
        padding:15px;
        border-radius:10px;
        border:1px solid #ddd;
        color:black;
        font-size:16px;
    ">
    <ul>
        <li><b>Large percentage of schools lack electricity access most especially public schools.</b></li>
        <li><b>Poor access to improved sanitation facilities.</b></li>
        <li><b>Extremely high student-to-teacher ratios in public schools.</b></li>
        <li><b>Rural LGAs show significantly lower infrastructure quality.</b></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📍 Regions Needing Attention")

    with st.expander("View Regional Infrastructure Gaps"):
     st.markdown("""
    <div style="
        background-color:white;
        padding:15px;
        border-radius:10px;
        border:1px solid #ddd;
        color:black;
        font-size:16px;
    ">
     <li><b>Northern states show lower infrastructure development.
     <li><b>Certain LGAs have less than 30% electricity access.
     <li><b>High population states like Lagos and Kano show overcrowding.
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏛 Recommendations")

    with st.expander("View Policy & Development Recommendations"):
        st.markdown("""
    <div  style="
        background-color:white;
        padding:15px;
        border-radius:10px;
        border:1px solid #ddd;
        color:black;
        font-size:16px;
    ">
    <li><b>Government should prioritize rural electrification of schools.
    <li><b>NGOs should focus on sanitation infrastructure projects.
    <li><b>Teacher recruitment programs are needed in high-ratio states.
    <li><b>Infrastructure funding should be data-driven using this dashboard.
    </ul>
    </div>
    """, unsafe_allow_html=True)
        

    st.markdown("---")
    st.subheader("⬇ Download Filtered Data")

    csv = filtered_data.to_csv(index=False).encode("utf-8")

    st.download_button(
    label="Download Filtered Dataset as CSV",
    data=csv,
    file_name="filtered_educational_facilities.csv",
    mime="text/csv",
)
    

    st.markdown("---")
    st.caption("🏫 Nigeria Educational Facilities Dashboard | Data update in real time.")
    
if __name__ == "__main__":
    main()