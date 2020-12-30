# Fryday - A Peebody Service
# Gurshawn Lehal
# December 25th, 2020

# importing hierarchy and os module 
from hierarchy import Field
from hierarchy import Task
from hierarchy import Course 
import os
import datetime

# function to update tasks and courses
def update_secondary_lists(fields, current_course_output, current_task_output):
    current_course_output.clear()    
    current_task_output.clear()
    for field in fields:
        for course in field.courses:
            if course.course_status == 'S':
                current_course_output.append(course)
            current_set_of_tasks = course.get_active_tasks()
            for i in current_set_of_tasks:
                current_task_output.append(i)


# function to return a sorted array based on time
def sort_time(i_list):
    # i_list.sort(key=lambda item:item['date'], reverse=True)
    return sorted(i_list, key=lambda x: x.date.strftime("%Y/%d/%m/"), reverse = True)

# asking the main question
def ask_question():
    return input("\n\tWould you like to list ('l') or change ('c') contents? ('q' to quit): ")

# asking what they want to list
def list_question():
    return int(input("\n\tWhat do you want to list?\n\t[0] Active Tasks\n\t[1] Current Courses\n\t[2] Description of a Course\n\t[3] Description of a Field\n\t[4] Archived Tasks\n\t[5] Archived Courses\n\t: "))

def change_question():
    return int(input("\n\tWhat do you want to do?\n\t[0] Add\n\t[1] Change Attributes\n\t[2] Delete.\n\t: "))

def determine_catagory():
    return int(input("\n\tWhat would you like to operate on? \n\t[0] Task\n\t[1] Course\n\t[2] Field.\n\t: "))

# reading enumerated array contents function
def read_contents(array):
    for (index, content) in enumerate(array):
        print("\t[%-3d] %s."%(index, content))

# initializing variables 
file_name = ""

fields = [] 

#holding objects
current_tasks = [] #DONE
sorted_current_tasks = []
current_courses = [] #DONE

archived_tasks = [] #DONE
finished_courses = [] #DONE

# backup file
backup = open("backup.txt", 'w')

# get the file name
answer = input("\tWould you like to open an existing file ('y' or 'n'): ")
existing_file = True 
current_file = ""

if answer.lower() == 'n':
    file_name = input("\tEnter a file name: ") 
    full_file = "data/" + file_name + ".txt"
    existing_file = False
    current_file = open(full_file, 'w')
else:
    file_name = input("\tEnter the catagory you wish to Fry (file name excluding extention): ")
    while not os.path.isfile("data/%s.txt"%file_name):
        file_name = input("\tInvalid file, try again: ")
    existing_file = True
    full_file = "data/" + file_name + ".txt"
    current_file = open(full_file, 'r')
# openining the file reading the contents 


if existing_file == True:
    # populating array(s)
    field_number = 0
    course_number = 0

    line = current_file.readline()
        #populating base array(s)
    while line != "":
        backup.write(line)
        # identifying line contents
        split_line = line.split("|")
        line_catagory = split_line[0]

        # if we are done a field or course, we continue and reset the value(s)
        if line_catagory == "DONE_COURSE,":
            course_number += 1
        elif line_catagory == "DONE_FIELD,":
            course_number = 0
            field_number += 1
            line = current_file.readline()
            continue

        #if it is a field, course, or task, we do the appropirate task
        if line_catagory == "Field":
            fields.append(Field(split_line[1],split_line[2],split_line[3],split_line[4]))
        elif line_catagory == "Course":
            fields[field_number].add_course(split_line[1], split_line[2], split_line[3], split_line[4], split_line[5], split_line[6], split_line[7])
        elif line_catagory == "Task":
            task_status = True
            if split_line[7] == "False":
                task_status = False
            elif split_line[7] == "True":
                task_status = True


            fields[field_number].courses[course_number].add_task(int(split_line[1]), int(split_line[2]), int(split_line[3]), int(split_line[4]), int(split_line[5]), split_line[6], task_status, split_line[8])

        line = current_file.readline()

        # populating secondary arrays

    # getting current tasks
    update_secondary_lists(fields, current_courses, current_tasks) 

    # sorting the tasks based on time
    sorted_current_tasks = sort_time(current_tasks)


# prompting the user (main program)

print("\n\tWELCOME TO FRYDAY.\n\tYou have %s fields and %s active tasks."%(len(fields), len(current_tasks)))
print("\n"+"-"*50)
answer = ask_question()

