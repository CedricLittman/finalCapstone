# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.
# Code Fix

#=====importing libraries===========
import os
from datetime import date
from datetime import datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"
today_date = date.today()


def menu():
    # Used
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
    e - Exit
    : ''').lower()

        if menu == "r":
            reg_user()

        elif menu == 'a':
            add_task(menu)
            
        elif menu == 'va':
            view_all()    

        elif menu == 'vm':
            view_mine()

        elif menu == 'gr':
            generate_reports()

        elif menu == 'ds' and curr_user == 'admin': 
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            num_users = len(username_password.keys())
            num_tasks = len(task_list)

            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")    

        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")

    


def check_tasks_status(tasks):
    # Get the current date
    today = datetime.now().date()
    
    for task in tasks:
        person = task[0]
        task_name = task[1]
        due_date = datetime.strptime(task[3], '%Y-%m-%d').date()
        completed = task[-1] == 'Yes'
        
        # Check if the task is complete
        if completed:
            print(f"{person}'s task '{task_name}' is complete.")
        elif today > due_date and not completed:
            print(f"{person}'s task '{task_name}' is overdue.")
        else:
            print(f"{person}'s task '{task_name}' is not due yet.")



def generate_reports():
    print("""This allows you to generate reports on the users or the tasks
          to be written to text files """)
    report = input("Please enter 1 for user report or 2 for task report  ")
    if report.isdigit() and report != "0" and report !="3":
        print(f"report is {report}")
        if report == "1":
            calculate_task_statistics()
        elif report == "2":
            user_report()
    else:
        print("please enter 1 or 2")
        generate_reports()


def user_report():
    # 22-3-24
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
            break  # Exit the loop after handling the 'y' case
        elif write_to_file == 'n':
            menu()
            break  # Exit the loop after handling the 'n' case
        else:
            print("Please enter 'Y' for yes or 'N' for no.")
    

def write_user_report_to_file(users, user_stats):
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


from datetime import datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def mark_completed(task_number):
    # Used
    print(f"LINE 182 HERE task_number = {task_number}")
    # Step 1: Read existing tasks into a list of dictionaries
    task_list = []
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

    # Step 2: Modify the specified task's completion status
    task_index = task_number - 1  # Adjust for zero-based indexing
    if 0 <= task_index < len(task_list):
        task_list[task_index]['completed'] = True
        print(f"Task {task_number} marked completed.")
    else:
        print(f"Task {task_number} not found.")

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




# def mark_completed(task_number):
#     print(f"The task to be edited is {task_number}")
#     # completed_or_edit = input("Do you wish to mark Complete (C) or Edit (E) the task? Enter E or C  ")
#     # if completed_or_edit.lower() == "c":                
#     #     # print(f"task_list(index) = {task_list[int(task_number)-1]["completed"]}")
#     #     task_list[int(task_number)-1]["completed"] = True
#     #     # print(f"task_list(index) = {task_list[int(task_number)-1]["completed"]}")
#     with open("tasks.txt", "w") as task_file:
#         print(f"LINE 186 HERE task_file = {task_file}")
#         task_list_to_write = []
#         print(f"LINE 187 HERE len(task_file) = {len(task_file)} and task_number = {task_number}")        
#         for t in task_list:
#             print(f"LINE 188 HERE t = {t}")
#             str_attrs = [
#                 t['username'],
#                 t['title'],
#                 t['description'],
#                 t['due_date'].strftime(DATETIME_STRING_FORMAT),
#                 t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
#                 "Yes" if t['completed'] else "No"
#             ]
#             print(f"LINE 196 HERE str_attrs = {str_attrs}")
#             task_list_to_write.append(";".join(str_attrs))
#         task_file.write("\n".join(task_list_to_write))
#     print("Task {task_number} marked completed.")
    # elif completed_or_edit.lower() == "e":
    #     change_description(task_number)
    # else:
    #     mark_completed(task_number)   # task_number might not work here

def edit_task(task_number, task_list):
    index = 1
    # print(f"task list = {task_list}")
    for t in task_list:
        # print(f"t is {t}")
        disp_str = f"Task number = {index}\n"
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        # print(f"t = {t}")
        index += 1
        # print(disp_str)

    task_number = input("Edit or mark complete which task?\nPlease input the task number  ")
    if task_number.isdigit() and int(task_number) <= index:
        mark_complete = input("Do you wish to mark this task completed?  (Y/N): ")
        if mark_complete.lower() == "y" or mark_complete.lower() == "n":
            if mark_complete.lower() == "n":
                change_description(task_number)
            else:
                print("LINE 274 HERE Task marked completed.")
                mark_completed(int(task_number))
            # print(f"Line 72 - task_list is {task_list}")
        else:

            edit_task()
    else:
        edit_task()

def change_description(task_number):
    # Used
    print(f"LINE 288 HERE task_number = {task_number}")
    print(f"LINE 289 HERE type(task_number) = {type(task_number)}")
    task_number = int(task_number)
    # Step 1: Read existing tasks into a list of dictionaries
    task_list = []
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

    # Step 2: Modify the specified task's completion status
    task_index = task_number - 1  # Adjust for zero-based indexing
    if 0 <= task_index < len(task_list):
        confirm = input(f"LINE 307 HERE The description to be changed is {task_list[task_index]["description"]}, Y/N?  ")
        if confirm.lower() != "y" and confirm.lower() != "n":
            view_mine()
        else:
            new_description = input("Please input the new task description  \n")
            print(f"The new description is {new_description}")
            task_list[task_index]["description"] = new_description
        # task_list[task_index]['completed'] = True
        print(f"Task description changed.")
    else:
        print(f"Task {task_number} not found.")

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
    
    
    
    
    # print(f"LINE 97 {task_list[int(task_number)]["description"]}")
    # print(f"The description you are going to change is: {task_list[int(task_number)]["description"]}")
    # description = input("Please input the new description \n")
    # print(f"The new description is {description}")
    # correct = input("is this correct, Y or N?  ")
    # if correct.lower() != "y" and correct.lower() != "n":
    #     print("You must enter Y or N")
    #     change_description(task_number)
    # elif correct.lower() == "n":
    #     pass
    # elif correct.lower() == "y":
    #     # print(f"LINE 107 task -list is {task_list}")
    #     index_to_change = 0  # Index of the list entry to change
    #     new_entry = "New Entry"  # Replace this with your new entry

    #     if index_to_change < len(task_list):
    #         task_list[index_to_change]['title'] = new_entry

    #     print("Updated data:")
    #     for item in task_list:
    #         entry_str = ';'.join([f"{key}:{value}" for key, value in item.items()])
    #         print(entry_str)


def reg_user():
    # Request input of a new username
    new_username = input("New Username: ")

    with open("user.txt", "r") as out_file:
        users = []  # Initialize an empty list to store usernames
        for line in out_file:
            username, _ = line.strip().split(";")  # Split each line by semicolon and extract the username
            print(f"LINE 209 username = {username}")
            users.append(username)  # Append the username to the list
    print(f"LINE 213  users = {users}")

    if new_username in users:
        print(f"{new_username} is already registered")
        print("Please choose a new username")
        reg_user()
                
    else:
        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
                        
            with open("user.txt", "w") as out_file:
                print(f"LINE 232 user_data = {user_data}")
                print(f"LINE 233 user_data = {user_data}")
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
             
        # - Otherwise you present a relevant message.
        else:
            print("""Passwords do no match
            Please try again
                """)
            reg_user()

# Comment
def add_task(menu):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
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

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
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
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        # print(f"Line 189 task_file is {task_file}")
        return

def view_all():
             
            '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
            ''' 
            for t in task_list:
                # print(f"LINE 259 task_list = {task_list}")
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
        

