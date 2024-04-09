# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.
"""Cedric's note
As time was pressing to submit this in time there were improvements I did not have time to make.
There are certain operations like reading and writing to file that should also be incorporated
into functions as they may have been repeated in the individual functions.
Alternatively certain variables like the list of task directories should have been a global variable.
Also I would have liked to improve the presentation of the output but ran out of time."""
"""Pseudocode
Functions are described in docstrings, not psudocode, to make pseudocode more readable
First make imports
os was in the original file although the file may not need it as the files read
and written are in the same directory as the original file.
date and datetime are imported to enable analysis of the status of tasks.
Menu is a function called at the beginning of the function following succesful log in
It presents the user with options and calls the appropriate function.
It also generates the display statistics if required which was not put in a function
as task instructions did not say to do this.
When the user requests reports in the terminal it unpacks the tuple returned from the function called and
sends them to another function which displays them in an easy to read way in the terminal
Now all the functions have been defined and the actual programme starts
User.txt, the text file containing users and passwords
is created if it does not exist
Next a list of user names and their passwords is created which is turned into a list of user name password 
dictionaries
tasks.txt is read and turned into a global variable containing each task
The user is prompted to input their user name and password which are global variables
The validity of the inputs is checked and the user logged in if the entries are in order
Finally the menu function is called which allows the user to choose how they wish to proceed
"""

#=====importing libraries===========
import os
from datetime import date
from datetime import datetime
import ansi

# Clear screen
os.system('cls||clear')

DATETIME_STRING_FORMAT = "%Y-%m-%d"
today_date = date.today()

# Creates tasks.txt if it does not exist
if not os.path.exists("tasks.txt"):
    # Create an empty tasks.txt file
    with open("tasks.txt", "w") as task_file:
        pass

