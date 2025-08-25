import streamlit as st
import random
import json
import os

# -------------------------------
# Load or initialize task data
# -------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "points" not in st.session_state:
    st.session_state.points = 0

# Persistence file
DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            st.session_state.tasks = data.get("tasks", [])
            st.session_state.points = data.get("points", 0)

def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump({"tasks": st.session_state.tasks, "points": st.session_state.points}, f)

load_tasks()

# -------------------------------
# App title
# -------------------------------
st.title("🎯 Fun To-Do List")
st.write("Complete tasks, earn points, and have fun!")

# -------------------------------
# Add new task
# -------------------------------
with st.form("add_task_form"):
    new_task = st.text_input("Add a new task:")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks.append({"task": new_task, "done": False})
        save_tasks()
        st.success(f"Task '{new_task}' added!")

# -------------------------------
# Show tasks
# -------------------------------
st.subheader("Your Tasks:")
if st.session_state.tasks:
    for i, t in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            if st.checkbox(t["task"], value=t["done"], key=i):
                if not t["done"]:
                    # Mark as done
                    t["done"] = True
                    st.session_state.points += 10
                    st.success("✅ Task completed! +10 XP")
                    # Random motivation
                    motivation = random.choice([
                        "🔥 Keep going, you're crushing it!",
                        "🚀 Great job! One step closer!",
                        "💪 You got this!",
                        "⭐ Amazing! Keep it up!"
                    ])
                    st.info(motivation)
                    if all(task["done"] for task in st.session_state.tasks):
                        st.balloons()
                save_tasks()
        with col2:
            if st.button("❌", key=f"delete_{i}"):
                del st.session_state.tasks[i]
                save_tasks()
                st.experimental_rerun()
else:
    st.write("No tasks yet. Add one above!")

# -------------------------------
# Progress bar
# -------------------------------
total = len(st.session_state.tasks)
done = sum(1 for t in st.session_state.tasks if t["done"])
if total > 0:
    st.subheader("Progress:")
    st.progress(done / total)
    st.write(f"{done}/{total} tasks completed")

# -------------------------------
# XP Display
# -------------------------------
st.subheader(f"🏆 XP: {st.session_state.points}")

# Save on exit
save_tasks()
