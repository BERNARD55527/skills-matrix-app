import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# נתוני מטריצת כישורים מעודכנים
roles_skills = {
    "מנהלת תפעול": {
        "כישורים מקצועיים": ["דיני עבודה", "ניהול תהליכים"],
        "כישורים אישיים": ["פתרון בעיות", "עמידה בלחץ"],
        "כישורים טכנולוגיים": ["מערכות ניהול (SAP)", "Excel"],
        "כישורים ניהוליים": ["ניהול צוותים", "תכנון אסטרטגי"]
    },
    "רכזת תפעול": {
        "כישורים מקצועיים": ["דיני עבודה", "טיפול בתהליכים אדמיניסטרטיביים"],
        "כישורים אישיים": ["סדר וארגון", "מיומנויות תקשורת"],
        "כישורים טכנולוגיים": ["Excel", "מערכות HRIS"],
        "כישורים ניהוליים": ["עבודה בצוות"]
    },
    "עובדת סוציאלית": {
        "כישורים מקצועיים": ["תמיכה רגשית", "התערבות במשברים"],
        "כישורים אישיים": ["אמפתיה", "הקשבה פעילה"],
        "כישורים טכנולוגיים": ["ניהול מערכות ייעוץ"],
        "כישורים ניהוליים": ["עבודה מול ממשקים רבים"]
    }
}

# רמות כישורים
skill_levels = {"מתחיל": 1, "בינוני": 2, "מתקדם": 3, "מומחה": 4}

# אתחול או טעינת נתונים קיימים
if "employees" not in st.session_state:
    st.session_state["employees"] = {}

st.title("מטריצת כישורים במשאבי אנוש")

# בחירת תפקיד
role = st.selectbox("בחר תפקיד", list(roles_skills.keys()))

# הצגת הכישורים הנדרשים
skills = roles_skills[role]
st.write(f"### כישורים נדרשים עבור {role}")
for category, skill_list in skills.items():
    st.write(f"**{category}:** ", ", ".join(skill_list))

# הוספת עובד והקצאת רמות כישורים
st.write("### הקצאת כישורים לעובד")
employee_name = st.text_input("הזן שם עובד")

if employee_name:
    if employee_name not in st.session_state["employees"]:
        st.session_state["employees"][employee_name] = {}
    
    for category, skill_list in skills.items():
        for skill in skill_list:
            level = st.selectbox(f"בחר את הרמה של {employee_name} עבור {skill}", list(skill_levels.keys()), key=f"{employee_name}_{skill}")
            st.session_state["employees"][employee_name][skill] = level

# הצגת ויזואליזציה גרפית
def plot_skill_matrix():
    employees = list(st.session_state["employees"].keys())
    if not employees:
        st.warning("אין נתונים להצגה.")
        return
    
    skill_data = {skill: [] for category in skills.values() for skill in category}
    for emp in employees:
        for skill in skill_data.keys():
            level = st.session_state["employees"].get(emp, {}).get(skill, "מתחיל")
            skill_data[skill].append(skill_levels[level])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(skill_data))
    width = 0.2
    
    for i, emp in enumerate(employees):
        ax.bar(x + i * width, [skill_data[skill][i] for skill in skill_data], width, label=emp)
    
    ax.set_xlabel("כישורים")
    ax.set_ylabel("רמת כישורים")
    ax.set_title("רמות כישורים לפי עובדים")
    ax.set_xticks(x + width / len(employees))
    ax.set_xticklabels(skill_data.keys(), rotation=45, ha="right")
    ax.legend()
    
    st.pyplot(fig)

st.write("### ויזואליזציה של מצב הצוות")
plot_skill_matrix()

# כפתור הורדת הנתונים
st.download_button("הורד מטריצת כישורים", pd.DataFrame.from_dict(st.session_state["employees"], orient='index').to_csv(index=True), "skill_matrix.csv", "text/csv")
