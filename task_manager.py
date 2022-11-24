#Task Manager by Kyle Jacobs
# Best width 80chars 
# Please note that where the return startement is used without a value then the value of none is returned to the function 
# caller and is used where the user would like to escape out of the current menu and return to previous menu without a value.
## Fixed the date type error with the date util parser module
# =====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import date, datetime
from dateutil.parser import parse


#====Functions====#
def reg_user():
    '''Function that reads in user data from an input file. User to then input new users credentials. Function prevents registering duplicate credentials, does password confirmation checks and writes data to output file used to store user data.'''
    with open('user.txt', 'r+') as f:
        user_list = [(item.strip()).split(',')[0]for item in f.readlines() if item[0][0]]
    
    # Declare 'lines' string variable
    lines = ''

    # User to input new username and store as variable 'newUser'
    while True:
        newUser = input("\nPlease input new username: ")
        if newUser not in user_list:
            break
        else:
            print('\nInput Error | Please check and try again!\n')
    
    #User to input new password and store as variable 'newPassword'
    newPassword = input(f"\nPlease input a password for {newUser}: ")
    #User to confirm password input
    passconfirm = input(f"\nPlease confirm password for {newUser}: ")
    if newPassword == passconfirm:
        #If passwords match add inputs to list variable
        credentials = [f'{lines}\n' + f'{newUser}, {newPassword}']
        with open('user.txt', 'r+') as f:
            for line in f:
                lines += line
            #Iterate over list variable and write output to file
            for creds in credentials:
                f.write(creds)

    else:
            #If passwords do not match print error message
            print("\nPasswords do not match, Please Try again!!")

def add_task():
    '''Funtion that reads in user and task data from two input files. User can add a new task by inputting required fields. Function checks if user to which task will be assigned exists, password confirmation, and a future feature will ensure that input due dates is only subnitted in the required format. Data is then written to output file used to store task data.'''
    # Header
    print(f'''{'*' * 80}
            \n{' ' * 28}Task Manager | Add Task
            \n{'*' * 80}''')

    # Declare boolean variable 'taskComplete' as No
    # Declare empty string variable 'lines'
    taskComplete = 'No'

    # Request user to input username to assign to task and store as variable
    user_list = open('user.txt', 'r')
    user_list = [(item.strip()).split(', ')[0] for item in user_list.readlines()]

    while True:
    
        taskUser = input('''\nPlease input username to assign to task!!
        \nUsername: ''')
        if taskUser not in user_list:
            print('\nInput Error | Please check and try again!')
        else:
            break
        
    # Request User to input task title ad store as variable
    print("\nPlease input the title of the task!!\n")
    taskTitle = input("Title: ")

    # Request User to input task description and store as variable
    print("\nPlease input a brief description of the task!!\n")
    TaskDescription = input("Description: ")

    # Request user to input task due date and store as variable
    print("\nPlease Assign a due date to the task!!\n")
    taskDD = input("Due date (yyyy-mm-dd): ")

    # Get todays date and store as variable 'today'
    today = date.today()

    # Read in task data to grab task count
    task_data = open('tasks.txt', 'r')
    task_data = [item.strip().split(', ') for item in task_data.readlines()]

    # Inittialize 'taskList' list variable
    # Assign task varibles as list values
    taskList = f"\n{len(task_data)+1}, {taskUser}, {taskTitle}, {TaskDescription}, {taskDD}, {today}, {taskComplete}"

    writable_file = open('tasks.txt', 'a')
    writable_file.write(taskList)
    writable_file.close()

def view_all():
    '''Function that reads in task data from an input file. Displays all tasks in order.'''
    # Header
    print(f'''{'*' * 80}
            \n{' ' * 26}Task Manager | View All Tasks
            \n{'*' * 80}''')
    
    # Read task data from file and store in list variable 'task_list'. 
    # Initialize counter and store in int variable 'num'.
    task_list = [item.strip().split(', ') for item in open('tasks.txt', 'r').readlines()]
    num = 0

    # Display task data
    print('_' * 80)
    while num < (len(task_list)):
        print('\nTask:', num + 1, '\n')

        print(f'''Title:\t\t {'.' * 20} {task_list[num][2]}
        \nAssigned To:\t {'.' * 20} {task_list[num][1]}
        \nDate Assigned:\t {'.' * 20} {task_list[num][5]}
        \nDue Date:\t {'.' * 20} {task_list[num][4]}
        \nTask Complete:\t {'.' * 20} {task_list[num][6]}
        \nTask Description:{'.' * 58}\n''')
        print(task_list[num][3])

        num += 1

        if num < len(task_list):
            input(f'\nTask: {num + 1} (Press Enter!)')
        else:
            input(f'\nEOF (Press Enter to return!)')

        print('_' * 80)
    
