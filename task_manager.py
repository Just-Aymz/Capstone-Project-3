# -------------------------------- Imports -------------------------------- #
import os
from datetime import datetime as dt

# ----------------------------- User-Functions ---------------------------- #


def menu():
    """
    A function that returns the menu options when the username is not
    admin.
    """
    print('\nPlease select from the following options:')
    print('r - register user')
    print('a - add task')
    print('va - view all tasks')
    print('vm - view my tasks')
    print('e - exit')


def admin_menu():
    """
    A function that returns the menu options when the username is
    admin.
    """
    print('\nPlease select from the following options:')
    print('r - register user')
    print('a - add task')
    print('va - view all tasks')
    print('vm - view my tasks')
    print('ds - display statistics')
    print('gr - generate reports')
    print('vr - view reports')
    print('e - exit')


def edit_menu():
    """
    A function that returns this menu options when the user chooses
    to edit a task.

    returns:
        edit(str): Returns the input from the user as a variable
    """
    print("e - To mark the task as complete")
    print("a - To change who the task is assigned to")
    edit = input("d - To edit the due date of the task: ")

    return edit


def path_directory(filename: str):
    """
    A function that finds the filepath on a system depending on where
    this file is on the system, and takes in the filename as an input,
    to create the filepath to the file.

    Args:
        filename(str): The name of the desired .txt file as a string

    Returns:
        filepath(str): The filepath to the program and file
    """
    dirname = os.path.dirname((__file__))
    file_path = os.path.join(dirname, filename)

    return file_path


def read_file(filename: str, mode: str):
    """
    A function that takes in a .txt file and reads and returns its
    contents, using the read method or the read and write method,
    depending on the mode input.

    Args:
        filename(str): The name of the desired .txt file as a string
        mode(str): The mode which the file is read

    Returns:
        content(list): Returns the contents of a file as a nested list
        with each new line being represented as a seperated list
        element when "r+" mode is selected, or returns the file as
        single string if "r" mode is selected. Error message is
        returned if mode selected is neither "r" or "r+"
    """
    file_path = path_directory(filename)
    with open(file=file_path, mode=mode, encoding="utf-8") as file:
        if mode == "r+":
            content = file.readlines()
        elif mode == "r":
            content = file.read()
        else:
            raise ValueError("mode needs to be 'r' or 'r+'")

    return content


def user_authentication(filename: str):
    """
    A function that creates a dictionary of the users and their
    passwords from a .txt file containing the users and their passwords
    on each line

    Args:
        filename(str): a .txt file as a string

    Returns:
        user_password_dict(dict): a dict with the key value
        representing the user and the value representing the
        password of that user
    """
    file_content = read_file(filename, "r+")
    user_password_dict = {}
    for element in file_content:
        # Remove any whitespace and unpack values from file line
        username, password = element.strip().split(", ")
        # Append to dictionary
        user_password_dict.update({username: password})

    return user_password_dict


def write_file(filename: str, mode: str, content: str):
    """
    A function that opens a filename an adds specified content onto
    what is already on the .txt, or creates a new .txt file if it does
    not exist.

    Args:
        filename(str): a .txt file of to write to
        mode(str): the method with which the file will be written in
        content(str): the content to write to the file.
    """
    file_path = path_directory(filename)
    with open(file=file_path, mode=mode, encoding="utf-8") as file:
        file.write(content)


def new_user(filename: str):
    """
    A function that allows for the admin to register a new user, if the
    user is not on the database already.

    Args:
        filename(str): a .txt file which new user will be written into
    """
    while True:
        print("\nPlease provide the new username to", end=" ")
        new_username = input("be registered: ").lower()
        if new_username in users.keys():
            print("User is already registered.")
            break
        else:
            while True:
                print("Please provide password for,", end=" ")
                new_password = input(f'{new_username.title()}: ')
                password_confirmation = input("Please confirm password: ")
                if new_password == password_confirmation:
                    write_file(filename, "a+",
                               f"\n{new_username}, {new_password}")
                    print(f"\n{new_username.title()} has been ", end=" ")
                    print("successfully added to database.\n")
                    break
                else:
                    print("\nPassword and confirmation", end=" ")
                    print("password do not match.")
            break


