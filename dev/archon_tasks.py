#!/usr/bin/env python3
"""
Archon Task Management Script for Stuart Data Cleaner

This script provides task management following Archon workflow principles.
Use this to track progress and update task status.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def load_project():
    """Load the Archon project configuration"""
    project_file = Path(__file__).parent / "archon_project.json"
    if not project_file.exists():
        print("Project file not found. Run setup_archon_project.py first.")
        sys.exit(1)
    
    with open(project_file, 'r') as f:
        return json.load(f)

def show_task_status():
    """Show current task status"""
    project = load_project()
    
    print(f"Target: {project['project']['title']}")
    print(f"Phase: {project['project']['phase']}")
    print(f"Status: {project['project']['status']}")
    print("=" * 60)
    
    # Group tasks by status
    status_groups = {}
    for task in project['tasks']:
        status = task['status']
        if status not in status_groups:
            status_groups[status] = []
        status_groups[status].append(task)
    
    # Show tasks by status
    for status in ['doing', 'review', 'todo']:
        if status in status_groups:
            print(f"\n{status.upper()} ({len(status_groups[status])} tasks):")
            for task in status_groups[status]:
                print(f"  {task['priority']}. {task['title']}")
                print(f"     Estimated: {task['estimated_hours']} hours")
                print(f"     Dependencies: {', '.join(task['dependencies'])}")

def update_task_status(task_id: int, new_status: str):
    """Update task status following Archon workflow"""
    project = load_project()
    
    if task_id < 1 or task_id > len(project['tasks']):
        print(f"Invalid task ID: {task_id}")
        return
    
    task = project['tasks'][task_id - 1]
    old_status = task['status']
    
    # Validate status transition
    valid_transitions = {
        'todo': ['doing'],
        'doing': ['review'],
        'review': ['complete', 'doing']  # Can go back to doing if issues found
    }
    
    if new_status not in valid_transitions.get(old_status, []):
        print(f"Invalid status transition: {old_status} -> {new_status}")
        print(f"Valid transitions: {valid_transitions.get(old_status, [])}")
        return
    
    # Update task status
    task['status'] = new_status
    task['last_updated'] = datetime.now().isoformat()
    
    # Update project
    project['last_updated'] = datetime.now().isoformat()
    
    # Save updated project
    project_file = Path(__file__).parent / "archon_project.json"
    with open(project_file, 'w') as f:
        json.dump(project, f, indent=2)
    
    print(f"Task {task_id} status updated: {old_status} -> {new_status}")
    print(f"Title: {task['title']}")

def show_next_actions():
    """Show next actions based on current task status"""
    project = load_project()
    
    print("Next Actions:")
    print("=" * 40)
    
    # Find highest priority doing task
    doing_tasks = [t for t in project['tasks'] if t['status'] == 'doing']
    if doing_tasks:
        current_task = min(doing_tasks, key=lambda x: x['priority'])
        print(f"Current Focus: {current_task['title']}")
        print(f"   Priority: {current_task['priority']}")
        print(f"   Estimated: {current_task['estimated_hours']} hours")
        print(f"   Dependencies: {', '.join(current_task['dependencies'])}")
        print("\n   Acceptance Criteria:")
        for criterion in current_task['acceptance_criteria']:
            print(f"     * {criterion}")
    
    # Find next todo task
    todo_tasks = [t for t in project['tasks'] if t['status'] == 'todo']
    if todo_tasks:
        next_task = min(todo_tasks, key=lambda x: x['priority'])
        print(f"\nNext Task: {next_task['title']}")
        print(f"   Priority: {next_task['priority']}")
        print(f"   Dependencies: {', '.join(next_task['dependencies'])}")

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python archon_tasks.py status                    # Show task status")
        print("  python archon_tasks.py next                     # Show next actions")
        print("  python archon_tasks.py update <task_id> <status> # Update task status")
        print("\nExamples:")
        print("  python archon_tasks.py status")
        print("  python archon_tasks.py next")
        print("  python archon_tasks.py update 1 review")
        return
    
    command = sys.argv[1]
    
    if command == "status":
        show_task_status()
    elif command == "next":
        show_next_actions()
    elif command == "update" and len(sys.argv) == 4:
        task_id = int(sys.argv[2])
        new_status = sys.argv[3]
        update_task_status(task_id, new_status)
    else:
        print("Invalid command or arguments")
        print("Use 'python archon_tasks.py' for help")

if __name__ == "__main__":
    main()