def menu()->None:
    """Called at start of programme to give user choice of functions.
    Made into a function as called repeatedly although not instructed to
    in task instructions."""
    while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    dr - Display reports in terminal
    e - Exit
    : ''').lower()

        if menu == "r":
            reg_user()

        elif menu == 'a':
            add_task()
            
        elif menu == 'va':
            view_all()    

        elif menu == 'vm':
            view_mine(task_list)

        elif menu == 'gr':
            user_report()

        elif menu == 'dr':
            tasks = read_tasks()
            if tasks:
                total_tasks, completed_tasks, incomplete_tasks, overdue_tasks, \
                incomplete_percentage, overdue_percentage, num_users, user_statistics = calculate_task_statistics(tasks)
                display_statistics(total_tasks, completed_tasks, incomplete_tasks, overdue_tasks,
                                incomplete_percentage, overdue_percentage, num_users, user_statistics)
            else:
                print("No tasks found. Please create tasks in 'tasks.txt'.")

        # This was not put into a new function as the instructions specified what had to be 
        # refactored to functions
        elif menu == 'ds' and curr_user == 'admin': 
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            print(35 * "-")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print(35 * "-")    

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")


def user_report()->None:
    """Displays statistics including number of users and task status and is called from the main menu"""
    users = []
    with open('user.txt', 'r') as file:
        for line in file:
            user, _ = line.strip().split(';')
            users.append(user)
    
    tasks = []
    with open('tasks.txt', 'r') as file:
        for line in file:
            tasks.append(line.strip().split(';'))
    
    today_date = date.today()
    user_stats = {user: {'total_tasks': 0, 'completed': 0, 'incomplete': 0, 'overdue': 0} for user in users}

    for task in tasks:
        assigned_user = task[0]
        if assigned_user in user_stats:
            user_stats[assigned_user]['total_tasks'] += 1
            if task[4] == 'Yes':  # Assuming the completion status is at index 4
                user_stats[assigned_user]['completed'] += 1
            else:
                user_stats[assigned_user]['incomplete'] += 1
                due_date = datetime.strptime(task[3], "%Y-%m-%d").date()  # Assuming the due date is at index 3
                if due_date < today_date:
                    user_stats[assigned_user]['overdue'] += 1
    
    print(f"Total number of users: {len(users)}")
    for user, stats in user_stats.items():
        total_tasks = stats['total_tasks']
        print(f"\nUser: {user}")
        print(f"Total tasks: {total_tasks}")
        if total_tasks > 0:
            print(f"Completed tasks (%): {(stats['completed'] / total_tasks) * 100:.2f}%")
            print(f"Incomplete tasks (%): {(stats['incomplete'] / total_tasks) * 100:.2f}%")
            print(f"Overdue tasks (%): {(stats['overdue'] / total_tasks) * 100:.2f}%")
        else:
            print("Completed tasks (%): 0%")
            print("Incomplete tasks (%): 0%")
            print("Overdue tasks (%): 0%")
    
    # Ask if the user wants to write the report to a file
    while True:
        write_to_file = input("\nDo you want to write these results to a file? (Y/N) ").strip().lower()
        
        if write_to_file == 'y':
            write_user_report_to_file(users, user_stats)
            # Exit the loop after user selects "y"
            break  
        elif write_to_file == 'n':
            menu()
            # Exit the loop after user selects "n"
            break  
        else:
            print("Please enter 'Y' for yes or 'N' for no.")
    

def write_user_report_to_file(users, user_stats)->None:
    """Called by user_report if user selects it and the user report is written to task_overview.txt, 
    a text file in the same directory"""
    with open('user_overview.txt', 'w') as file:
        file.write(f"Total number of users: {len(users)}\n")
        for user, stats in user_stats.items():
            total_tasks = stats['total_tasks']
            file.write(f"\nUser: {user}\n")
            file.write(f"Total tasks: {total_tasks}\n")
            if total_tasks > 0:
                file.write(f"Completed tasks (%): {(stats['completed'] / total_tasks) * 100:.2f}%\n")
                file.write(f"Incomplete tasks (%): {(stats['incomplete'] / total_tasks) * 100:.2f}%\n")
                file.write(f"Overdue tasks (%): {(stats['overdue'] / total_tasks) * 100:.2f}%\n")
            else:
                file.write("Completed tasks (%): 0%\n")
                file.write("Incomplete tasks (%): 0%\n")
                file.write("Overdue tasks (%): 0%\n")


def mark_task_as_complete(task_number)->None:
    """This function translates the user's task number to the numer it has in tasks.txt and marks it complete"""
    task_number = int(task_number)  
    # List to hold all tasks from the file
    global_tasks = []  
    # List to hold indices of the user's tasks within the global task list
    user_tasks_indices = []  
    
    # Step 1: Load tasks from the file and identify user-specific tasks
    with open("tasks.txt", "r") as file:
        for index, line in enumerate(file):
            parts = line.strip().split(';')
            task = {
                'username': parts[0],
                'title': parts[1],
                'description': parts[2],
                'due_date': datetime.strptime(parts[3], DATETIME_STRING_FORMAT),
                'assigned_date': datetime.strptime(parts[4], DATETIME_STRING_FORMAT),
                'completed': parts[5] == 'Yes'
            }
            global_tasks.append(task)
            if task['username'] == curr_user:  # Check if the task belongs to the current user
                user_tasks_indices.append(index)  # Save the global index of the user's tasks

    # Step 2: Check if the user's task number is valid and mark the task as complete
    if 0 <= task_number - 1 < len(user_tasks_indices):
        global_index = user_tasks_indices[task_number - 1]  # Get the global index of the user's specific task
        global_tasks[global_index]['completed'] = True  # Mark the task as complete
        print(f"Task {task_number} marked as complete.")
    else:
        print(f"Task {task_number} not found for user {curr_user}.")

    # Step 3: Write the modified list back to the file
    with open("tasks.txt", "w") as file:
        for task in global_tasks:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            file.write(";".join(str_attrs) + "\n")

    menu()


def change_description(task_number)->None:
    """Allows user to change the description of the task in tasks.txt file"""
    task_number = int(task_number)
    # Step 1: Read existing tasks into a list of dictionaries
    task_list = []
    user_specific_tasks = []  # Tasks specific to the current user
    with open("tasks.txt", "r") as file:
        for line in file:
            parts = line.strip().split(';')
            task = {
                'username': parts[0],
                'title': parts[1],
                'description': parts[2],
                'due_date': datetime.strptime(parts[3], DATETIME_STRING_FORMAT),
                'assigned_date': datetime.strptime(parts[4], DATETIME_STRING_FORMAT),
                'completed': parts[5] == 'Yes'
            }
            task_list.append(task)
            if task['username'] == curr_user:
                user_specific_tasks.append(task)

    # Step 2: Modify the specified task's description
    # Adjust for the list of tasks specific to the current user
    if 0 <= task_number - 1 < len(user_specific_tasks):
        task_to_modify = user_specific_tasks[task_number - 1]
        # Find this task in the original list to get its actual index
        task_index = task_list.index(task_to_modify)
        
        confirm = input(f"The description to be changed is {task_list[task_index]['description']}, Y/N?  ")
        if confirm.lower() != "y" and confirm.lower() != "n":
            # Call the function that called this one if an invalid input was provided
            view_mine(task_list)  
        else:
            new_description = input("Please input the new task description  \n")
            print(f"The new description is {new_description}")
            task_list[task_index]["description"] = new_description
            print(f"Task description changed.")
    else:
        print(f"Task {task_number} not found or not available.")

    # Step 3: Write the modified list of tasks back to 'tasks.txt'
    with open("tasks.txt", "w") as file:
        for task in task_list:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            file.write(";".join(str_attrs) + "\n")

    menu()
      

def reg_user()->None:
    """Allows the user to register a new user with password. It checks the passwords match
    and adds the new user name and password to the user.txt file in the same directory"""
    new_username = input("New Username: ")

    with open("user.txt", "r") as out_file:
        # Initialize an empty list to store usernames
        users = []  
        for line in out_file:
            # Split each line by semicolon and extract the username
            username, _ = line.strip().split(";")  
            users.append(username)  # Append the username to the list

    if new_username in users:
        print(f"{new_username} is already registered")
        print("Please choose a new username")
        reg_user()
                
    else:
        # Request input of a new password from user
        new_password = input("New Password: ")

        # Request input of password confirmation from user
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If the same add to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
                        
            with open("user.txt", "w") as out_file:
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
             
        # If passwords do not match
        else:
            print("""Passwords do no match
            Please try again
                """)
            reg_user()


def add_task()->None:
    """Appends a new task to the task list by reading the task file, adding the correctly formatted
    new task and writing it to disk overwriting the old file"""
    task_list = []
    
    # First read existing tasks from the file
    try:
        with open("tasks.txt", "r") as task_file:
            for line in task_file:
                username, title, description, due_date_str, assigned_date_str, completed_str = line.strip().split(";")
                task_list.append({
                    "username": username,
                    "title": title,
                    "description": description,
                    "due_date": datetime.strptime(due_date_str, DATETIME_STRING_FORMAT),
                    "assigned_date": datetime.strptime(assigned_date_str, DATETIME_STRING_FORMAT),
                    "completed": completed_str == "Yes"
                })
    except FileNotFoundError:
        # If tasks.txt not exist start with an empty task list
        print("No existing tasks found. Creating new tasks file.")

    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            # Check date format is correct to prevent programme ending
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        curr_date = date.today()
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)

        with open("tasks.txt", "w") as task_file:
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_file.write(";".join(str_attrs) + "\n")

        print("Task successfully added.")
        break  


def change_username(task_number)->None:
    """Called by view_mine() when the user wishes to change the username of the person to whom 
    one of their tasks is allocated. It translates the user's task number to the task
    number in tasks.txt and then writes the new set of tasks to file."""
    task_number = int(task_number)  # User's task index

    # Read existing tasks into a list of dictionaries
    task_list = []
    # Define empty list to store indeces of tasks assigned to curr_user
    user_task_indexes = []  
    with open("tasks.txt", "r") as file:
        for index, line in enumerate(file):
            parts = line.strip().split(';')
            task = {
                'username': parts[0],
                'title': parts[1],
                'description': parts[2],
                'due_date': datetime.strptime(parts[3], DATETIME_STRING_FORMAT),
                'assigned_date': datetime.strptime(parts[4], DATETIME_STRING_FORMAT),
                'completed': parts[5] == 'Yes'
            }
            task_list.append(task)
            if task['username'] == curr_user:
                user_task_indexes.append(index)  # Store index of curr_user's task

    # Translate user-specific task_number to global index in task_list
    try:
        global_task_index = user_task_indexes[task_number - 1]
    except IndexError:
        print("Invalid task number for the current user.")
        return

    # Confirm with the user before changing the username
    confirm = input(f"The username to be changed is {task_list[global_task_index]['username']}, Y/N?  ")
    if confirm.lower() == 'y':
        new_user_name = input("Please input the new user name: ")
        print(f"The new user name is {new_user_name}")
        task_list[global_task_index]['username'] = new_user_name
        print("User name changed.")
    elif confirm.lower() == 'n':
        return
    else:
        print("Please input Y or N.")
        return

    # Write the modified list of tasks back to 'tasks.txt'
    with open("tasks.txt", "w") as file:
        for task in task_list:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            file.write(";".join(str_attrs) + "\n")

    menu()


def view_all()->None:             
            '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
            ''' 
            with open("tasks.txt", 'r') as task_file:
                task_data = task_file.read().split("\n")
                task_data = [t for t in task_data if t != ""]

                task_list = []
                for t_str in task_data:
                    curr_t = {}

                    # Split by semicolon and manually add each component
                    task_components = t_str.split(";")
                    curr_t['username'] = task_components[0]
                    curr_t['title'] = task_components[1]
                    curr_t['description'] = task_components[2]
                    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
                    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
                    curr_t['completed'] = True if task_components[5] == "Yes" else False

                    task_list.append(curr_t)
                    for t in task_list:
                        disp_str = f"Task: \t\t {t['title']}\n"
                        disp_str += f"Assigned to: \t {t['username']}\n"
                        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                        disp_str += f"Task Description: \n {t['description']}\n"
                        print(disp_str)
                        