def view_mine(currentUser):
    '''Function that reads in data from two input files used to store user credentials and task data. Displays all tasks assigned to the current signed in user, first in a summary format from which the user can select to view expanded task details by inputting the task number. User can then select to edit the task or mark it complete if not already marked done. Editing task details allows user to change the assigned user and due date.'''
    
    # Initialize string and counter variables
    error_str =  '\nInput Error | Please check and try again!!\n'
    writable_task_str = ''
    str_store = ''
    count = 0
    task_options = ['x','e','-1'] 

    # Iterate over user and task files to store data in list variables. 
    user_list = [(item.strip()).split(',')[0]for item in open('user.txt', 'r+').readlines() if item[0][0]]
    task_list = [(item.strip()).split(', ') for item in open('tasks.txt', 'r+').readlines()]

    # Header
    print(f'''
    \n{'*' * 80}
    \n{' ' * 26}Task Manager | View My Tasks
    \n{'*' * 80}''')

    # Loop that handles all changes and displays of task data. Nesting 
    # ensures that data is diplayed and updated interactively as the 
    # progrum runs.
    selection_list = [item for item in task_list.copy() if currentUser in item]
    # Iterates over task_list data and stores non user tasks in a 
    # separate list variable 'non_selection_list'.
    non_selection_list = [item for item in task_list if currentUser not in item]

   # Loop that displays condensed task data and stores fata in string 
   # variable.
    while True:
        print(f'''
        \nTask Number:\t{'.' * 15} {count + 1} 
        \nTask: \t\t{'.' * 15} {selection_list[count][2]}
        \nAssigned To: \t{'.' * 15} {selection_list[count][1]}
        \nTask Complete? \t{'.' * 15} {selection_list[count][6]}''')
        print('_' * 80)
        
        str_store += f'''
        \nTask Number:\t{'.' * 15} {count + 1} 
        \nTask: \t\t{'.' * 15} {selection_list[count][2]}
        \nAssigned To: \t{'.' * 15} {selection_list[count][1]}
        \nTask Complete? \t{'.' * 15} {selection_list[count][6]}''' + '\n' + '_' * 80
       
        count += 1

        if count == len(selection_list):
            break
        else:
            continue
    
    # Loop that dusplays expanded task data based on user input selection
    # and handles any input errors.
    while True:
        try:

            count = int(input('''\nTo view task data, select task number or '-1' to return to main menu!
            \n: ''')) - 1

            if count == -2:
                return
        
            task_selection = selection_list.pop(count)
            
            if 'No' in task_selection:
                # Header
                print(f'''
                \n{'*' * 80}
                \n{' ' * 25}Task Manager | Task Selection
                \n{'*' * 80}''')

                # Body
                print(f'''
                \nTask Number:\t{'.' * 15} {count + 1} 
                \nTask: \t\t{'.' * 15} {task_selection[2]}
                \nAssigned To: \t{'.' * 15} {task_selection[1]}
                \nDate Assigned: \t{'.' * 15} {task_selection[5]}
                \nDue Date: \t{'.' * 15} {task_selection[4]}
                \nTask Complete? \t{'.' * 15} {task_selection[6]}
                \nTask Description: {'.' * 60}\n''')
                print(task_selection[3])
                print('_' * 80)
                break
            
            else:
                 # Header
                print(f'''
                \n{'*' * 80}
                \n{' ' * 25}Task Manager | Task Selection
                \n{'*' * 80}''')

                # Body
                print(f'''
                \nTask Number:\t{'.' * 15} {count} 
                \nTask: \t\t{'.' * 15} {task_selection[2]}
                \nAssigned To: \t{'.' * 15} {task_selection[1]}
                \nDate Assigned: \t{'.' * 15} {task_selection[5]}
                \nDue Date: \t{'.' * 15} {task_selection[4]}
                \nTask Complete? \t{'.' * 15} {task_selection[6]}
                \nTask Description: {'.' * 60}\n''')
                print(task_selection[3])
                print('_' * 80)
                input('\nNo Task options available | Task has already been completed!!\n\n-Press any key to return-\n')
                return
                
        except ValueError:
                print(error_str)
        except UnboundLocalError:
            print(error_str)
        except IndexError:
            print(error_str)

    # Initialise section booleans
    block_0 = False
    block_1 = False
    block_2 = False
    block_3 = False

    # Loop that handles the task option input. 
    while True:

        # Header
        task_option = input(f'''
        \n{'*' * 80}
        \n{' ' * 21}Mark Complete - 'x' | Edit Task - 'e'
        \n{'*' * 80}
        \n: ''')
        break
    
    # Conditions checks if input matches list and triggers boolean variables
    if task_option in task_options:
        if task_option == 'x':
            block_0 = True
        elif task_option == 'e':
            while True:    
                try:
                    edit_option = int(input(f'''\n-|Edit Task Options|-
                    \n0   -   edit User
                    \n1  -   edit due date
                    \n2  -   both
                    \n: '''))
                    
                    if edit_option == 0:
                        block_1 = True
                        break
                    elif edit_option == 1:
                        block_2 = True
                        break
                    elif edit_option == 2:
                        block_3 = True
                        break
                    else:
                        print(error_str)
                except ValueError:
                    print(error_str)
        else:
            print(error_str)
    else:
        print(error_str)

    # Secoond condition handles computations based on the booleans 
    # triggered in the first and adds a few fata checks.
    if block_0:
        task_selection[6] = 'Yes'
    elif block_1:
        task_user = task_selection[1] = input('New user: ')
        if task_user not in user_list:
            print(error_str)
            return
    elif block_2:
        new_dd = task_selection[4] = input('New due date: ') 
    elif block_3:
        task_user = task_selection[1] = input('\nnew user: ')
        if task_user not in user_list:
            print(error_str)
            
        else:
            new_dd = task_selection[4] = input('New due date: ')

     # Header
    print(f'''
    \n{'*' * 80}
    \n{' ' * 25}Task Manager | Task Selection
    \n{'*' * 80}''')

    # Display focussed task Data
    print(f'''
    \nTask Number:\t{'.' * 15} {task_selection[0]} 
    \nTask: \t\t{'.' * 15} {task_selection[2]}
    \nAssigned To: \t{'.' * 15} {task_selection[1]}
    \nDate Assigned: \t{'.' * 15} {task_selection[5]}
    \nDue Date: \t{'.' * 15} {task_selection[4]}
    \nTask Complete? \t{'.' * 15} {task_selection[6]}
    \nTask Description: {'.' * 60}\n''')
    print(task_selection[3])
    print('_' * 80)

    # Merges split data back with non selected data data.
    selection_list += [task_selection]
    
    # Reset counter
    count = 0

    # Join user and non user tasks into sorted task_list variable.
    task_list = sorted(non_selection_list + selection_list) 

    # Loop which writes list data to create writable string variable.
    for items in task_list:
        count += 1
        writable_task_str += f'{count}, {items[1]}, {items[2]}, {items[3]}, {items[4]}, {items[5]}, {items[6]}\n'
    
    # Write string data to file
    with open('tasks.txt', 'r+') as f:
        f.writelines(writable_task_str.rstrip())
    
    
        
