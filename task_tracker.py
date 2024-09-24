# task_tracker
import json
import argparse
import os
import datetime

#adds argparser
parser = argparse.ArgumentParser(prog='Task Tracker', description='Adds tasks into a list', epilog='Example command: --')

#adds argparser args
parser.add_argument('-a', '--add', help='Adds description to the task', required=False)
parser.add_argument('-l', '--list', help='type -l or --list "todo", "in-progress" or "all" to view tasks', required=False)
parser.add_argument('-u', '--update', help='Type new task description', required=False)
parser.add_argument('-p', '--pick', help='Pick the task ID', required=False)
parser.add_argument('-m', '--mark', help='Mark task as in-progress or done', required=False)
parser.add_argument('-d', '--delete', help='Type ID of task to delete', required=False)

#Process given args
args = parser.parse_args()

#access given args, debug
print(f'Added: {args.add if args.add else "No task added"}')
print(f'List: {args.list if args.list else "No list chosen"}')
print(f'Updated: {args.update if args.update else "No task updated"}')
print(f'Picked: {args.pick if args.pick else "No ID chosen"}')
print(f'Marked: {args.mark if args.mark else "No task marked"}')
print(f'Deleted: {args.delete if args.delete else "No task deleted"}')

file_path = 'tasks.json'

curr_time = datetime.datetime.now()
formatted_time = datetime.datetime.now().replace(microsecond=0).isoformat()

def list_tasks(status):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    if status == 'all':
        print(json.dumps(data, indent=4))
    
    elif status == 'todo':
        filter_tasks = [task for task in data if task.get('status') == 'todo']
        print(json.dumps(filter_tasks, indent=4))
    
    elif status == 'in-progress':
        filter_tasks = [task for task in data if task.get('status') == 'in-progress']
        print(json.dumps(filter_tasks, indent=4))

    elif status == 'done':
        filter_tasks = [task for task in data if task.get('status') == 'done']
        print(json.dumps(filter_tasks, indent=4))
    
    else:
        print('Invalid input or unexpected error, try again')
        exit()

def add_task():
    desc = args.add

    if not os.path.exists(file_path):
        tasks = [
            {
                'id': 1,
                'description': desc,
                'status': 'todo',
                'createdAt': formatted_time,
                'updatedAt': formatted_time
            }
        ]
        with open(file_path, 'w') as file:
            json.dump(tasks, file, indent=4)
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)
            id_incr = max(task['id'] for task in data) if data else 0
            new_task = {
                'id': id_incr + 1,
                'description': args.add,
                'status': 'todo',
                'createdAt': formatted_time,
                'updatedAt': formatted_time
                }
            data.append(new_task)

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)


def update_task_mark():
    with open(file_path, 'r') as file:
            data = json.load(file)
            found_task = False
            for task in data:
                if task['id'] == int(args.pick):
                    task['status'] = str(args.mark)
                    task['updatedAt'] = formatted_time
                    found_task = True
                    break
        
            if found_task:
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                print(f'Task status on id {args.pick} has been marked as {args.mark}')


def update_task_desc():
    with open(file_path, 'r') as file:
            data = json.load(file)
            found_task = False
            for task in data:
                if task['id'] == int(args.pick):
                    task['description'] = str(args.update)
                    task['updatedAt'] = formatted_time
                    found_task = True
                    break
        
            if found_task:
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                print(f'Task description on id {args.pick} has been updated to "{args.update}"')

""" def delete_task():
with open(file_path, 'r') as file:
        data = json.load(file)

        remove_task = False
        for task in data:
            if task['id'] == int(args.delete):
                data.remove(remove_task)
                remove_task = True
                break
        
        if remove_task:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            print(f'Task with id {args.pick} has been deleted.') """


def delete_task():
    with open(file_path, 'r') as file:
            data = json.load(file)
            found_task = False
            for task in data:
                if task['id'] == int(args.delete):
                    task_to_remove = task
                    found_task = True
                    break
        
            if found_task:
                data.remove(task_to_remove)
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
                print(f'Task with ID {args.delete} has been removed')    


if args.add:
    add_task()

elif args.list:
    list_tasks(args.list)

elif args.update:
    update_task_desc()

elif args.delete:
    delete_task()

elif args.pick:
    if args.update:
        update_task_desc()
    elif args.mark:
        update_task_mark()
    else:
        parser.error('Specify either --update, --mark or --delete')

exit()