def add_task():
    """
    A  function that stores the inputs of a user about the tasks
    assigned to another authorised user, and returns the input
    information in a readable string format.

    Returns:
        content(str): Returns formatted string
    """
    while True:
        taskee = input("\nUsername to assign task to: ")
        # checks using membership operator whether the taskee is in the
        # users list of keys
        if taskee in users.keys():
            break
        else:
            print("User has not been register.", end=" ")
            print("Please assign tasks to registered users only.\n")

    while True:
        print("Provide short description of task", end=" ")
        task_description = input('(<255 characters): ')
        if len(task_description) < 255:
            break
        else:
            print("You have exceeded the limit,", end=" ")
            print("please provide a shorter description", end=" ")
            print("of less than 255 characters\n")

    while True:
        print("Due date of the task in {dd mon yyyy} format", end=" ")
        due_date = input("(mon is months abbreviated name): ").strip().title()
        try:
            # strptime() method of datetime module to ensure correct
            # format provided. Returns value error if wrong format
            # provided
            due_date_check = dt.strptime(due_date, '%d %b %Y').date()
            break
        except ValueError:
            print("You did not provide the correct format.\n")

    # # Use the date portion of the datetime object
    assignment_date = dt.today().date()
    assignment_date = dt.strftime(assignment_date, '%d %b %Y')
    task_completion = "No"
    task_title = input("Provide the title of the task: ")
    content = (f"\n{taskee}, {task_title}, {task_description}, "
               f"{assignment_date}, {due_date}, {task_completion}")
    print(f"\nTask successfully assigned to {taskee.title()}")
    return content


def view_all(filename: str):
    """
    A function that splits each line in filename by the comma and
    stores each split into its own variable and stores those variables
    into a readable format, which is returned when the function is
    called

    Args:
        filename(str): a .txt file where data will be read into from

    Returns:
        view_all_tasks(str): Formatted string of all the tasks assigned
        on the database
    """
    view_all_tasks = ""
    file_content = read_file(filename, "r+")
    for line in file_content:
        # Split each line from the file_contents at the comma
        line_content = line.split(',')
        # Use splat operator to pass list elements to each argument
        view = f"{'-'*165}{view_format(*line_content)}\n{'-'*165}\n"
        view_all_tasks = view_all_tasks + view

    return view_all_tasks


def view_my(filename: str):
    """
    A function that splits each line in filename by the comma and
    stores each split into its own variable and stores those variables
    into a readable format. If the 'user' variable is the same as the
    username, the other variables related to that 'user' will then be
    stored as a variable which is returned when the function is
    called

    Args:
        filename(str): a .txt file where data will be read from

    Returns:
        view_my_tasks(str): A formatted string of all the tasks of the
        user that is logged in.
    """
    view_my_tasks = ""
    file_contents = read_file(filename, "r+")
    counter = 1
    for line in file_contents:
        # Split each line from the file_contents at the comma
        data = line.split(',')
        # Remove any whitespace
        if data[0].strip() == username:
            # Use splat operator to pass list elements to each argument
            view = f"{'-'*165}\n{counter}.{view_format(*data)}\n{'-'*165}\n"
            view_my_tasks = view_my_tasks + view
            counter += 1

        else:
            pass

    return view_my_tasks


def user_tasks(filename: str):
    """
    A function that is responsible for reading in a file and retrieving
    all the tasks assigned to the user currently logged onto the system
    , and storing the task information as a dictionary. Each task dict
    is then stored in a list.

    Args:
        filename(str): the filename that is to be read.

    Return:
        user_tasks_list(list): A list of dictionaries, each
        representing a task assigned to the user logged into the system
    """
    file_contents = read_file(filename, "r+")
    user_tasks_list = []
    for line in file_contents:
        # Split each line from the file_contents at the comma
        data = line.split(', ')
        # Remove any whitespace
        if data[0].strip() == username:
            user_task = task_dct(*data)
            user_tasks_list.append(user_task)
        else:
            pass

    return user_tasks_list


