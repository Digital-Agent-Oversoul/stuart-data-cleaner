#!/usr/bin/env python3
"""
Archon Project Initialization Script for Stuart Data Cleaner

This script initializes the Stuart project in Archon and sets up proper task tracking
following the Archon workflow principles.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Project configuration
PROJECT_CONFIG = {
    "title": "Stuart Data Cleaning System",
    "description": "Unified data cleaning engine with multiple workflows for customer contact processing",
    "github_repo": "github.com/stuart-org/data-cleaner",
    "project_type": "python",
    "phase": "Phase 1 - Core LLM Engine",
    "status": "active_development"
}

# Initial tasks following Archon principles
INITIAL_TASKS = [
    {
        "title": "Complete Core Data Processing Implementation",
        "description": "Implement the missing data processing logic in DataProcessor class",
        "priority": 1,
        "status": "doing",
        "estimated_hours": 6,
        "dependencies": ["core_engine", "configuration_system"],
        "acceptance_criteria": [
            "process_survey_data() method fully implemented",
            "process_contact_export_data() method fully implemented",
            "Data validation and error handling added",
            "Tested with sample datasets"
        ]
    },
    {
        "title": "Implement Workflow Processors",
        "description": "Complete the workflow processor implementations for Survey and Contact Export",
        "priority": 2,
        "status": "doing",
        "estimated_hours": 4,
        "dependencies": ["core_data_processing", "llm_engine"],
        "acceptance_criteria": [
            "SurveyProcessor.process_survey_data() completed",
            "ExportProcessor.process_contact_export() completed",
            "Location-based filtering logic implemented",
            "Date range filtering logic implemented"
        ]
    },
    {
        "title": "CLI Interface Testing and Validation",
        "description": "Test the CLI interface with real data and validate output generation",
        "priority": 3,
        "status": "review",
        "estimated_hours": 2,
        "dependencies": ["core_processing", "workflow_processors"],
        "acceptance_criteria": [
            "CLI interface tested with sample data files",
            "Output generation validated",
            "Error handling tested",
            "Performance benchmarks established"
        ]
    },
    {
        "title": "Data Validation and Error Handling",
        "description": "Implement comprehensive data validation and error handling",
        "priority": 4,
        "status": "todo",
        "estimated_hours": 3,
        "dependencies": ["core_processing_implementation"],
        "acceptance_criteria": [
            "Input data validation implemented",
            "Error recovery mechanisms added",
            "User-friendly error messages created",
            "Error logging system established"
        ]
    },
    {
        "title": "Output Management System",
        "description": "Implement comprehensive output file management",
        "priority": 5,
        "status": "todo",
        "estimated_hours": 3,
        "dependencies": ["core_processing", "cli_interface"],
        "acceptance_criteria": [
            "Output directory structure created",
            "File naming conventions implemented",
            "Output format options added",
            "Processing summary reports generated"
        ]
    },
    {
        "title": "Integration Testing",
        "description": "End-to-end testing of complete workflows",
        "priority": 6,
        "status": "todo",
        "estimated_hours": 4,
        "dependencies": ["all_core_functionality"],
        "acceptance_criteria": [
            "Integration test suite created",
            "Survey workflow tested end-to-end",
            "Contact Export workflow tested end-to-end",
            "Output quality and accuracy validated"
        ]
    }
]

def create_archon_project_file():
    """Create Archon project configuration file"""
    project_file = Path(__file__).parent / "archon_project.json"
    
    project_data = {
        "project": PROJECT_CONFIG,
        "tasks": INITIAL_TASKS,
        "created": "2025-01-21T00:00:00Z",
        "last_updated": "2025-01-21T00:00:00Z",
        "archon_version": "1.0.0"
    }
    
    with open(project_file, 'w') as f:
        json.dump(project_data, f, indent=2)
    
    print(f"✅ Created Archon project file: {project_file}")
    return project_file

def create_task_management_script():
    """Create script to manage tasks following Archon principles"""
    script_content = '''#!/usr/bin/env python3
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
        print("❌ Project file not found. Run setup_archon_project.py first.")
        sys.exit(1)
    
    with open(project_file, 'r') as f:
        return json.load(f)

def show_task_status():
    """Show current task status"""
    project = load_project()
    
    print(f"🎯 {project['project']['title']}")
    print(f"📊 Phase: {project['project']['phase']}")
    print(f"🔄 Status: {project['project']['status']}")
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
            print(f"\\n{status.upper()} ({len(status_groups[status])} tasks):")
            for task in status_groups[status]:
                print(f"  {task['priority']}. {task['title']}")
                print(f"     Estimated: {task['estimated_hours']} hours")
                print(f"     Dependencies: {', '.join(task['dependencies'])}")

def update_task_status(task_id: int, new_status: str):
    """Update task status following Archon workflow"""
    project = load_project()
    
    if task_id < 1 or task_id > len(project['tasks']):
        print(f"❌ Invalid task ID: {task_id}")
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
        print(f"❌ Invalid status transition: {old_status} → {new_status}")
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
    
    print(f"✅ Task {task_id} status updated: {old_status} → {new_status}")
    print(f"📝 {task['title']}")

def show_next_actions():
    """Show next actions based on current task status"""
    project = load_project()
    
    print("🚀 Next Actions:")
    print("=" * 40)
    
    # Find highest priority doing task
    doing_tasks = [t for t in project['tasks'] if t['status'] == 'doing']
    if doing_tasks:
        current_task = min(doing_tasks, key=lambda x: x['priority'])
        print(f"🎯 Current Focus: {current_task['title']}")
        print(f"   Priority: {current_task['priority']}")
        print(f"   Estimated: {current_task['estimated_hours']} hours")
        print(f"   Dependencies: {', '.join(current_task['dependencies'])}")
        print("\\n   Acceptance Criteria:")
        for criterion in current_task['acceptance_criteria']:
            print(f"     • {criterion}")
    
    # Find next todo task
    todo_tasks = [t for t in project['tasks'] if t['status'] == 'todo']
    if todo_tasks:
        next_task = min(todo_tasks, key=lambda x: x['priority'])
        print(f"\\n📋 Next Task: {next_task['title']}")
        print(f"   Priority: {next_task['priority']}")
        print(f"   Dependencies: {', '.join(next_task['dependencies'])}")

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python archon_tasks.py status                    # Show task status")
        print("  python archon_tasks.py next                     # Show next actions")
        print("  python archon_tasks.py update <task_id> <status> # Update task status")
        print("\\nExamples:")
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
        print("❌ Invalid command or arguments")
        print("Use 'python archon_tasks.py' for help")

if __name__ == "__main__":
    main()
'''
    
    script_file = Path(__file__).parent / "archon_tasks.py"
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    # Make executable
    script_file.chmod(0o755)
    
    print(f"✅ Created Archon task management script: {script_file}")
    return script_file

def main():
    """Main initialization function"""
    print("🚀 Initializing Stuart Data Cleaner Project in Archon")
    print("=" * 60)
    
    # Create project file
    project_file = create_archon_project_file()
    
    # Create task management script
    task_script = create_task_management_script()
    
    print("\\n✅ Archon project initialization complete!")
    print("\\n📋 Next Steps:")
    print("1. Review project configuration in archon_project.json")
    print("2. Use archon_tasks.py to manage tasks:")
    print("   python archon_tasks.py status    # View current status")
    print("   python archon_tasks.py next      # View next actions")
    print("   python archon_tasks.py update 1 review  # Update task status")
    print("\\n🎯 Current Focus: Task 1 - Complete Core Data Processing Implementation")
    print("   Status: doing")
    print("   Estimated: 6 hours")
    print("   Dependencies: core_engine, configuration_system")

if __name__ == "__main__":
    main()