def generate_reports():
    '''Function that reads in data from two input files used to store user credentials and task deta. Data is split into two sections: Task Overview and User overview. 

    - Under task overview general tasks stats are extrapolated from the data.
        * Total task count
        * Total user count
        * Total completed tasks
        * Total uncompleted tasks
        * Percentage incomplete tasks
        * Percentage overdue tasks
    
    - Under userview user specific tasks stats are extrapolated from the data.
        * Total tasks per user
        * Percentage of total tasks per user
        * Percentage complete tasks
        * Percentage uncomplete tasks
        * Percentage incomplete tasks
    '''
    
    # Initialize string, list and count variables.
    current_task_ov = ''
    current_user_ov = ''
    user_list = []
    task_count = []
    x = 0

    # Read in user and task data and store in list variables
    task_list = open('tasks.txt', 'r')
    task_list = [(item.strip()).split(', ') for item in task_list]
    user_list = open('user.txt', 'r')
    user_list = [(item.strip()).split(', ')[0] for item in user_list]
    
    # Initialize dictionary with userlist values as keys and empty lists as 
    # values. 
    tasks_dict = dict.fromkeys(user_list, [])

    # Loop/Condition that appends user tasksas values to the corresponding user keys.
    while True:
        task_list_copy = task_list.copy()
        user = user_list[x]
        tasks_dict[user] = [item for item in task_list_copy if user in item]
    
        if x == (len(user_list) - 1):
            break

        x += 1

    # Filtering task overview data from various data structures and 
    # storing in appropriate variables
    tot_tasks = len(task_list)
    tot_users = len(user_list)
    tot_complete = len([item for item in task_list if 'Yes' in item])
    tot_uncomplete = tot_tasks - tot_complete
    date_list = list([parse(item[4]) for item in task_list if 'No' in item])
    tot_incomplete = len([[item] for item in date_list if item < datetime.today()])
    date_list = list([parse(item[4]) for item in task_list])
    tot_overdue = len([[item] for item in date_list if item < datetime.today()])
 
    # Create formatted string with task data and append to string 
    # variable.
    current_task_ov = f'{tot_tasks}, '
    current_task_ov += f'{tot_complete}, '
    current_task_ov +=  f'{tot_uncomplete}, '
    current_task_ov += f'{tot_incomplete}, '
    current_task_ov += f'{round((tot_incomplete / tot_tasks) * 100)}%, '
    current_task_ov += f'{round((tot_overdue / tot_tasks) * 100)}%, '
    current_task_ov += f'{tot_users}\n'
 
    # Loop that extracts user/task data from dictionary, stores data in 
    # appropriate variables and appends data to string variable.
    for key in tasks_dict:
        if key:
            try:

                # Data extraction
                task_list = tasks_dict.get(key)
                task_count = len(task_list)    
                complete = len([item for item in task_list if 'Yes' in item])
                uncomplete = task_count - complete
                date_list = list([parse(item[4]) for item in task_list if 'No' in item])
                incomplete_count = len([[item] for item in date_list if item < datetime.today()])
 
                # Data assigning
                current_user_ov += f'{key}, '
                current_user_ov += f'{task_count}, ' + f'{round((task_count / tot_tasks) * 100)}%, '
                current_user_ov += f'{round((complete / task_count) * 100)}%, ' 
                current_user_ov += f'{round((uncomplete / task_count) * 100)}%, '
                current_user_ov += f'{round((incomplete_count / task_count) * 100)}%\n' 
 
            except ZeroDivisionError:
                current_user_ov += '\n'
                continue

    # Commit data to file            
    with open('task_overview.txt', 'w') as f:
        f.writelines(current_task_ov)
    # 
    with open('user_overview.txt', 'w') as f:
        f.writelines(current_user_ov)

    # Display confirmation message. 
    print('^==^ Reports Generated successfully!!\n')
    input('|Press any key to continue <==>\n')

    