def view_mine():
    # Used
    """Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
    """
    print(f"LINE 431 HERE task_list = {task_list}")  # task_list is a list of dictionaries
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
            disp_str += f"Task Description: \n {t['description']}\n"
            index += 1
    print(f"LINE 388 NHERE disp_str = {disp_str}")
    
    view_specific_task = input("View specific task? Y/N or -1 for main menu: ")
    if view_specific_task.lower() != "y" and view_specific_task.lower() != "n" and view_specific_task.lower() != "-1":
        print("Please input Y or N")
        view_mine()
    elif view_specific_task.lower() == "n" and view_specific_task.lower() == "-1":
        pass
    elif view_specific_task.lower() == "y":
        task_to_change = input("Which number task would you like to change?  ")
        print(f"LINE 400 HERE int(task_to_change) = {int(task_to_change)}")
        if task_to_change.isdigit() and int(task_to_change) > 0 and int(task_to_change) <= index:
            print(f"You would like to edit, mark complete or change task description {task_to_change}?")
            edit_complete = input("Would you like to edit (E) or mark this task as completed (C)? E/C  " )
            if edit_complete.lower() != "c" and edit_complete.lower() != "e":
                print("Please input E or C")
                view_mine()
            elif edit_complete.lower() == "c":
                mark_completed(int(task_to_change))
            elif edit_complete.lower() == "e":
                # Has task been completed?
                print("You can only make these changes if task not yet completed")
                is_task_complete(int(task_to_change))

                while True:
                    edit_chosen = input("""Please select your choice below
                    1 - Change Username
                    2 - Change Description
                    3 - Change Due Date\n""")
                    
                    if edit_chosen == "2":
                        change_description(task_to_change)
                    elif edit_chosen == "1":
                            change_username(task_to_change)
                    elif edit_chosen == "3":
                        pass
                    else:
                        print("Please make a valid input, D or U")
             
        else:
            view_mine()