while answer != 'q':
    try:
        while answer.lower() not in ['l', 'c', 'q']:
            print("\n\tSorry, I didn't get that")
            answer = ask_question()

        if answer.lower() == 'l':

            # if the answer is not valid, ask again
            list_answer = list_question()
            while list_answer not in [0,1,2,3,4,5]:
                print("\n\tSorry, we didn't get that.")
                list_answer = list_question()

            if list_answer == 0:
                read_contents(sorted_current_tasks)
            elif list_answer == 1:
                for i in fields:
                    i.get_current_courses()
            elif list_answer == 2:
                read_contents(current_courses)
                course_answer = int(input("\n\tSelect the course you would like to get the description of (0 if none): "))

                if course_answer < 0 or course_answer > (len(current_courses) - 1):
                    print("\n\tAnswer out of range.")
                    answer = ask_question()
                    continue

                print(current_courses[course_answer])
            elif list_answer == 3:
                read_contents(fields)
                field_answer = int(input("\n\tSelect the field you would like to get the description of (0 if none): "))
                
                if field_answer < 0 or field_answer > (len(fields) - 1):
                    print("\nAnswer out of range.")
                    answer = ask_question()
                    continue

                fields[field_answer].describe_field()
            elif list_answer == 4:
                for i in fields:
                    for course in i.courses:
                        course.get_archived_tasks()
            elif list_answer == 5:
                for i in fields:
                    i.get_finished_courses()
            else:
                print("\n\tInvalid option, try again")
        elif answer.lower() == 'c':

            # if the answer is not valid, ask again
            change_answer = change_question()
            while change_answer not in [0,1,2]:
                print("\n\tSorry, I didn't get that.")
                change_answer = change_question()

            if change_answer == 0:
                catagory = determine_catagory()

                # if the catagory is not valid, ask again
                while catagory not in [0,1,2]:
                    print("\n\tSorry, I didn't get that.")
                    catagory = determine_catagory()

                if catagory == 0:

                    read_contents(fields)
                    field_add = int(input("\n\tSelect the appropirate field for the task (0 if none): "))
                    if field_add < 0 or field_add > (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    valid_indexes = []
                    for index, course in enumerate(fields[field_add].courses):
                        if course.course_status == "S":
                            valid_indexes.append(index)
                            print("\n\t[%-3d] %s"%(index, course.name))

                    task_add = int(input("\n\tSelect the appropirate course for the task (0 if none): "))
                    if task_add not in valid_indexes:
                        print("\n\tCouldn't find the appropirate course.")
                        answer = ask_question()
                        continue

                    # add task to course
                    fields[field_add].courses[task_add].user_add_task()

                    # add the task to current task, and sort again

                if catagory == 1:
                    read_contents(fields)

                    course_add = int(input("\n\tSelect the appropirate field for the course (0 if none): "))
                    if course_add < 0 or course_add > (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    fields[course_add].user_add_course()
                if catagory == 2:
                    name = input("\tEnter name: ")
                    description = input("\tEnter description: ") 
                    purpose = input("\tEnter purpose: ")
                    road_map = input("\tEnter roadmap link (if its NA, then put nothing): ")

                    if road_map == "":
                        road_map = "NONE"

                    fields.append(Field(name, description, purpose, road_map))

            elif change_answer == 1:
                catagory = determine_catagory()

                # if the catagory is not valid, ask again
                while catagory not in [0,1,2]:
                    print("\n\tSorry, I didn't get that.")
                    catagory = determine_catagory()

                if catagory == 0:
                    read_contents(fields)

                    field_task_selection = int(input("\n\tSelect the appropirate field for the task (0 if none): "))
                    if field_task_selection < 0 or field_task_selection > (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    read_contents(fields[field_task_selection].courses)

                    course_selection = int(input("\n\tSelect the appropirate course (0 if none): "))
                    if course_selection < 0 or course_selection > (len(fields[field_task_selection].courses) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    read_contents(fields[field_task_selection].courses[course_selection].tasks)
                    task_selection = int(input("\n\tSelect the appropirate task (0 if none): "))

                    operation = int(input("\n\tWhat would you like to do? \n\t[0] Mark task as finished. \n\t[1] Change date of task. \n\t[2] Change description. \n\t: "))

                    if operation == 0:
                        fields[field_task_selection].courses[course_selection].tasks[task_selection].finished_task()
                    elif operation == 1:
                        fields[field_task_selection].courses[course_selection].tasks[task_selection].change_date()
                    elif operation == 2:
                        fields[field_task_selection].courses[course_selection].tasks[task_selection].change_description()
                    else:
                        print("\n\tInvalid operation.")

                elif catagory == 1:
                    read_contents(fields)

                    field_course_selection = int(input("\n\tSelect the appropirate field for the course (0 if none): "))
                    if field_course_selection < 0 or field_course_selection > (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    read_contents(fields[field_course_selection].courses)

                    course_selection = int(input("\n\tSelect the appropirate course (0 if none): "))
                    if course_selection < 0 or course_selection > (len(fields[field_course_selection].courses) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    operation = int(input("\n\tWhat would you like to do? \n\t[0] Mark course as started. \n\t[1] Mark course as finished. \n\t[2] Change workload. \n\t[3] Set bookmark. \n\t[4] Change name. \n\t[5] Change description. \n\t[6] Change link. \n\t: "))

                    if operation == 0:
                        fields[field_course_selection].courses[course_selection].started_course()
                    elif operation == 1:
                        fields[field_course_selection].courses[course_selection].finished_course()
                    elif operation == 2:
                        fields[field_course_selection].courses[course_selection].set_workload()
                    elif operation == 3:
                        fields[field_course_selection].courses[course_selection].set_bookmark()
                    elif operation == 4:
                        fields[field_course_selection].courses[course_selection].set_name()
                    elif operation == 5:
                        fields[field_course_selection].courses[course_selection].set_description()
                    elif operation == 6:
                        fields[field_course_selection].courses[course_selection].set_link()
                    else:
                        print("\n\tInvalid operation.")

                elif catagory == 2:
                    read_contents(fields)

                    field_selection = int(input("\n\tSelect the appropirate field to change (0 if none): "))
                    if field_selection < 0 or field_selection> (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    operation = int(input("\n\tWhat would you like to do? \n\t[0] Change name. \n\t[1] Change description. \n\t[2] Change purpose. \n\t[3] Change roadmap link. : "))

                    if operation == 0:
                        fields[field_selection].change_name()
                    elif operation == 1:
                        fields[field_selection].change_description()
                    elif operation == 2:
                        fields[field_selection].change_purpose()
                    elif operation == 3:
                        fields[field_selection].change_link()

            elif change_answer == 2:
                catagory = determine_catagory()

                 # if the catagory is not valid, ask again
                while catagory not in [0,1,2]:
                    print("\n\tSorry, I didn't get that.")
                    catagory = determine_catagory()


                if catagory == 0:
                    read_contents(fields)

                    field_del = int(input("\n\tSelect the appropirate field for the task (0 if none): "))
                    if field_del < 0 or field_del > (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    read_contents(fields[field_del].courses)

                    course_del = int(input("\n\tSelect the appropirate course for the task (0 if none): "))
                    if course_del < 0 or course_del > (len(fields[field_del].courses)):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    read_contents(fields[field_del].courses[course_del].tasks)
                    
                    task_del = int(input("\n\tSelect the appropirate task to delete (0 if none): "))
                    if task_del < 0 or task_del > (len(fields[field_del].courses[course_del].tasks[task_del]) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    fields[field_del].courses[course_del].delete_task(task_del)
                    print("\n\tTask deleted.")

                elif catagory == 1:
                    read_contents(fields)

                    field_del = int(input("\n\tSelect the appropirate field for the course (0 if none): "))
                    if field_del < 0 or field_del > (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    read_contents(fields[field_del].courses)

                    course_del = int(input("\n\tSelect the appropirate course to delete (0 if none): "))
                    if course_del < 0 or course_del > (len(fields[field_del].courses)):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    del fields[field_del].courses[course_del]
                    print("\n\tCourse deleted.")

                elif catagory == 2:
                    read_contents(fields)

                    field_del = int(input("\n\tSelect the appropirate field to delete (0 if none): "))
                    if field_del < 0 or field_del > (len(fields) - 1):
                        print("\n\tAnswer out of range.")
                        answer = ask_question()
                        continue

                    del fields[field_del]
                    print("\n\tField deleted.")


        update_secondary_lists(fields, current_courses, current_tasks) 
        sorted_current_tasks = sort_time(current_tasks)
        print("\n"+"-"*50)
        answer = ask_question()
    except:
        update_secondary_lists(fields, current_courses, current_tasks) 
        sorted_current_tasks = sort_time(current_tasks)
        print("\n"+"-"*50)
        answer = ask_question()
        continue

# writing output to the file

backup.close()

if existing_file:
    current_file.close()
    os.remove(full_file)
    with open (full_file, 'w') as new_file:
        for field in fields:
            new_file.write("%s"%(field.database_description()))
else:
    for field in fields:
        new_file.write("%s"%(field.database_description()))
    current_file.close()