def stats():   
    '''Function to display admin stats. Reads in data from two input files used to store user and task data stats. Includes input pauses between displays.''' 

    # Loop that checks if file exists. Creates file if false and runs the 
    # generate reports function.
    while True:
        try:
            task_overview = open('task_overview.txt', 'x')
            user_overview = open('user_overview.txt', 'x')
            generate_reports()
            break
        except FileExistsError:
            break

        
    # String headers and formatting
    header_0 = f'''
        \n{'*' * 80}
        \n{' ' * 29}Task List | Admin Stats
        \n{'*' * 80}'''
    sub_head_1 = f'|  Tasks created  |  Completed Tasks  |  Uncompleted Tasks |\n'
    sub_head_3 = f'''Task Count | % of all Tasks | % Completed\n'''
    sub_head_4 = f'''\n{" " * 52}% Uncompleted | % Incomplete\n'''
    sub_head_2 = f'''|  Incomplete Tasks | % Tasks Incomplete | % Tasks Overdue |\n'''
    
    # Loop that reads in task and userview data and stores in list 
    # variables.
    task_overview = [(item.strip()).split(', ') for item in open('task_overview.txt', 'r').readlines()]
            
    user_overview = [(item.strip()).split(', ') for item in open('user_overview.txt', 'r').readlines()]
            
    # Reset counter
    x = 0
    # assign indexed values and formatting data to string variables.
    tot_tasks = ' ' * 28 + task_overview[0][0]
    yes = ' ' * 20 + task_overview[0][1]
    no = ' ' * 21 + task_overview[0][2]
    incomplete = ' ' * 30 + task_overview[0][3]
    perc_incomplete = ' ' * 19 + task_overview[0][4]
    perc_uncomplete = ' ' * 17 + task_overview[0][5]
    tot_users = task_overview[0][6]
   
    # Display Header
    print(header_0)

    # Display Task overview data
    print(f'''{' ' * 20}{sub_head_1}
    \n{tot_tasks}{yes}{no}
    \n-|Task Overview|-{' ' * 3}|{'-_' * 29}|\n
    \n{' ' * 20}{sub_head_2}
    \n{incomplete}{perc_incomplete}{perc_uncomplete}''')
    print('-' * 80)

    input('\nPress Enter to proceed\n')

    print('-' * 80)
    print(f"{'>' * 30}-|User Overview|-{'<' * 33}")
    print(f"| User Count ==> {tot_users}{' ' * 16}{tot_tasks} <== Task Count |")
    print('-' * 80)
    
    # Loop that displays user overview data
    while x < len(user_overview):
        try:

            space = ' ' * (35- len(user_overview[x][0]))
            print(f'\n-|{user_overview[x][0]}|-{space}{sub_head_3}')
            print(f'''{" " * 45}{user_overview[x][1]}{" " * 12}{user_overview[x][2]}{" " * 12}{user_overview[x][3]}''')
            print(' ' * 37, '_-' * 21)
            print(sub_head_4)
            print(f'''{" " * 58}{user_overview[x][4]}{" " * 12}{user_overview[x][5]}''')
            print('-' * 80)

        except IndexError:

            print(f"\n{' ' * 56}No Data\n")
            print('-' * 80)
        
        x += 1

    input('\nPress Enter to proceed')
         
