"""
intern_portal.py - Intern Self-Service Dashboard
==================================================
Provides interns with:
- AI Virtual Mentor with personalized action plans
- Performance Rings benchmarked against department averages
- Skill Matrix Comparison (You vs. Department)
- 4-Week Trajectory tracking with seeded randomization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import hashlib
from streamlit_lottie import st_lottie
from config import load_lottieurl, stream_typing_effect


def render_intern_portal(df):
    """Main entry point for the Intern dashboard."""
    my_data = df[df["Employee_ID"] == st.session_state.emp_id]

    if my_data.empty:
        st.error(f"Cannot find data for {st.session_state.emp_id}. Please contact HR.")
        return

    my_data = my_data.iloc[0]
    dept = my_data.get("Department", "N/A")

    st.title(f"👋 Welcome back, {my_data.get('Employee_Name', 'Intern')}!")
    st.markdown(f"**Department:** {dept} | **ID:** {st.session_state.emp_id}")

    st.divider()
    _render_ai_mentor(my_data)

    st.divider()
    st.subheader("📊 Performance Rings (vs Dept Average)")
    dept_df = df[df["Department"] == dept]

    if not dept_df.empty:
        _render_performance_rings(my_data, dept_df)
        st.divider()
        _render_charts(my_data, dept_df, dept)
    else:
        st.warning("Not enough department data to generate benchmarking yet.")


def _render_ai_mentor(my_data):
    """Render the AI Virtual Mentor section with personalized coaching."""
    ment_col1, ment_col2 = st.columns([1, 3])

    with ment_col1:
        lottie_robot = load_lottieurl(
            "https://lottie.host/21191060-8456-42d8-bf11-7393e1104eab/lQfXU4JtZ8.json"
        )
        if lottie_robot:
            st_lottie(lottie_robot, height=200, key="robot")

    with ment_col2:
        st.subheader("🤖 Your AI Virtual Mentor")
        trend = my_data["Performance_Trend"]

        if trend == "Pending AI Assessment":
            st.info(
                "⏳ Your recent weekly data is currently being evaluated by the AI. "
                "Check back once HR runs the latest models!"
            )
        elif trend in ["Stable", "Improving"]:
            st.success(f"**Current Trajectory:** {trend} 🚀")
            st.write_stream(
                stream_typing_effect(
                    "You are on a great path! Keep maintaining your task completion rates "
                    "and engagement levels."
                )
            )
        else:
            st.error(f"**Current Trajectory:** {trend} ⚠️")
            st.write("**Your AI-Generated Action Plan for this week:**")

            action_plan = ""
            if my_data["Stress_Level"] >= 7.0:
                action_plan += (
                    "- 🧘 **Wellbeing:** Your stress metric is high. "
                    "Please schedule a quick sync with your manager.\n"
                )
            if my_data["Task_Completion_Rate"] < 75.0:
                action_plan += (
                    "- ⏱️ **Productivity:** You are falling behind on tasks. "
                    "Try the Pomodoro technique (25-minute focused sprints).\n"
                )
            if my_data["Engagement_Score"] < 60.0:
                action_plan += (
                    "- 🤝 **Engagement:** Try to participate more in team stand-ups "
                    "or reach out to a peer for a collaborative session.\n"
                )
            if my_data["Weekly_Learning_Hours"] < 10.0:
                action_plan += (
                    "- 📚 **Upskilling:** Block out at least 2 hours on your calendar "
                    "specifically dedicated to your learning modules.\n"
                )

            if action_plan:
                st.write_stream(stream_typing_effect(action_plan))


def _render_performance_rings(my_data, dept_df):
    """Render gauge charts comparing intern vs department averages."""
    avg_task = dept_df["Task_Completion_Rate"].mean()
    avg_att = dept_df["Attendance_Rate"].mean()
    avg_eng = dept_df["Engagement_Score"].mean()

    ring_c1, ring_c2, ring_c3 = st.columns(3)

    def create_gauge(title, value, reference, color):
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": title, "font": {"size": 18, "color": "white"}},
                delta={
                    "reference": reference,
                    "increasing": {"color": "#4CAF50"},
                    "decreasing": {"color": "#FF5252"},
                },
                gauge={
                    "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "white"},
                    "bar": {"color": color},
                    "bgcolor": "rgba(0,0,0,0)",
                    "borderwidth": 2,
                    "bordercolor": "rgba(255,255,255,0.2)",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(255,255,255,0.05)"},
                        {"range": [50, 80], "color": "rgba(255,255,255,0.1)"},
                    ],
                },
            )
        )
        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
        )
        return fig

    with ring_c1:
        st.plotly_chart(
            create_gauge("Task Completion", my_data["Task_Completion_Rate"], avg_task, "#4CAF50"),
            use_container_width=True,
        )
    with ring_c2:
        st.plotly_chart(
            create_gauge("Attendance", my_data["Attendance_Rate"], avg_att, "#2196F3"),
            use_container_width=True,
        )
    with ring_c3:
        st.plotly_chart(
            create_gauge("Engagement", my_data["Engagement_Score"], avg_eng, "#9C27B0"),
            use_container_width=True,
        )


def _render_charts(my_data, dept_df, dept):
    """Render the Skill Matrix bar chart and 4-Week Trajectory line chart."""
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📊 Skill Matrix Comparison")
        categories = [
            "Technical_Assessment_Score", "Coding_Test_Score", "Average_Quiz_Score",
            "Task_Completion_Rate", "Attendance_Rate", "Engagement_Score",
        ]
        intern_scores = [my_data[cat] for cat in categories]
        dept_scores = [dept_df[cat].mean() for cat in categories]
        bar_df = pd.DataFrame({
            "Metric": categories * 2,
            "Score": intern_scores + dept_scores,
            "Type": ["You"] * len(categories) + [f"{dept} Average"] * len(categories),
        })
        fig_bar = px.bar(bar_df, x="Metric", y="Score", color="Type", barmode="group", text_auto=".1f")
        fig_bar.update_layout(
            yaxis=dict(range=[0, 105], title="Score"),
            xaxis=dict(title=""),
            legend_title_text="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.subheader("📈 Your 4-Week Trajectory")
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4 (Current)"]
        current_task = my_data["Task_Completion_Rate"]
        current_eng = my_data["Engagement_Score"]
        current_stress = my_data["Stress_Level"] * 10

        seed_val = int(hashlib.md5(st.session_state.emp_id.encode()).hexdigest(), 16) % (10 ** 8)
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
        fig_line = px.line(trend_df, x="Week", y="Score", color="Metric", markers=True)
        fig_line.update_layout(
            yaxis=dict(range=[0, 105], title="Score"),
            xaxis=dict(title=""),
            legend_title_text="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig_line, use_container_width=True)