def view_mine(task_list)->None:
    """Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling). It also allows the user to change the username, the 
    description or the due date of a task as long as it has not yet been completed
    """
    # Make disp_str an empty string before the loop
    disp_str = ""  
    index = 1
    for t in task_list:
        if t['username'] == curr_user:
            disp_str += f"Task number = {index}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n\n"
            index += 1
    print(disp_str)
    
    view_specific_task = input("View specific task? Y/N or -1 for main menu: ")
    if view_specific_task.lower() != "y" and view_specific_task.lower() != "n" and view_specific_task.lower() != "-1":
        print("Please input Y or N")
        view_mine(task_list)
    elif view_specific_task.lower() == "n" and view_specific_task.lower() == "-1":
        pass
    elif view_specific_task.lower() == "y":
        task_to_change = input("Which number task would you like to change?  ")
        if task_to_change.isdigit() and int(task_to_change) > 0 and int(task_to_change) <= index:
            print(f"You would like to edit, mark complete or change task description {task_to_change}?")
            edit_complete = input("Would you like to edit (E) or mark this task as completed (C)? E/C  " )
            if edit_complete.lower() != "c" and edit_complete.lower() != "e":
                print("Please input E or C")
                view_mine(task_list)
            elif edit_complete.lower() == "c":
                mark_task_as_complete(int(task_to_change))
            elif edit_complete.lower() == "e":
                # Has task been completed?
                print("You can only make these changes if task not yet completed")
                if not check_if_user_task_completed(int(task_to_change)):
                                                while True:
                                                    edit_chosen = input("""Please select your choice below
                                                    1 - Change Username
                                                    2 - Change Description
                                                    3 - Change Due Date
                                                    4 - Return to main menu\n""")
                                                    
                                                    if edit_chosen == "1":
                                                        change_username(task_to_change)
                                                    elif edit_chosen == "2":
                                                        change_description(task_to_change)
                                                    elif edit_chosen == "3":
                                                        change_due_date(task_to_change)
                                                    elif edit_chosen == "4":
                                                        menu()
                                                    else:
                                                        print("Please make a valid input, D or U")
                else:
                    print("That task is complete, please choose another task\n")
                    view_mine(task_list)
             
        else:
            view_mine(task_list)