#====Login Section====#
# Declare empty list variable 'credentials' and
# set boolean variable 'login' and 'extendMenu' to 'False'
credentials = []
login = False
extendMenu = False

with open('user.txt', 'r') as f:
    # Process input file and store content in list variable
    for line in f:
        credentials.append(line.replace('\n', ''))
        
while login == False:
    # While boolean remains false repeat user inputs and
    # Declare string variable 'currentUser'
    # store as 'userInput' string variable
    print('''\nWelcome to Task Manager :)
            \nPlease input your Username and Password!!\n''')
    currentUser = input('UserName: ')
    userInput = f"{currentUser}, {input('Password: ')}"
    
    
    # check if input string matches string in list
    # If yes change boolean to true, if not throw error message
    if userInput in credentials:
        login = True
        print("\n***Successfully Authenticated***\n")

    elif userInput not in credentials:
        print("\nmmmmh Thats not right...!!\n")

#====Menu Section====#
while login == True:

    # Header
    print(f'''
        \n{'*' * 80}
        \n{' ' * 29}Task Manager | {currentUser}
        \n{'*' * 80}''')

    if currentUser == 'admin':
        print('\n')
        # presenting the menu to the admin user and 
        # making sure that the user input is coneverted to lower case.
        menu= input(f'''Select one of the following Options below:\n
r   - Registering a user
a   - Adding a task
va  - View all tasks
vm  - View my tasks
s   - Admin Stats
gr  - Generate reports    
e   - Exit\n
: ''').lower()
        print('\n')
        
        
    elif currentUser != 'admin':
        print('\n')
        # presenting the menu to the user and 
        # making sure that the user input is coneverted to lower case.
        menu= input(f'''Select one of the following Options below:
r   - Registering a user
a   - Adding a task
va  - View all tasks
vm  - view my task  
e   - Exit
: ''').lower()
        print('\n')

#====Function Calls====#
    if menu == 'r'and currentUser == 'admin':
        pass
        reg_user()

    elif menu == 'r' and currentUser != 'admin':
        #Throw error if Current user not an Admin
        print("You're barking up the wrong tree \nPlease ensure you are assogned to the appropriate UserGroup!!")

    elif menu == 'a':
        pass
        add_task()

    elif menu == 'va':
        pass
        view_all()
    
    elif menu == 'vm':
        pass
        view_mine(currentUser)

    elif menu == 's':
        pass
        stats()
    
    elif menu == 'gr':
        pass
        generate_reports()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    
    else:
        print("You have made a wrong choice, Please Try again")