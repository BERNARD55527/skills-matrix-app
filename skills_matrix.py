import streamlit as st
import pandas as pd

# Sample skill matrix data
roles_skills = {
    "Recruiter": ["Interviewing", "Candidate Sourcing", "Employer Branding"],
    "HR Business Partner": ["Employee Relations", "HR Strategy", "Performance Management"],
    "Training Coordinator": ["Training Design", "Facilitation", "LMS Management"]
}

# Skill levels
skill_levels = ["Beginner", "Intermediate", "Advanced", "Expert"]

# Initialize or load existing data
if "employees" not in st.session_state:
    st.session_state["employees"] = {}

st.title("HR Skills Matrix")

# Select role
role = st.selectbox("Select a Role", list(roles_skills.keys()))

# Display required skills
skills = roles_skills[role]
st.write(f"### Skills required for {role}")
st.write(", ".join(skills))

# Add employee and assign skill levels
st.write("### Assign Skills to an Employee")
employee_name = st.text_input("Enter Employee Name")

if employee_name:
    if employee_name not in st.session_state["employees"]:
        st.session_state["employees"][employee_name] = {}
    
    for skill in skills:
        level = st.selectbox(f"Select {employee_name}'s level in {skill}", skill_levels, key=f"{employee_name}_{skill}")
        st.session_state["employees"][employee_name][skill] = level

# Display current skill matrix
data = []
for emp, skill_data in st.session_state["employees"].items():
    for skill, level in skill_data.items():
        data.append([emp, skill, level])

df = pd.DataFrame(data, columns=["Employee", "Skill", "Level"])
st.write("### Current Skills Matrix")
st.dataframe(df)

# Download button
st.download_button("Download Skill Matrix", df.to_csv(index=False), "skill_matrix.csv", "text/csv")