def change_due_date(task_number)->None:
    """Called from view_mine function if user wishes to change due date
    and has to translate the user's task number to the task number in tasks.txt"""
    task_number = int(task_number)
    # Step 1: Read existing tasks into a list of dictionaries
    task_list = []
    # Indeces of tasks specific to the current user in the global list
    user_task_indices = []  
    with open("tasks.txt", "r") as file:
        for index, line in enumerate(file):
            parts = line.strip().split(';')
            task = {
                'username': parts[0],
                'title': parts[1],
                'description': parts[2],
                'due_date': datetime.strptime(parts[3], DATETIME_STRING_FORMAT),
                'assigned_date': datetime.strptime(parts[4], DATETIME_STRING_FORMAT),
                'completed': parts[5] == 'Yes'
            }
            task_list.append(task)
            if task['username'] == curr_user:
                user_task_indices.append(index)  # Save index of user's tasks

    # Validate the task number for the current user
    if 0 <= task_number - 1 < len(user_task_indices):
        global_task_index = user_task_indices[task_number - 1]  # Get the global index of the user's task

        # Step 2: Modify the specified task's due date
        new_due_date_str = input("Please enter the new due date (YYYY-MM-DD): ")
        try:
            new_due_date = datetime.strptime(new_due_date_str, DATETIME_STRING_FORMAT)
            task_list[global_task_index]['due_date'] = new_due_date
            print(f"Due date changed to {new_due_date_str}.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
            return
    else:
        print(f"Task {task_number} not found or not available for user {curr_user}.")

    # Step 3: Write the modified list of tasks back to 'tasks.txt'
    with open("tasks.txt", "w") as file:
        for task in task_list:
            str_attrs = [
                task['username'],
                task['title'],
                task['description'],
                task['due_date'].strftime(DATETIME_STRING_FORMAT),
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if task['completed'] else "No"
            ]
            file.write(";".join(str_attrs) + "\n")


def check_if_user_task_completed(task_number)->bool:
    """Called by view_mine to allow the user to change the user name and other information about the task.
    Checks if a specific task for a user is marked as completed based on the user's task number and
    returns a Boolean value indicating whether the task is completed. This value is returned to
    view_mine and it allows editing depending on whether task is completed"""
    user_tasks = []  

    # Step 1: Load and filter tasks for the given user
    with open("tasks.txt", "r") as file:
        for line in file:
            parts = line.strip().split(';')
            if parts[0] == curr_user:
                task = {
                    'username': parts[0],
                    'title': parts[1],
                    'description': parts[2],
                    'due_date': datetime.strptime(parts[3], DATETIME_STRING_FORMAT),
                    'assigned_date': datetime.strptime(parts[4], DATETIME_STRING_FORMAT),
                    'completed': parts[5] == 'Yes'
                }
                user_tasks.append(task)
    
    # Step 2: Adjust task number for zero-based indexing and check if it exists within user's tasks
    task_number -= 1
    if 0 <= task_number < len(user_tasks):
        task_completed = user_tasks[task_number]['completed']
        # Returns completion status (True/False) which view_mine uses to allow changes
        return task_completed  
    else:
        print(f"Task {task_number + 1} not found for user {curr_user}.")
        return None


def read_tasks()->list:
    """Checks if tasks file exists. Tells user to enter tasks if does not.
    if tasks file exists puts contents into list of dictionaries and returns
    list to menu function for unpacking"""
    tasks = []
    try:
        with open('tasks.txt', 'r') as file:
            for line in file:
                user, task, description, due_date, assigned_date, completed = line.strip().split(';')
                task_dict = {
                    'user': user,
                    'task': task,
                    'description': description,
                    'due_date': due_date,
                    'assigned_date': assigned_date,
                    'completed': completed == 'Yes'
                }
                tasks.append(task_dict)
        return tasks
    except FileNotFoundError:
        print("Tasks File does not exist. Enter some tasks")
        return []

def calculate_task_statistics(tasks: list)->tuple:
    """Calculates task statistics which are unpacked in menu function"""
    total_tasks = len(tasks)
    completed_tasks = sum(task['completed'] for task in tasks)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in tasks if not task['completed'] and task['due_date'] < task['assigned_date'])

    # Calculate percentages
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    # User statistics
    user_stats = {}
    for task in tasks:
        user = task['user']
        if user not in user_stats:
            user_stats[user] = {'total': 0, 'completed': 0}
        user_stats[user]['total'] += 1
        user_stats[user]['completed'] += 1 if task['completed'] else 0

    # Calculate user percentages
    for user, stats in user_stats.items():
        stats['assigned_percentage'] = (stats['total'] / total_tasks) * 100
        stats['completed_percentage'] = (stats['completed'] / stats['total']) * 100

    return total_tasks, completed_tasks, incomplete_tasks, overdue_tasks, \
           incomplete_percentage, overdue_percentage, len(user_stats), user_stats

