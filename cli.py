#!/usr/bin/env python3
"""
Command-Line Interface for Workspace Assistant
"""

import argparse
import json
import sys
from workspace_assistant import WorkspaceAssistant, BlockedOperationError, ConfirmationRequiredError

def main():
    parser = argparse.ArgumentParser(description="Workspace Assistant CLI for Google Workspace")
    subparsers = parser.add_subparsers(dest="service", help="Workspace Service")

    # Gmail
    gmail_parser = subparsers.add_parser("gmail", help="Gmail operations")
    gmail_sub = gmail_parser.add_subparsers(dest="action")
    gmail_sub.add_parser("profile", help="Get user profile")
    
    list_msg = gmail_sub.add_parser("list", help="List messages")
    list_msg.add_argument("--query", "-q", default="", help="Search query")
    list_msg.add_argument("--max", type=int, default=10, help="Max results")

    draft_msg = gmail_sub.add_parser("draft", help="Create a draft")
    draft_msg.add_argument("--to", required=True)
    draft_msg.add_argument("--subject", required=True)
    draft_msg.add_argument("--body", required=True)

    send_msg = gmail_sub.add_parser("send", help="Send email")
    send_msg.add_argument("--to", required=True)
    send_msg.add_argument("--subject", required=True)
    send_msg.add_argument("--body", required=True)
    send_msg.add_argument("--confirmed", action="store_true", help="Explicit user confirmation")

    # Calendar
    cal_parser = subparsers.add_parser("calendar", help="Calendar operations")
    cal_sub = cal_parser.add_subparsers(dest="action")
    
    cal_list = cal_sub.add_parser("list", help="List upcoming events")
    cal_list.add_argument("--max", type=int, default=10)

    cal_freebusy = cal_sub.add_parser("freebusy", help="Query availability")
    cal_freebusy.add_argument("--start", required=True, help="ISO start time")
    cal_freebusy.add_argument("--end", required=True, help="ISO end time")

    # Tasks
    tasks_parser = subparsers.add_parser("tasks", help="Tasks operations")
    tasks_sub = tasks_parser.add_subparsers(dest="action")
    tasks_sub.add_parser("list-lists", help="List task lists")
    
    tasks_list = tasks_sub.add_parser("list", help="List tasks")
    tasks_list.add_argument("--tasklist", default="@default")

    tasks_add = tasks_sub.add_parser("create", help="Create task")
    tasks_add.add_argument("--title", required=True)
    tasks_add.add_argument("--notes")
    tasks_add.add_argument("--due")

    # Drive
    drive_parser = subparsers.add_parser("drive", help="Drive operations")
    drive_sub = drive_parser.add_subparsers(dest="action")
    
    drive_list = drive_sub.add_parser("list", help="List files")
    drive_list.add_argument("--max", type=int, default=10)
    drive_list.add_argument("--query", "-q")

    drive_trash = drive_sub.add_parser("trash", help="Move file to trash")
    drive_trash.add_argument("--file-id", required=True)
    drive_trash.add_argument("--confirmed", action="store_true")

    args = parser.parse_args()
    if not args.service:
        parser.print_help()
        sys.exit(1)

    try:
        assistant = WorkspaceAssistant()
        if args.service == "gmail":
            if args.action == "profile":
                print(json.dumps(assistant.gmail.get_profile(), indent=2))
            elif args.action == "list":
                print(json.dumps(assistant.gmail.list_messages(query=args.query, max_results=args.max), indent=2))
            elif args.action == "draft":
                print(json.dumps(assistant.gmail.create_draft(to=args.to, subject=args.subject, body=args.body), indent=2))
            elif args.action == "send":
                print(json.dumps(assistant.gmail.send_message(to=args.to, subject=args.subject, body=args.body, confirmed=args.confirmed), indent=2))
        elif args.service == "calendar":
            if args.action == "list":
                print(json.dumps(assistant.calendar.list_events(max_results=args.max), indent=2))
            elif args.action == "freebusy":
                print(json.dumps(assistant.calendar.query_freebusy(time_min=args.start, time_max=args.end), indent=2))
        elif args.service == "tasks":
            if args.action == "list-lists":
                print(json.dumps(assistant.tasks.list_tasklists(), indent=2))
            elif args.action == "list":
                print(json.dumps(assistant.tasks.list_tasks(tasklist_id=args.tasklist), indent=2))
            elif args.action == "create":
                print(json.dumps(assistant.tasks.create_task(title=args.title, notes=args.notes, due=args.due), indent=2))
        elif args.service == "drive":
            if args.action == "list":
                print(json.dumps(assistant.drive.list_files(page_size=args.max, query=args.query), indent=2))
            elif args.action == "trash":
                print(json.dumps(assistant.drive.move_to_trash(file_id=args.file_id, confirmed=args.confirmed), indent=2))
    except (BlockedOperationError, ConfirmationRequiredError) as e:
        print(f"SECURITY GUARDRAIL TRIGGERED: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