def view_format(user: str, task: str, task_description: str,
                date_assign: str, due_date: str, task_comp: str):
    """
    A function that is responsible for returning the desired formatting
    of the provided arguments

    Args:
        user(str): User that the task is assigned to
        task(str): Task that is assigned to the user
        task_description(str): Description of the task that is assigned
        date_assign(str): Date the task is assigned on
        due_date(str): Date the task is due on
        task_comp(str): Whether the task is complete or not

    Returns:
        view(str): Formatted string of all the provided arguments
    """
    view = (
        f"\nAssigned to:\t\t {user}"
        f"\nTask:\t\t\t{task}"
        f"\nTask description:\t{task_description}"
        f"\nDate assigned:\t\t{date_assign}"
        f"\nDue date:\t\t{due_date}"
        f"\nTask Completed?\t\t{task_comp}"
    )

    return view


def task_dct(user: str, task: str, task_description: str,
             date_assign: str, due_date: str, task_comp: str):
    """
    A function that is responsible for returning a dictionary from the
    provided arguments.

    Args:
        user(str): User that the task is assigned to
        task(str): Task that is assigned to the user
        task_description(str): Description of the task that is assigned
        date_assign(str): Date the task is assigned on
        due_date(str): Date the task is due on
        task_comp(str): Whether the task is complete or not

    Returns:
        task(dict): a key:value dictionary of all the information of a
        task
    """
    task = {
        "user": user,
        "task": task,
        "task_description": task_description,
        "date_assign": date_assign,
        "due_date": due_date,
        "task_comp": task_comp
    }

    return task


def file_overwrite(filename: str, list_of_dct: list):
    """
    A function that is responsible for overwriting an existing filename

    Args:
        filename(str): A .txt file that will be overwritten
        list_of_dct(str): A list of dictionaries that represent each
        task in the filename with the changed values.
    """
    # Use the first dictionary in list_dct to overwrite
    # current tasks.txt file
    new_line = ", ".join(list_of_dct[0].values())
    write_file(filename, "w+", f"{new_line}\n")
    # Append the rest of the list_dct elements into the
    # tasks.txt file
    for dct in list_of_dct[1:]:
        new_line = ", ".join(list(dct.values()))
        write_file(filename, "a+", f"{new_line}\n")


def edit_overwrite(edit: dict):
    """
    A function that is responsible for overwriting a task dictionary,
    if the tasks description and the edited tasks description are the
    same, that task dictionary's values are then replaced according to
    the keyword arguments

    Args:
        edit(dict): a dict representing a task that has been edited
    """
    all_tasks_override = task_list_dct("tasks.txt")
    # Loop through each dict in the list
    for dct in all_tasks_override:
        # if the "task_description" for the dictionary instance in the
        # loop, and that of the edit passed to the function are the
        # same, update the loop instance with the edit dictionary
        if dct["task_description"] == edit["task_description"]:
            dct.update(edit)
    file_overwrite('tasks.txt', all_tasks_override)


def statistics(user_filename: str, tasks_filename: str):
    """
    A function that summerises the total number of users and the total
    number of tasks in the user_filename and tasks_filename, and prints
    the information in a summerised format
    """
    users = user_authentication(user_filename)
    # Counts the current total number of users in the user_filename
    total_users = len(users.keys())
    total_tasks = 0
    file = read_file(tasks_filename, "r+")
    # Use placeholder to iterate file
    for _ in file:
        total_tasks += 1

    print("STATISTICS\n")
    print(f"Total number of registered users:\t\t {total_users}")
    print(f"Total number of tasks for all users:\t\t {total_tasks}\n")


