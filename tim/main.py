import argparse


from tim.tim import Tim, TimManager
from tim.event import EventDefinition, EventTable
from tim.project import ProjectTable, Project, Task


def handle_project_list(_):
    projects = ProjectTable.load()
    for project_id, project in projects.list_projects():
        print(f"{project_id}) {project.name}")
        for task_id, task in project.list_tasks():
            print(f"  {task_id} - {task.name}")


def handle_project_new(args):
    projects = ProjectTable.load()
    project_id = args.id
    project_name = args.name

    projects.add_project(Project(project_id, project_name))
    projects.save()


def handle_project_delete(args):
    projects = ProjectTable.load()
    project_id = args.id

    projects.remove_project(project_id)
    projects.save()


def handle_project_add(args):
    projects = ProjectTable.load()
    project_id = args.project_id
    task_id = args.task_id
    task_name = args.name

    prj = projects.get_project(project_id)
    if prj is not None:
        prj.add_task(Task(task_id, task_name))
        projects.save()


def handle_event_list(args):
    events = EventTable.load()
    projects = ProjectTable.load()
    for event_id, event in events.list_events():
        prj = projects.get_project(event.project_id)
        if prj is None:
            print(f"No project associated with event: {event_id}, {event}. ")
        else:
            task = prj.get_task(event.task_id)
            if task is None:
                print(f"Task id {event.task_id} not associated with project {prj}.")
            else:
                print(f"{event_id}) {prj.name} - {task.name}: {event.description}")


def handle_event_add(args):
    events = EventTable.load()
    project_id = args.project_id
    task_id = args.task_id
    description = args.description

    events.add_event(EventDefinition(project_id, task_id, description))
    events.save()


def handle_event_delete(args):
    events = EventTable.load()
    events.delete_event(args.id)
    events.save()


def handle_log_list(args):
    logs = TimManager.load()
    for date, log in logs.list_logs():
        print(f"{date}")


def handle_log_start(args):
    projects = ProjectTable.load()
    events = EventTable.load()
    logs = TimManager.load()
    log = logs.start(args.event)
    log.save()
    log.show(projects, events)


def handle_log_show(args):
    projects = ProjectTable.load()
    events = EventTable.load()
    logs = TimManager.load()
    id = args.log
    if id is None:
        log = logs.latest()
    else:
        log = logs.get_log(id)

    log.show(projects, events)


def handle_log_delete(args):
    logs = TimManager.load()
    id = args.log
    logs.delete(id)


def handle_log_stop(args):
    projects = ProjectTable.load()
    events = EventTable.load()
    logs = TimManager.load()
    log = logs.latest()
    log.stop()
    log.save()
    log.show(projects, events)


def handle_log_export(args):
    projects = ProjectTable.load()
    events = EventTable.load()
    logs = TimManager.load()
    log = logs.latest()
    print(log.export(events))


def handle_log_add(args):
    projects = ProjectTable.load()
    events = EventTable.load()
    logs = TimManager.load()
    log = logs.latest()
    log.add(args.event)
    log.save()
    log.show(projects, events)


def handle_log_edit_time(args):
    projects = ProjectTable.load()
    events = EventTable.load()
    logs = TimManager.load()
    log = logs.latest()
    vals = {
        "year": args.year,
        "month": args.month,
        "day": args.day,
        "hour": args.hour,
        "minute": args.minute,
    }
    log.update_time(args.position, **vals)
    log.save()
    log.show(projects, events)


def handle_log_edit_event(args):
    projects = ProjectTable.load()
    events = EventTable.load()
    logs = TimManager.load()
    log = logs.latest()
    position = args.position
    val = args.id
    log.update_event(position, val)
    log.save()
    log.show(projects, events)


