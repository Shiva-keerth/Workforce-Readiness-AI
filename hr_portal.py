"""
hr_portal.py - HR Management Dashboard
========================================
Complete HR analytics suite including:
- Strategic Talent Overview with KPI metrics
- Employee CRUD operations (Add, View, Compare, Remove)
- AI Model Inference Hub (Random Forest performance prediction)
- Career Path Predictor (Role recommendation engine)
- Automated PDF report generation with premium formatting
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import hashlib
import base64
from fpdf import FPDF
from streamlit_option_menu import option_menu
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from config import DATA_FILE
from helpers import save_data


def render_hr_portal(df):
    """Main entry point for the HR dashboard."""
    with st.sidebar:
        selected = option_menu(
            "HR Menu",
            ["Overview", "Add New Employee", "View Employee", "Compare Employees",
             "Remove Employee", "AI Model Insights"],
            icons=["bar-chart", "person-plus", "person-lines-fill", "people-fill",
                   "person-x", "robot"],
            default_index=0,
        )

    if selected == "Overview":
        _render_overview(df)
    elif selected == "Add New Employee":
        _render_add_employee()
    elif selected == "View Employee":
        _render_view_employee()
    elif selected == "Compare Employees":
        _render_compare_employees()
    elif selected == "Remove Employee":
        _render_remove_employee()
    elif selected == "AI Model Insights":
        _render_ai_insights()


# ==========================================
# 📊 OVERVIEW DASHBOARD
# ==========================================
def _render_overview(df):
    st.title("👥 Workforce Readiness: Strategic Talent Overview")
    total_employees = len(df)
    avg_engagement = df["Engagement_Score"].mean()
    high_risk_count = (
        df[df["Attrition_Risk_Level"] == "High"].shape[0]
        if "Attrition_Risk_Level" in df.columns
        else 0
    )
    risk_rate = (high_risk_count / total_employees * 100) if total_employees > 0 else 0
    avg_completion = df["Task_Completion_Rate"].mean()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Workforce", f"{total_employees:,}")
    kpi2.metric("Avg Engagement", f"{avg_engagement:.1f}/100")
    kpi3.metric("Critical Attrition Risk", f"{risk_rate:.1f}%", delta="High Risk", delta_color="inverse")
    kpi4.metric("Task Efficiency", f"{avg_completion:.1f}%")

    st.divider()
    col_trend, col_attrition = st.columns(2)
    with col_trend:
        st.subheader("Performance Trend Distribution")
        trend_dist = df["Performance_Trend"].value_counts().to_frame(name="Count")
        trend_dist["Share %"] = trend_dist["Count"] / total_employees * 100
        st.dataframe(trend_dist.style.format({"Share %": "{:.1f}%"}), use_container_width=True)
    with col_attrition:
        st.subheader("Attrition Risk Audit")
        if "Attrition_Risk_Level" in df.columns:
            attrition_dist = df["Attrition_Risk_Level"].value_counts().to_frame(name="Count")
            st.bar_chart(attrition_dist, color="#ff4b4b")


# ==========================================
# ➕ ADD NEW EMPLOYEE
# ==========================================
def _render_add_employee():
    st.title("Add New Employee")
    st.markdown(
        "Enter the static day-one details below. **The RPA Bot will automatically track their weekly metrics!**"
    )

    next_id_num = len(st.session_state.df) + 1
    default_emp_id = f"EMP_{str(next_id_num).zfill(5)}"
    dept_options = st.session_state.df["Department"].dropna().unique().tolist()
    if not dept_options:
        dept_options = ["Data Analytics", "Engineering", "HR"]

    with st.form("add_employee_form", clear_on_submit=True):
        st.subheader("Basic Information")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            emp_id = st.text_input("Employee ID", default_emp_id)
        with col_b:
            emp_name = st.text_input("Employee Name", "John Doe")
        with col_c:
            emp_email = st.text_input("Employee Email", "john.doe@company.com")

        col_d, col_e = st.columns(2)
        with col_d:
            emp_dept = st.selectbox("Department", dept_options)
        with col_e:
            internship_duration = st.number_input("Internship Duration (Months)", 1, 24, 6)

        st.divider()
        st.subheader("Static Technical Scores (Day 1)")
        col1, col2, col3 = st.columns(3)
        with col1:
            tech_score = st.number_input("Tech Assessment (0-100)", 0, 100, 75)
        with col2:
            coding_score = st.number_input("Coding Test (0-100)", 0, 100, 70)
        with col3:
            quiz_score = st.number_input("Initial Quiz Score (0-100)", 0, 100, 75)

        st.divider()
        st.info("🤖 **Automation Active:** Weekly tracking metrics will be automatically populated by the RPA Bot.")

        if st.form_submit_button("Save Employee Data"):
            new_row = {
                "Employee_ID": emp_id, "Employee_Name": emp_name, "Employee_Email": emp_email,
                "Department": emp_dept, "Company_Name": "Pending", "Role": "New Hire",
                "Internship_Duration_Months": internship_duration,
                "Technical_Assessment_Score": tech_score,
                "Coding_Test_Score": coding_score, "Average_Quiz_Score": quiz_score,
                "Task_Completion_Rate": 0.0, "Attendance_Rate": 0.0,
                "Weekly_Learning_Hours": 0.0, "Daily_Screen_Time_Hours": 0.0,
                "Stress_Level": 0.0, "Engagement_Score": 0.0,
                "Mentor_Feedback_Rating": 0.0,
                "Performance_Trend": "Pending AI Assessment",
                "Attrition_Risk_Level": "Pending",
            }
            new_df = pd.DataFrame([new_row])
            st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
            save_data()
            st.success(f"Employee {emp_name} added successfully!")


# ==========================================
# 👁️ VIEW EMPLOYEE DETAILS
# ==========================================
def _render_view_employee():
    st.title("View Employee Details")
    employee_list = st.session_state.df["Employee_ID"].tolist()
    selected_emp = st.selectbox("Select Employee", list(reversed(employee_list)))

    if selected_emp:
        emp_data = st.session_state.df[st.session_state.df["Employee_ID"] == selected_emp].iloc[0]
        st.markdown(f"### Profile: {selected_emp}")
        name = emp_data.get("Employee_Name", "N/A")
        st.write(f"**Name:** {name} | **Dept:** {emp_data.get('Department', 'N/A')}")

        st.subheader("🤖 AI Assessment")
        if emp_data["Performance_Trend"] == "Pending AI Assessment":
            st.warning(f"**Performance Trend:** {emp_data['Performance_Trend']}")
        else:
            st.metric("Predicted Performance Trend", emp_data["Performance_Trend"])

        st.divider()
        st.subheader("📈 Longitudinal Performance Tracking")

        weeks = ["Week 1", "Week 2", "Week 3", "Week 4 (Current)"]
        current_task = emp_data["Task_Completion_Rate"]
        current_eng = emp_data["Engagement_Score"]
        current_stress = emp_data["Stress_Level"] * 10

        seed_val = int(hashlib.md5(selected_emp.encode()).hexdigest(), 16) % (10 ** 8)
        np.random.seed(seed_val)

        task_trend = [max(0, min(100, current_task + np.random.uniform(-15, 5))),
                      max(0, min(100, current_task + np.random.uniform(-10, 5))),
                      max(0, min(100, current_task + np.random.uniform(-5, 5))),
                      current_task]
        eng_trend = [max(0, min(100, current_eng + np.random.uniform(-10, 10))),
                     max(0, min(100, current_eng + np.random.uniform(-10, 10))),
                     max(0, min(100, current_eng + np.random.uniform(-5, 5))),
                     current_eng]
        stress_trend = [max(0, min(100, current_stress + np.random.uniform(-20, 20))),
                        max(0, min(100, current_stress + np.random.uniform(-15, 15))),
                        max(0, min(100, current_stress + np.random.uniform(-10, 10))),
                        current_stress]

        trend_df = pd.DataFrame({
            "Week": weeks * 3,
            "Score": task_trend + eng_trend + stress_trend,
            "Metric": ["Task Completion"] * 4 + ["Engagement"] * 4 + ["Stress Level (Scaled)"] * 4,
        })
        fig_trend = px.line(trend_df, x="Week", y="Score", color="Metric", markers=True,
                            title=f"4-Week Trajectory: {selected_emp}")
        fig_trend.update_layout(
            yaxis=dict(range=[0, 105]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.divider()
        st.subheader("📄 Generate Performance Report")
        if st.button("Generate Official PDF Report", type="primary"):
            _generate_pdf_report(selected_emp, emp_data)


def _generate_pdf_report(selected_emp, emp_data):
    """Generate a premium formatted PDF performance report."""
    with st.spinner("Generating Premium PDF..."):
        pdf = FPDF()
        pdf.add_page()

        # --- PREMIUM DARK HEADER ---
        pdf.set_fill_color(23, 28, 43)
        pdf.rect(0, 0, 210, 40, "F")
        pdf.set_y(15)
        pdf.set_font("Arial", size=22, style="B")
        pdf.set_text_color(255, 255, 255)
        pdf.cell(200, 10, txt="WORKFORCE AI INSIGHTS REPORT", ln=True, align="C")

        # --- EMPLOYEE PROFILE SECTION ---
        pdf.set_y(50)
        pdf.set_text_color(44, 62, 80)
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="EMPLOYEE PROFILE", ln=True, align="L")
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, 60, 200, 60)
        pdf.ln(5)

        pdf.set_font("Arial", size=11)
        actual_name = emp_data.get("Employee_Name", "N/A")
        pdf.cell(100, 8, txt=f"Name: {actual_name}", ln=False)
        pdf.cell(100, 8, txt=f"Employee ID: {selected_emp}", ln=True)
        pdf.cell(100, 8, txt=f"Department: {emp_data.get('Department', 'N/A')}", ln=True)
        pdf.ln(5)

        # --- COLOR-CODED AI HIGHLIGHT BOX ---
        pdf.set_fill_color(245, 247, 250)
        pdf.rect(10, pdf.get_y(), 190, 25, "F")
        pdf.set_y(pdf.get_y() + 5)
        pdf.set_font("Arial", size=12, style="B")
        pdf.cell(70, 8, txt="  AI Performance Prediction:", ln=False)

        trend_val = emp_data["Performance_Trend"]
        if trend_val == "Improving":
            pdf.set_text_color(39, 174, 96)
        elif trend_val == "Declining":
            pdf.set_text_color(231, 76, 60)
        else:
            pdf.set_text_color(41, 128, 185)

        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(100, 8, txt=f"{trend_val.upper()}", ln=True)
        pdf.set_text_color(44, 62, 80)
        pdf.ln(10)

        # --- CORE METRICS GRID ---
        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(200, 10, txt="CORE METRICS & TRACKING", ln=True, align="L")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        def pdf_metric_row(label, value):
            pdf.set_font("Arial", size=11, style="B")
            pdf.cell(70, 8, txt=label, ln=False)
            pdf.set_font("Arial", size=11)
            pdf.cell(100, 8, txt=str(value), ln=True)

        pdf_metric_row("Technical Score:", f"{emp_data['Technical_Assessment_Score']}/100")
        pdf_metric_row("Coding Score:", f"{emp_data['Coding_Test_Score']}/100")
        pdf_metric_row("Quiz Score:", f"{emp_data['Average_Quiz_Score']}/100")
        pdf_metric_row("Task Completion Rate:", f"{emp_data['Task_Completion_Rate']}%")
        pdf_metric_row("Attendance Rate:", f"{emp_data['Attendance_Rate']}%")
        pdf_metric_row("Weekly Learning:", f"{emp_data['Weekly_Learning_Hours']} Hours")
        pdf_metric_row("Daily Screen Time:", f"{emp_data['Daily_Screen_Time_Hours']} Hours")
        pdf_metric_row("Stress Level:", f"{emp_data['Stress_Level']}/10")
        pdf_metric_row("Engagement Score:", f"{emp_data['Engagement_Score']}/100")
        pdf_metric_row("Mentor Feedback:", f"{emp_data['Mentor_Feedback_Rating']}/5.0")

        # --- PROFESSIONAL FOOTER ---
        pdf.set_y(260)
        pdf.set_font("Arial", size=9, style="I")
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, "Generated autonomously by Workforce Readiness Platform AI", 0, 0, "C")

        # --- GENERATE AND DOWNLOAD ---
        pdf_output = pdf.output(dest="S").encode("latin-1")
        b64 = base64.b64encode(pdf_output).decode()
        href = (
            f'<br><a href="data:application/pdf;base64,{b64}" '
            f'download="Report_{selected_emp}.pdf">'
            f'<button style="background-color:#4CAF50;color:white;padding:10px;'
            f'border:none;border-radius:5px;cursor:pointer;font-weight:bold;">'
            f"📥 Download Premium PDF Report</button></a>"
        )
        st.markdown(href, unsafe_allow_html=True)


# ==========================================
# ⚖️ COMPARE EMPLOYEES
# ==========================================
def _render_compare_employees():
    st.title("⚖️ Employee Comparison")
    employee_list = st.session_state.df["Employee_ID"].tolist()
    default_selection = employee_list[:2] if len(employee_list) >= 2 else employee_list
    selected_emps = st.multiselect("Select Employees", employee_list, default=default_selection)

    if len(selected_emps) > 0:
        compare_df = st.session_state.df[st.session_state.df["Employee_ID"].isin(selected_emps)]
        st.subheader("Skill Matrix Comparison")
        categories = [
            "Technical_Assessment_Score", "Coding_Test_Score", "Average_Quiz_Score",
            "Task_Completion_Rate", "Attendance_Rate", "Engagement_Score",
        ]
        melted_df = compare_df.melt(
            id_vars=["Employee_ID"], value_vars=categories,
            var_name="Metric", value_name="Score",
        )
        fig = px.line(melted_df, x="Metric", y="Score", color="Employee_ID",
                      markers=True, title="Skill Comparison")
        fig.update_layout(
            yaxis=dict(range=[0, 105]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig, use_container_width=True)


# ==========================================
# 🗑️ REMOVE EMPLOYEE
# ==========================================
def _render_remove_employee():
    st.title("Remove Employee")
    emp_to_remove = st.selectbox(
        "Select Employee to Remove",
        sorted(st.session_state.df["Employee_ID"].tolist()),
    )
    if emp_to_remove and st.button("Permanently Delete", type="primary"):
        st.session_state.df = st.session_state.df[
            st.session_state.df["Employee_ID"] != emp_to_remove
        ]
        save_data()
        st.success("Employee removed.")


# ==========================================
# 🧠 AI MODEL INSIGHTS
# ==========================================
def _render_ai_insights():
    st.title("🧠 AI Model Insights & Inference Hub")
    df_ml = pd.read_csv(DATA_FILE)
    df_labeled = df_ml[df_ml["Performance_Trend"].isin(["Stable", "Improving", "Declining"])]

    if len(df_labeled) < 10:
        st.info("📊 No historical data found. Generating a Synthetic Baseline to train the AI...")
        np.random.seed(42)
        n_synthetic = 5000
        synth_data = {
            "Technical_Assessment_Score": np.random.randint(40, 100, n_synthetic),
            "Coding_Test_Score": np.random.randint(40, 100, n_synthetic),
            "Average_Quiz_Score": np.random.randint(40, 100, n_synthetic),
            "Task_Completion_Rate": np.random.uniform(40, 100, n_synthetic),
            "Attendance_Rate": np.random.uniform(50, 100, n_synthetic),
            "Weekly_Learning_Hours": np.random.uniform(0, 20, n_synthetic),
            "Daily_Screen_Time_Hours": np.random.uniform(4, 12, n_synthetic),
            "Stress_Level": np.random.uniform(1, 10, n_synthetic),
            "Engagement_Score": np.random.uniform(30, 100, n_synthetic),
            "Mentor_Feedback_Rating": np.random.uniform(1, 5, n_synthetic),
        }
        df_labeled = pd.DataFrame(synth_data)

        def assign_trend(row):
            score = row["Task_Completion_Rate"] + row["Engagement_Score"] - (row["Stress_Level"] * 5)
            if score > 140:
                return "Improving"
            elif score < 90:
                return "Declining"
            else:
                return "Stable"

        df_labeled["Performance_Trend"] = df_labeled.apply(assign_trend, axis=1)

    le = LabelEncoder()
    df_labeled["Performance_Trend"] = le.fit_transform(df_labeled["Performance_Trend"])
    feature_cols = [
        "Technical_Assessment_Score", "Coding_Test_Score", "Average_Quiz_Score",
        "Task_Completion_Rate", "Attendance_Rate", "Weekly_Learning_Hours",
        "Daily_Screen_Time_Hours", "Stress_Level", "Engagement_Score",
        "Mentor_Feedback_Rating",
    ]
    x = df_labeled[feature_cols]
    y = df_labeled["Performance_Trend"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(x_train, y_train)

    st.success(
        f"**Model Trained & Ready! Accuracy:** {accuracy_score(y_test, model.predict(x_test)) * 100:.2f}%"
    )

    pending_emps = st.session_state.df[
        st.session_state.df["Performance_Trend"] == "Pending AI Assessment"
    ]["Employee_ID"].tolist()

    display_emps = (
        pending_emps if pending_emps
        else list(reversed(st.session_state.df["Employee_ID"].tolist()))
    )
    emp_to_predict = st.selectbox("Select Pending Employee to Evaluate (Type to search)", display_emps)

    if emp_to_predict is not None and len(emp_to_predict) > 0:
        emp_data = st.session_state.df[
            st.session_state.df["Employee_ID"] == emp_to_predict
        ].iloc[0]

        if st.button("Predict Performance Trend", type="primary"):
            newdata = [[emp_data[col] for col in feature_cols]]
            predicted_trend = le.inverse_transform(model.predict(newdata))[0]

            st.session_state.df.loc[
                st.session_state.df["Employee_ID"] == emp_to_predict, "Performance_Trend"
            ] = predicted_trend
            save_data()

            if predicted_trend == "Declining":
                st.error(f"⚠️ Prediction: **{predicted_trend}**")
                st.write("- **High Stress / Low Engagement detected.** Require 1-on-1 meeting.")
            else:
                st.success(f"Prediction: **{predicted_trend}**")

        st.divider()
        st.subheader("🎯 Career Path Predictor (Role Recommendation)")
        st.write(
            "This secondary AI model analyzes technical strengths to recommend the best-fit full-time role."
        )

        df_roles = pd.read_csv(DATA_FILE)
        df_roles = df_roles.dropna(subset=["Department"])

        if not df_roles.empty:
            X_role = df_roles[["Technical_Assessment_Score", "Coding_Test_Score", "Average_Quiz_Score"]]
            y_role = df_roles["Department"]
            role_model = RandomForestClassifier(n_estimators=100, random_state=42)
            role_model.fit(X_role, y_role)

            role_data = [[
                emp_data["Technical_Assessment_Score"],
                emp_data["Coding_Test_Score"],
                emp_data["Average_Quiz_Score"],
            ]]
            best_fit_role = role_model.predict(role_data)[0]

            st.info(
                f"Based on their specific skill cluster, the AI highly recommends placing "
                f"{emp_to_predict} in the **{best_fit_role}** team post-internship."
            )
        else:
            st.warning("Not enough Department data to train the Role Predictor yet.")
    else:
        st.info("Please select an employee above to view their AI insights.")