def task_list_dct(filename: str):
    """
    A function that is responsible for reading a file and storing each
    line of its contents about a task as a dictionary that is then
    appended to a list that represents the entire content of the read
    file

    Args:
        filename(str): A .txt file that contains information about tasks
        that will be read in

    Returns:
        list_dct(dict): A list containing dictionary elements which
        represent a task.
    """
    # Stores each task as a dct in a list
    list_dct = []
    file_contents = read_file(filename, "r+")
    for line in file_contents:
        line_content = line.strip().split(', ')
        # unpack the line_content into the args of the task_dct
        # function
        task = task_dct(*line_content)
        list_dct.append(task)

    return list_dct


def task_overview(list_of_dct: list):
    """
    A function that is responsible for generating the task overview
    details in a .txt file

    Args:
        list_of_dct(dict): A list of dictionaries containing
        information about a task

    Returns:
        view(str): Returns the task overview information in a desired
        format
    """
    total_num_tasks = len(list_of_dct)
    # Use incremental operator to return total completed tasks
    completed_tasks = 0
    for dct in list_of_dct:
        if dct["task_comp"] == "Yes":
            completed_tasks += 1

    # Use incremental operator to return total incomplete tasks
    incompleted_tasks = 0
    for dct in list_of_dct:
        if dct["task_comp"] == "No":
            incompleted_tasks += 1

    # Use incremental operator to return total overdue tasks
    overdue_tasks = 0
    for dct in list_of_dct:
        # Convert due_date to a datetime object
        dct["due_date"] = dt.strptime(dct["due_date"], '%d %b %Y').date()
        today = dt.today().date()

        if (dct["task_comp"] == "No") & (dct["due_date"] < today):
            overdue_tasks += 1

    incomplete_pct = round((incompleted_tasks / total_num_tasks) * 100, 2)
    overdue_pct = round((overdue_tasks / total_num_tasks) * 100, 2)

    view = (
        f"TASKS REPORT"
        f"\n\nTotal tasks:                   {total_num_tasks}"
        f"\nTotal Completed tasks:         {completed_tasks}"
        f"\nTotal Incompleted tasks:       {incompleted_tasks}"
        f"\nTotal Overdue tasks:           {overdue_tasks}"
        f"\nIncomplete tasks percent(%):   {incomplete_pct}%"
        f"\nOverdue tasks percent(%):      {overdue_pct}%\n"
    )

    write_file('task_overview.txt', 'w+', view.strip())