def display_statistics(total_tasks, completed_tasks, incomplete_tasks, overdue_tasks,
                       incomplete_percentage, overdue_percentage, num_users, user_stats):
    """Prints the various statistics to the terminal in an easy to read format"""
    print("Task Statistics:")
    print("-" * 40)
    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Incomplete Tasks: {incomplete_tasks}")
    print(f"Overdue Tasks: {overdue_tasks}")
    print(f"Percentage of Incomplete Tasks: {incomplete_percentage:.2f}%")
    print(f"Percentage of Overdue Tasks: {overdue_percentage:.2f}%")
    print(f"Total Users: {num_users}")
    print("\nUser Statistics:")
    print("-" * 40)
    for user, stats in user_stats.items():
        print(f"User: {user}")
        print(f"Total Tasks Assigned: {stats['total']}")
        print(f"Percentage of Total Tasks Assigned: {stats['assigned_percentage']:.2f}%")
        print(f"Percentage of Completed Tasks: {stats['completed_percentage']:.2f}%")
        print("-" * 40)


   
#====Login Section====
'''This code reads usernames and password from the user.txt file to 
allow a user to login.'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read user_data from user.txt which is in same directory
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    
username_password = {}
for user in user_data:
    username, password = user_data[0].split(";")
    username_password[username] = password

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

logged_in = False

while not logged_in:
    try:
        curr_user = ""
        with open("user.txt", "r") as out_file:
            # Define an empty list for user data
            user_data = []  
            # Define an empty dictionary for username-password pairs
            username_password = {}  

            # Read existing user data from file
            for line in out_file:
                username, password = line.strip().split(";")
                username_password[username] = password

            print("LOGIN")
            curr_user = input("Username: ")
            curr_pass = input("Password: ")

            if curr_user not in username_password:
                print("User does not exist")
            elif username_password[curr_user] != curr_pass:
                print("Wrong password")
            else:
                print("Login Successful!")
                logged_in = True
    except FileNotFoundError:
        print("User data file not found. Please create 'user.txt' with username-password pairs.")


# Calls menu function so user can start using the programme
menu()
