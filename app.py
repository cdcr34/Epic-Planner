import streamlit as st
import random
import json
import os
from datetime import date

# -------------------------------
# Initialize state
# -------------------------------
if "tasks_today" not in st.session_state:
    st.session_state.tasks_today = []
if "backlog" not in st.session_state:
    st.session_state.backlog = []
if "points" not in st.session_state:
    st.session_state.points = 0

# Persistence file
DATA_FILE = "tasks.json"

# -------------------------------
# Functions for saving/loading
# -------------------------------
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            st.session_state.tasks_today = data.get("tasks_today", [])
            st.session_state.backlog = data.get("backlog", [])
            st.session_state.points = data.get("points", 0)

def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump({
            "tasks_today": st.session_state.tasks_today,
            "backlog": st.session_state.backlog,
            "points": st.session_state.points
        }, f)

load_tasks()

# -------------------------------
# App Title
# -------------------------------
st.title("🎯 Fun To-Do List")
st.write("Complete tasks, earn points, and manage your future plans!")

# -------------------------------
# Sidebar: Backlog Management
# -------------------------------
st.sidebar.header("📅 Backlog / Future Tasks")

# Form to add backlog task
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
        for i, t in enumerate(st.session_state.backlog):
            st.write(f"📌 {t['task']} (Due: {t['due']})")
            if st.button(f"➡ Add to Today", key=f"move_{i}"):
                st.session_state.tasks_today.append({"task": t["task"], "done": False})
                del st.session_state.backlog[i]
                save_tasks()
                st.experimental_rerun()
else:
    st.sidebar.write("No backlog tasks yet!")

# -------------------------------
# Main: Today's Task Management
# -------------------------------
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Add a new task for today:")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks_today.append({"task": new_task, "done": False})
        save_tasks()
        st.success(f"Task '{new_task}' added!")

st.subheader("Today's Tasks:")
if st.session_state.tasks_today:
    for i, t in enumerate(st.session_state.tasks_today):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            if st.checkbox(t["task"], value=t["done"], key=f"task_{i}"):
                if not t["done"]:
                    # Mark as done
                    t["done"] = True
                    st.session_state.points += 10
                    st.success("✅ Task completed! +10 XP")
                    # Show motivation
                    motivation = random.choice([
                        "🔥 Keep going, you're crushing it!",
                        "🚀 Great job! One step closer!",
                        "💪 You got this!",
                        "⭐ Amazing! Keep it up!"
                    ])
                    st.info(motivation)
