#!/usr/bin/env python3
import os
import re
from pathlib import Path
from datetime import datetime

SESSION_FILE = Path("sessions/SESSION.md")
TEMPLATE_FILE = Path("sessions/templates/daily-session.md")

def parse_session():
    if not SESSION_FILE.exists():
        return None
    
    content = SESSION_FILE.read_text(encoding='utf-8')
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "focus": "",
        "completed": [],
        "pending": [],
        "in_progress": [],
        "notes": ""
    }
    
    # Extraer Foco
    focus_match = re.search(r"## Today's Focus\n(.*?)\n", content, re.S)
    if focus_match:
        data["focus"] = focus_match.group(1).strip()
    
    # Extraer Tareas
    lines = content.splitlines()
    current_section = None
    for line in lines:
        if "### Pending" in line: current_section = "pending"
        elif "### In Progress" in line: current_section = "in_progress"
        elif "### Completed Today" in line: current_section = "completed"
        elif "## Notes & Decisions" in line: current_section = "notes"
        elif line.startswith("##"): current_section = None
        
        if line.strip().startswith("-"):
            task = line.strip()
            if current_section == "pending": data["pending"].append(task)
            elif current_section == "in_progress": data["in_progress"].append(task)
            elif current_section == "completed": data["completed"].append(task)
        elif current_section == "notes" and line.strip() and not line.startswith("##"):
            data["notes"] += line + "\n"

    return data

def generate_summary(data):
    if not data: return "Error: No data to summarize."
    
    summary = f"# Session Summary: {data['date']}\n\n"
    summary += f"## 🎯 Day's Focus\n{data['focus']}\n\n"
    
    summary += "## ✅ Accomplishments\n"
    for task in data["completed"]:
        summary += f"{task}\n"
    
    summary += "\n## 📝 Notes & Key Decisions\n"
    summary += data["notes"]
    
    summary += "\n## 🚀 Carry Forward (Tomorrow)\n"
    for task in data["in_progress"]:
        summary += f"{task} (In Progress)\n"
    for task in data["pending"]:
        summary += f"{task}\n"
        
    summary += f"\n## 📊 Metrics\n- Tasks Completed: {len(data['completed'])}\n"
    return summary

if __name__ == "__main__":
    data = parse_session()
    print(generate_summary(data))
