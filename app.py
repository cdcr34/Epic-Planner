import streamlit as st
import random
import json
import os
from datetime import date

# -------------------------------
# Persistence files
# -------------------------------
TASKS_FILE = "tasks.json"
NOTES_FILE = "notes.json"

# -------------------------------
# Initialize session state
# -------------------------------
if "tasks_today" not in st.session_state:
    st.session_state.tasks_today = []
if "backlog" not in st.session_state:
    st.session_state.backlog = []
if "points" not in st.session_state:
    st.session_state.points = 0

# Default notes categories
default_notes = {
    "📚 Italian": "",
    "📖 Urban Politics": "",
    "📝 Intern Class": "",
    "📚 Seminar": "",
    "📖 Friends of the Parks": "",
    "🏠 Personal Tasks": "",
    "🔁 Continuous Tasks": ""
}

# -------------------------------
# Load data
# -------------------------------
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            data = json.load(f)
            st.session_state.tasks_today = data.get("tasks_today", [])
            st.session_state.backlog = data.get("backlog", [])
            st.session_state.points = data.get("points", 0)

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump({
            "tasks_today": st.session_state.tasks_today,
            "backlog": st.session_state.backlog,
            "points": st.session_state.points
        }, f)

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return default_notes

def save_notes(notes_data):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes_data, f)

# Load everything
load_tasks()
notes_data = load_notes()

# -------------------------------
# App Layout
# -------------------------------
st.title("🎯 Funnnnnnn To-Do List + Quick Notes")

# -------------------------------
# Notes Section (Top)
# -------------------------------
st.subheader("🗒 Quick Notes")
st.caption("Use this for reminders, continuous tasks, or notes for classes. Auto-saves on edit.")

tabs = st.tabs(list(notes_data.keys()))
for i, category in enumerate(notes_data.keys()):
    with tabs[i]:
        notes_data[category] = st.text_area(
            f"Write notes for {category}",
            value=notes_data[category],
            height=150,
            key=f"note_{i}"
        )
        save_notes(notes_data)

st.download_button(
    label="📥 Download All Notes",
    data="\n\n".join([f"{cat}:\n{txt}" for cat, txt in notes_data.items()]),
    file_name="my_notes.txt"
)

st.markdown("---")

# -------------------------------
# Sidebar: Backlog / Future Tasks
# -------------------------------
st.sidebar.header("📅 Backlog / Future Tasks")
with st.sidebar.form("add_backlog", clear_on_submit=True):
    backlog_task = st.text_input("Future Task:")
    due_date = st.date_input("Due Date:", min_value=date.today())
    submitted_backlog = st.form_submit_button("Add to Backlog")
    if submitted_backlog and backlog_task.strip():
        st.session_state.backlog.append({"task": backlog_task, "due": str(due_date)})
        save_tasks()
        st.sidebar.success(f"Added '{backlog_task}' to backlog!")

# Display backlog with buttons
if st.session_state.backlog:
    with st.sidebar.expander("Your Backlog"):
        # Make a copy to iterate safely
        backlog_copy = st.session_state.backlog.copy()
        for i, t in enumerate(backlog_copy):
            st.write(f"📌 {t['task']} (Due: {t['due']})")
            if st.button(f"➡ Add to Today", key=f"move_{i}"):
                # Append to today's list
                st.session_state.tasks_today.append({"task": t["task"], "done": False})
                # Remove from backlog safely
                st.session_state.backlog.remove(t)
                # Save and rerun
                save_tasks()
                st.experimental_rerun()
else:
    st.sidebar.write("No backlog tasks yet!")

# -------------------------------
# Today's Tasks Section
# -------------------------------
st.subheader("✅ Today's Tasks")
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Add a new task for today:")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks_today.append({"task": new_task, "done": False})
        save_tasks()
        st.success(f"Task '{new_task}' added!")

if st.session_state.tasks_today:
    for i, t in enumerate(st.session_state.tasks_today):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            if st.checkbox(t["task"], value=t["done"], key=f"task_{i}"):
                if not t["done"]:
                    t["done"] = True
                    st.session_state.points += 10
                    st.success("✅ Task completed! +10 XP")
                    motivation = random.choice([
                        "🔥 Keep going, you're crushing it!",
                        "🚀 Great job! One step closer!",
                        "💪 You got this!",
                        "⭐ Amazing! Keep it up!"
                    ])
                    st.info(motivation)
                    if all(task["done"] for task in st.session_state.tasks_today):
                        st.balloons()
                save_tasks()
        with col2:
            if st.button("❌", key=f"delete_today_{i}"):
                del st.session_state.tasks_today[i]
                save_tasks()
                st.experimental_rerun()
else:
    st.write("No tasks yet. Add one above!")

# -------------------------------
# Progress & XP
# -------------------------------
total = len(st.session_state.tasks_today)
done = sum(1 for t in st.session_state.tasks_today if t["done"])
if total > 0:
    st.subheader("📊 Progress")
    st.progress(done / total)
    st.write(f"{done}/{total} tasks completed")

st.subheader(f"🏆 XP: {st.session_state.points}")

# Save tasks
save_tasks()