def user_overview(user_dct: dict, list_of_dct: dict):
    """
    A function that is responsible for generating the user overview
    details in a .txt file

    Args:
        list_of_dct(dict): A list of dictionaries containing
        information about a task

    Returns:
        view(str): Returns the user overview information in a desired
        format
    """
    total_num_tasks = len(list_of_dct)
    user_tasks_total = []
    # For each user in the database, do the following:
    for user in user_dct.keys():
        today = dt.today().date()
        user_tasks_count = 0
        overdue_tasks = float(0)
        user_task_comp = float(0)
        # Iterate through list_of_dct, which represents each task as a
        # dictionary
        for dct in list_of_dct:
            overdue_mask = ((dct.get("user") == user)
                            & (dct["task_comp"] == "No")
                            & (dct["due_date"] < today))
            completion_mask = ((dct.get("task_comp") == "Yes")
                               & (dct.get("user") == user))
            # When dct value is the same as user from user.keys() for
            # that instance of the iteration
            if dct.get("user") == user:
                # Add one to the user_tasks_count for user
                user_tasks_count += 1
            # If overdue_mask conditions are met
            if overdue_mask:
                # Add one to the overdue_tasks for user
                overdue_tasks += 1
            # If completion_mask conditions are met
            if completion_mask:
                # Add one to the user_task_comp for user
                user_task_comp += 1

        try:
            task_overdue_pct = round((overdue_tasks / user_tasks_count)
                                     * 100, 2)
        except ZeroDivisionError:
            task_overdue_pct = round(0, 2)
        try:
            task_comp_pct = round((user_task_comp / user_tasks_count)
                                  * 100, 2)
        except ZeroDivisionError:
            task_comp_pct = round(0, 2)
        # Store the information as a dictionary and append to
        # user_tasks_total
        summary_dct = {
            "user": user,
            "total_tasks": user_tasks_count,
            "overdue_pct": task_overdue_pct,
            "complete_tasks": user_task_comp,
            "tasks_comp_pct": task_comp_pct
        }
        user_tasks_total.append(summary_dct)
    # For each users summary,
    for user_summary in user_tasks_total:
        pct_of_all_tasks = round((user_summary.get("total_tasks")
                                 / total_num_tasks) * 100, 2)
        # Store as key:value in user_summary dictionary
        user_summary.update({"pct_of_tasks": round(pct_of_all_tasks, 2)})

    for user_summary in user_tasks_total:
        incomp_with_task = ((user_summary.get("tasks_comp_pct") == float(0))
                            & (user_summary.get("total_tasks") > 0))
        incomp_no_task = ((user_summary.get("tasks_comp_pct") == float(0))
                          & (user_summary.get("total_tasks") == 0))
        if incomp_with_task:
            incom_pct = float(100)
        elif incomp_no_task:
            incom_pct = float(0)
        else:
            # If user_task_comp is not zero, execute this block of code
            incom_pct = round(100 - user_summary.get("tasks_comp_pct"), 2)
        # Store as key:value in user_summary dictionary
        user_summary.update({"tasks_incom_pct": incom_pct})

    all_views = []
    for user_summary in user_tasks_total:
        view = (
            f"USER TASKS REPORT"
            f"\n\nUser:                   {user_summary.get('user')}"
            f"\nTotal tasks:            {user_summary.get('total_tasks')}"
            f"\n% of all tasks:         {user_summary.get('pct_of_tasks')}%"
            f"\n% of tasks completed:   {user_summary.get('tasks_comp_pct')}%"
            f"\n% of tasks incomplete:  {user_summary.get('tasks_incom_pct')}%"
            f"\n% of tasks overdue:     {user_summary.get('overdue_pct')}%"
        )
        all_views.append(view)

    # Write over the existing file
    write_file('user_overview.txt', 'w+', all_views[0].strip())
    # Use for loop to append to the file
    for view in all_views[1:]:
        write_file('user_overview.txt', 'a+', f"\n\n{view.strip()}")


def generate_report(filename: str):
    """
    A function that is responsible for producing the task over view
    report and the user over view reports.
    """
    list_dct = task_list_dct(filename)
    task_overview(list_dct)
    user_overview(users, list_dct)

# ---------------------------------- Login -------------------------------- #

# store the user/password dictionary as users to be able to access the
# users using the .keys() function, as well as the users passwords,
# using the .values() function


users = user_authentication("user.txt")
while True:
    # Use defensive means to ensure username is stored in lowercaps
    username = input('Please provide username to login: ').lower()
    # Check whether user input, "username" is in our users list
    if username in users.keys():
        print(f"Hello {username.title()}, please provide your", end=" ")
        password_request = input("password: ")
        # Use .get() function to access the values of the dictionary using
        # key
        if password_request == users.get(username):
            print("Password correct!", end=" ")
            print(f"Welcome back, {username.title()}!\n")
            break
        else:
            print('\nOops, that doesnt seem right,', end=' ')
            print("Let's try that again.")
    else:
        print('Username name on database. Please ensure', end=' ')
        print('you are providing the correct login details\n')

