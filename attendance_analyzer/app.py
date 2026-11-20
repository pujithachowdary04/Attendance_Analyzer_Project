import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Attendance Analyzer",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Attendance Analyzer")
st.write("30 Students Attendance Analysis Dashboard")

st.success("Dashboard is working successfully!")

# Attendance threshold
threshold = st.slider(
    "Attendance Eligibility Threshold (%)",
    1, 100, 75
)

# Student data - 30 students
students = [
    f"Student {i:02d}" for i in range(1, 31)
]

attendance = [
    90, 85, 78, 65, 92, 55, 80, 88, 72, 95,
    60, 76, 83, 69, 91, 74, 86, 58, 79, 98,
    67, 82, 89, 71, 94, 63, 77, 84, 50, 96
]

df = pd.DataFrame({
    "Student Name": students,
    "Attendance (%)": attendance
})

# Sidebar
st.sidebar.title("Dashboard Menu")
menu = st.sidebar.radio(
    "Select Option",
    ["Dashboard", "Student Details", "Attendance Chart"]
)

# Dashboard
if menu == "Dashboard":

    st.subheader("📊 Attendance Overview")

    total = len(df)
    average = round(df["Attendance (%)"].mean(), 2)
    eligible = len(df[df["Attendance (%)"] >= threshold])
    shortage = total - eligible

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", total)
    col2.metric("Average Attendance", f"{average}%")
    col3.metric("Eligible Students", eligible)
    col4.metric("Attendance Shortage", shortage)

    st.subheader("📋 Attendance Summary")

    st.dataframe(df, use_container_width=True)

    st.subheader("📌 Eligibility Status")

    df["Status"] = df["Attendance (%)"].apply(
        lambda x: "Eligible" if x >= threshold else "Shortage"
    )

    st.dataframe(df, use_container_width=True)

# Student Details
elif menu == "Student Details":

    st.subheader("👨‍🎓 Student Attendance Details")

    search = st.text_input("Search Student")

    filtered = df[
        df["Student Name"].str.contains(search, case=False)
    ]

    st.dataframe(filtered, use_container_width=True)

    st.subheader("✏️ Edit Attendance")

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed"
    )

    if st.button("Save Attendance Changes"):
        df = edited_df.copy()
        st.session_state["attendance_data"] = df
        st.success("Attendance updated successfully!")

# Attendance Chart
elif menu == "Attendance Chart":

    st.subheader("📈 Student Attendance Analysis")

    chart_data = st.session_state.get(
        "attendance_data", df
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    colors = [
        "green" if x >= threshold else "red"
        for x in chart_data["Attendance (%)"]
    ]

    ax.bar(
        chart_data["Student Name"],
        chart_data["Attendance (%)"],
        color=colors
    )

    ax.axhline(
        threshold,
        linestyle="--",
        color="blue",
        label=f"Threshold {threshold}%"
    )

    ax.set_ylabel("Attendance (%)")
    ax.set_xlabel("Students")
    ax.set_title("Student Attendance Analysis")
    ax.set_ylim(0, 105)
    ax.tick_params(axis="x", rotation=90)
    ax.legend()

    st.pyplot(fig)

# Download CSV
st.subheader("📥 Download Attendance Report")

download_df = st.session_state.get(
    "attendance_data", df
)

csv = download_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Attendance Report",
    data=csv,
    file_name="attendance_report.csv",
    mime="text/csv"
)

st.success("Attendance Dashboard Loaded Successfully!")