def is_task_complete(task_number):
    # Used
    # user_task_list = {}
    # for task in task_list:
    #     if task["username"] == curr_user:
    #         user_task_list.append(task)
    # print(f"LINE 545 HERE user_task_list = {user_task_list}")
    user_task_list = []

    # Filter tasks for the current user
    for task in task_list:
        if task["username"] == curr_user:
            user_task_list.append(task)

    # Now `user_task_list` contains dictionaries associated with the current user
    print(user_task_list)
"""
        task_list = []
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
"""
    
def change_username(task_number):
    # Used
    print(f"LINE 533 HERE task_number = {task_number}")
    print(f"LINE 534 HERE type(task_number) = {type(task_number)}")
    task_number = int(task_number)
    # Step 1: Read existing tasks into a list of dictionaries
    task_list = []
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

    # Step 2: Modify the specified user name
    task_index = task_number - 1  # Adjust for zero-based indexing
    if 0 <= task_index < len(task_list):
        confirm = input(f"LINE 554 HERE The username to be changed is {task_list[task_index]["username"]}, Y/N?  ")
        if confirm.lower() != "y" and confirm.lower() != "n":
            view_mine()
        else:
            new_user_name = input("Please input the new user name  \n")
            print(f"The new user name is {new_user_name}")
            task_list[task_index]["username"] = new_user_name
        # task_list[task_index]['completed'] = True
        print("User name changed.")
    else:
        print(f"Task {task_number} not found.")

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





def calculate_task_statistics():
    # 22-3-24
    tasks = []
    with open('tasks.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(';')
            tasks.append(parts)

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task[4] == 'Yes')
    incomplete_tasks = total_tasks - completed_tasks

    # Using today's date for comparison
    today_date = date.today()
    overdue_tasks = sum(1 for task in tasks if datetime.strptime(task[3], "%Y-%m-%d").date() < today_date and task[4] == 'No')

    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Outputting the statistics
    print(f"Total number of tasks: {total_tasks}")
    print(f"Total number of completed tasks: {completed_tasks}")
    print(f"Total number of tasks yet to be completed: {incomplete_tasks}")
    print(f"Total number of incomplete tasks that are overdue: {overdue_tasks}")
    print(f"Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%")
    print(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%")

    # Asking the user if they want to write these results to a file
    write_to_file = input("Do you want to write these results to 'task_overview.txt'? (Yes/No) ").strip().lower()
    if write_to_file == 'yes':
        write_statistics_to_file(total_tasks, completed_tasks, incomplete_tasks, overdue_tasks, incomplete_percentage, overdue_percentage)

def write_statistics_to_file(total_tasks, completed_tasks, incomplete_tasks, overdue_tasks, incomplete_percentage, overdue_percentage):
    with open('task_overview.txt', 'w') as file:
        file.write(f"Total number of tasks: {total_tasks}\n")
        file.write(f"Total number of completed tasks: {completed_tasks}\n")
        file.write(f"Total number of tasks yet to be completed: {incomplete_tasks}\n")
        file.write(f"Total number of incomplete tasks that are overdue: {overdue_tasks}\n")
        file.write(f"Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%\n")
        file.write(f"Percentage of tasks that are overdue: {overdue_percentage:.2f}%\n")


        



# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

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


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")
    print(f"LINE 342 user_data = {user_data}")
    print(f"LINE 343 user_data[0] = {user_data[0]}")
    print(f"LINE 343 user_data[1] = {user_data[0].split(";")}")

username_password = {}
for user in user_data:
    username, password = user_data[0].split(";")
    username_password[username] = password



logged_in = False

while not logged_in:
    try:
        with open("user.txt", "r") as out_file:
            user_data = []  # Initialize an empty list for user data
            username_password = {}  # Initialize an empty dictionary for username-password pairs

            # Read existing user data from the file
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

menu()