# ---------------------------------- Menu -------------------------------- #
choice = 'x'
while choice != 'e':
    if username == 'admin':
        admin_menu()
    else:
        menu()
    choice = input('Selection: ')
    if choice == 'r':
        if username == 'admin':
            new_user('user.txt')
            users = user_authentication('user.txt')
        else:
            print('Only admin has the rights to register new users')
    elif choice == 'a':
        new_task = add_task()
        write_file('tasks.txt', "a+", new_task)
    elif choice == 'va':
        all_tasks = view_all('tasks.txt')
        print("\nTasks for all users:")
        print(all_tasks)
    elif choice == 'vm':
        print(f"\nTasks for {username.title()}:\n")
        my_tasks = view_my('tasks.txt')
        print(my_tasks)

        list_dct = user_tasks('tasks.txt')

        while True:
            try:
                print("\nPlease provide the index of the task you'd", end=" ")
                print("like to edit, or return", end=" ")
                edit = int(input("-1 to go back to the previous menu: "))
                if edit == -1:
                    break
                elif edit <= len(list_dct):
                    # Subtract -1 from 'edit' to ignore zero-indexing
                    _task = list_dct[edit - 1]
                    # Remove blank spaces from values using dict
                    # comprehension
                    _task = {idx: value.strip()
                             for idx, value in _task.items()}
                    print("\nTASK SELECTED:")
                    print(f"{view_format(**_task)}\n")
                    # Strips any blank space from the input value
                    selection = edit_menu().strip()
                    if ((selection == "e")
                            & (_task["task_comp"].strip() == "No")):
                        _task["task_comp"] = "Yes"
                        # Overwrite the changes
                        edit_overwrite(_task)
                        # Confirmation message to user
                        print(f"\nTask: {_task['task']}", end=" ")
                        print("has been successfully marked as", end=" ")
                        print(f"complete for {_task['user'].title()}")
                    elif ((selection == "a")
                          & (_task["task_comp"].strip() == "No")):
                        reassign = input("\nUser to reassign task to: ")
                        if reassign not in users.keys():
                            print("Please ensure that user you are", end=" ")
                            print("reassigning task to, is a", end=" ")
                            print("validated user on the database\n")
                        else:
                            _task["user"] = reassign
                            # Overwrite the changes
                            edit_overwrite(_task)
                            print("Task successfully", end=" ")
                            print(f"reassigned to {reassign.title()}")
                    elif ((selection == "d")
                          & (_task["task_comp"].strip() == "No")):
                        while True:
                            print("Provide the new due date for the", end=" ")
                            # Store the first letter of the month as a capital
                            reassign_date = input(
                                "task (dd mon yyyy): ").title()
                            try:
                                # strptime() method of datetime module to
                                # ensure correct format provided. Returns
                                # value error if wrong format provided
                                due_date_check = (
                                    dt.strptime(reassign_date, '%d %b %Y')
                                    .date())
                                break
                            except ValueError:
                                print("Please provide the correct format.\n")
                        _task["due_date"] = reassign_date
                        # Overwrite the changes
                        edit_overwrite(_task)
                        # Confirmation message to user
                        print(f"\nTask: {_task['task']} date", end=" ")
                        print("has been successfully changed to", end=" ")
                        print(f"{reassign_date} for {_task['user'].title()}")
                    elif ((selection == "a")
                          & (_task["task_comp"].strip() == "Yes")):
                        print("\nOops! You cannot reassign a completed task!")
                    else:
                        print("\nInvalid Selection")
                        print(my_tasks)
                elif edit > len(list_dct):
                    print("\nInput provided is invalid. Please ", end=" ")
                    print("select a valid task number")
                    print(my_tasks)
            except ValueError:
                print("Please ensure you have provided valid option\n")
                print(my_tasks)
    elif choice == 'ds':
        print("\nSystem summative statistics:")
        print('*'*165)
        statistics('user.txt', 'tasks.txt')
        print(f"{'*'*165}\n")
    elif choice == 'gr':
        generate_report("tasks.txt")
        print("\nReport successfully generated!")
    elif choice == 'vr':
        print("\nTo view a report, please generate a report first.")
        print("1 - To generate a report")
        print("0 - To go back to the previous menu")
        answer = input("Submission: ")
        if answer == "1":
            generate_report("tasks.txt")
            t_overview = read_file("task_overview.txt", "r")
            u_overview = read_file("user_overview.txt", "r")
            print(f"\n{'*'*165}")
            print(f"\n{t_overview}\n{'*'*165}\n{u_overview}")
            print(f"\n{'*'*165}")
        elif answer == "0":
            break
        else:
            print("Please ensure valid option has been selected.")
    elif choice == 'e':
        print("\nGoodbye!")
    else:
        print("Please ensure to have made the correct input.")