def main():
    """
    want an interface that acts something like

    tim project new id name
    tim project delete id
    tim project add project_id task_id task_name
    tim project list


    """
    parser = argparse.ArgumentParser(description="Tool for time logging.")
    # needed so the func can just be called for all parsers
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    #
    # Project interface
    #
    parser_project = subparsers.add_parser(
        "project", description="The interface for working with projects."
    )
    parser_project.set_defaults(func=lambda _: parser_project.print_help())

    project_commands = parser_project.add_subparsers()
    project_list = project_commands.add_parser(
        "list", description="List projects and their respective tasks."
    )
    project_list.set_defaults(func=handle_project_list)

    project_new = project_commands.add_parser("new", description="Add a new project.")
    project_new.set_defaults(func=handle_project_new)
    project_new.add_argument("id", type=int, help="The id of the project.")
    project_new.add_argument("name", type=str, help="The name of the project.")

    project_delete = project_commands.add_parser(
        "delete", description="Delete an existing project."
    )
    project_delete.set_defaults(func=handle_project_delete)
    project_delete.add_argument("id", type=int, help="The id of the project to delete.")

    project_add = project_commands.add_parser(
        "add", description="Add a task to a project."
    )
    project_add.set_defaults(func=handle_project_add)
    project_add.add_argument(
        "project_id", type=int, help="The project id to add the task to."
    )
    project_add.add_argument("task_id", type=int, help="The id of the task to add.")
    project_add.add_argument("name", type=str, help="The name of the task to add.")

    #
    # Events interface
    #

    parser_event = subparsers.add_parser(
        "event", description="The interface for working with events."
    )
    parser_event.set_defaults(func=lambda _: parser_event.print_help())

    event_commands = parser_event.add_subparsers()
    event_list = event_commands.add_parser(
        "list", description="List currently defined events."
    )
    event_list.set_defaults(func=handle_event_list)

    event_add = event_commands.add_parser("add", description="Add an event definition.")
    event_add.add_argument("project_id", type=int, help="The project for the event.")
    event_add.add_argument("task_id", type=int, help="The task id for the event.")
    event_add.add_argument("description", type=str, help="The description of the task.")
    event_add.set_defaults(func=handle_event_add)

    event_delete = event_commands.add_parser(
        "delete", description="Delete an event definition."
    )
    event_delete.add_argument("id", type=int, help="The id of the event to delete.")
    event_delete.set_defaults(func=handle_event_delete)

    #
    # Log interface
    #
    parser_log = subparsers.add_parser(
        "log", description="The interface for working with logs."
    )
    parser_log.set_defaults(func=lambda _: parser_log.print_help())

    log_commands = parser_log.add_subparsers()
    log_list = log_commands.add_parser(
        "list", description="List the currently created logs."
    )
    log_list.set_defaults(func=handle_log_list)

    log_start = log_commands.add_parser("start", description="Start a new log.")
    log_start.add_argument("--event", type=int, help="The initial event to start with.")
    log_start.set_defaults(func=handle_log_start)

    log_show = log_commands.add_parser(
        "show", description="Show the current values in the log."
    )
    log_show.add_argument("--log", type=str, help="The date for the log to show")
    log_show.set_defaults(func=handle_log_show)

    log_delete = log_commands.add_parser(
        "delete", description="Delete the specified log."
    )
    log_delete.add_argument("log", type=str, help="The log to delete")
    log_delete.set_defaults(func=handle_log_delete)

    log_stop = log_commands.add_parser(
        "stop", description="Stop the current log. Sets the final timestep to be done."
    )
    log_stop.set_defaults(func=handle_log_stop)

    log_export = log_commands.add_parser(
        "export", description="Export the log to a csv to be uploaded."
    )
    log_export.set_defaults(func=handle_log_export)

    log_add = log_commands.add_parser(
        "add", description="Add a new event to the end of the log."
    )
    log_add.add_argument("event", type=int, help="The event id to add")
    log_add.set_defaults(func=handle_log_add)

    log_edit = log_commands.add_parser(
        "edit",
        description="Edit a part of a log.",
    )
    log_edit.set_defaults(func=lambda _: log_edit.print_help())
    log_edit_commands = log_edit.add_subparsers()
    log_edit_time = log_edit_commands.add_parser(
        "time", description="Edit the time fields."
    )
    log_edit_time.add_argument(
        "position", type=int, help="The position of the time to edit in the log."
    )
    log_edit_time.add_argument(
        "--minute", type=int, help="The minute value to update to."
    )
    log_edit_time.add_argument("--hour", type=int, help="The hour value to update to.")
    log_edit_time.add_argument("--day", type=int, help="The day value to update to.")
    log_edit_time.add_argument(
        "--month", type=int, help="The month value to update to."
    )
    log_edit_time.add_argument("--year", type=int, help="The year value to update to.")
    log_edit_time.set_defaults(func=handle_log_edit_time)

    log_edit_event = log_edit_commands.add_parser(
        "event", description="Edit the event fields."
    )
    log_edit_event.add_argument(
        "position", type=int, help="The position of the event to edit."
    )
    log_edit_event.add_argument("id", type=int, help="The event to update to.")
    log_edit_event.set_defaults(func=handle_log_edit_event)

    args = parser.parse_args()
    args.func(args)

    # projects = ProjectTable.load()

    # print(projects)
