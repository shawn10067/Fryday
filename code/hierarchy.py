# Fryday - A Peebody Service
# Gurshawn Lehal
# December 25th, 2020

import datetime 

# Get Date and Time
def get_date():

    current_date = datetime.datetime.today()

    # getting the date information
    day = (input("\tEnter day (enter 't' if your task is due tommorow): "))

    if day.isdigit() == False:
        if day == "t":
            time = datetime.time(12, 00)
            date = current_date + datetime.timedelta(days=1)
            return (date, time)
        else:
            print("\tNot valid, try again: ")
            day = (input("\tEnter day (enter 't' if your task is due tommorow): "))
            while day.isdigit() == False and day != "t":
                day = (input("\tEnter day (enter 't' if your task is due tommorow): "))

            if day == "t":
                time = datetime.time(24, 00)
                date = datetime.datetime.today() + datetime.timedelta(days=1)
                return (date, time)
            else:
                month = int(input("\tEnter month (0 if current): "))
                year = int(input("\tEnter year (0 if current): "))
                hour = int(input("\tEnter hour (00 if any time): "))
                minute = int(input("\tEnter minute (00 if any time): "))

                if year == 0 and month == 0:
                    date = datetime.datetime(current_date.year, current_date.month, int(day))
                elif year == 0:
                    date = datetime.datetime(current_date.year, month, int(day))
                elif month == 0:
                    date = datetime.datetime(year, current_date.year, int(day))
                else:
                    date = datetime.datetime(year, month, int(day))

                time = datetime.time(hour, minute)
                return (date, time)
    else:

        month = int(input("\tEnter month (0 if current): "))
        year = int(input("\tEnter year (0 if current): "))
        hour = int(input("\tEnter hour (00 if any time): "))
        minute = int(input("\tEnter minute (00 if any time): "))

        # formatting the information
        date = ""
        time = ""

        if year == 0 and month == 0:
            date = datetime.datetime(current_date.year, current_date.month, int(day))
        elif year == 0:
            date = datetime.datetime(current_date.year, month, int(day))
        elif month == 0:
            date = datetime.datetime(year, current_date.month, int(day))
        else:
            date = datetime.datetime(year, month, int(day))
        
        time = datetime.time(hour, minute)

        return (date, time)

class Field():
    # holds the information about a specified field

    # init
    def __init__(self, name, description, purpose, roadmap_link = "NONE"):
        self.name = name
        self.courses = []
        self.purpose = purpose
        self.roadmap_link = roadmap_link
        self.description = description

    # describing the field
    def describe_field(self):
        print("\n\tField: %s\n\tDescription: %s\n\tPurpose: %s\n\tRoadmap Link: %s"%(self.name, self.description, self.purpose, self.roadmap_link))
        print("\n\tCourses\n")
        for i in self.courses:
            print("\t\t%s"%(i.name))
        print()

    # text interpretation
    def database_description(self):
        field_description = "%s|%s|%s|%s|%s|"%("Field", self.name, self.description, self.purpose, self.roadmap_link)
        for i in self.courses:
            field_description += "\n%s"%(i.database_description())
        field_description += "\nDONE_FIELD,|\n"
        return field_description

    # add course from text
    def add_course(self, name, description, year, link, workload, bookmark, status):
        self.courses.append(Course(name, description, year, link, workload, bookmark, status))


    # add course from user
    def user_add_course(self):
        name = input("\tEnter course name: ")
        description = input("\tEnter course description: ")
        year = int(input("\tEnter year of course: "))
        link = input("\tEnter course link (if applicable): ")
        if link == "":
            link = "NONE"
        workload = input("\tEnter course workload (if applicable): ")
        if workload == "":
            workload = "NONE"
        bookmark = input("\tEnter bookmark (if applicable): ")
        if bookmark == "":
            bookmark = "NONE"
        status = "N" 

        self.courses.append(Course(name, description, year, link, workload, bookmark, status))

    # removing a course
    def remove_course(self, pos):
        print("\n\tDeleting %s"%(course[pos]))
        del self.courses[pos]


    # information the user wants

    # current courses
    def get_current_courses(self):
        print("\n%s\n\tCURRENT COURSES:"%(self.name))
        for course in self.courses:
            if course.course_status == "S":
                print("\n\t\t%s"%(course.name))

    # finished courses
    def get_finished_courses(self):
        print("\n\t%s\n\t\tFINISHED COURSES:"%(self.name))
        for course in self.courses:
            if course.course_status == "D":
                print("\n\t\t\t%s"%(course.name))

    # changing attributes for the course
    def change_name(self):
        self.name = input("\nEnter the new name for the field: ")
        print("\n\tName for the field has been changed.")

    def change_description(self):
        self.description = input("\nEnter the description: ")
        print("\n\tDescription has been changed.")

    def change_link(self):
        self.roadmap_link = input("Enter new link: ")
        print("\n\tRoadmap link has been changed to %s."%(self.link))

    def change_purpose(self):
        self.purpose = input("Enter new purpose: ")
        print("\n\tPurpose has been changed.")

    def __repr__(self):
        return "Field: %s; Link = %s"%(self.name, self.roadmap_link)

class Task():

    # init
    def __init__(self, description, date, time, status, course = "NONE"):
        self.description = description
        self.date = date
        self.time = time
        self.status = status
        self.course = course

    # finished task
    def finished_task(self):
        self.status = True 
        print("Finished")

    # string representation of task object
    def __repr__(self):
        date_string = self.date.strftime("%b %d, %Y")
        time_string = self.time.strftime("(%H:%M:%S)")
        return "\t%-25s: %-38s\n\t\tDue %s at %s\n"%(self.course, self.description.upper(), date_string, time_string)
        

    # change date
    def change_date(self):
        date = get_date()
        self.date = date[0]
        self.time = date[1]
        print("\n\tThe due date has been changed for: %s."%(self.description))

    # change description
    def change_description(self):
        self.description = input("\n\tEnter new description: ")
        print("\n\tThe description has been changed.")

    # text interpretation
    def database_description(self):
        return "%s|%s|%s|%s|%s|%s|%s|%s|%s|"%("Task", self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute, self.description, self.status, self.course)

class Course():
    # holds the infromation about a specified field

    # init
    def __init__(self, name, description, year, link = "NONE", workload = "NONE", bookmark = "NONE", status = "N"):
        self.name = name
        self.description = description
        self.year = year
        self.link = link
        self.tasks = []
        self.course_status = status
        self.workload = workload
        self.bookmark = bookmark

    # text interpretation
    def database_description(self):
        course_description = "%s|%s|%s|%s|%s|%s|%s|%s|"%("Course", self.name, self.description, self.year, self.link, self.workload, self.bookmark, self.course_status)
        for j in self.tasks:
            course_description += "\n%s"%(j.database_description())
        course_description += "\nDONE_COURSE,|"
        return course_description


    # started course
    def started_course(self):
        self.course_status = "S"
        print("\n\tMarked course as started.")

    # finished course
    def finished_course(self):
        self.course_status = "D"
        print("\n\tMarked course as finished.")

    # workload set
    def set_workload(self):
        self.workload = input("\n\tDescribe your workload: ")
        print("\n\tChanged workload.")

    # delete course task
    def delete_task(self, pos):
        del self.tasks[pos]
        print("\tTask Deleted.")

    # set chapter
    def set_bookmark(self):
        self.bookmark = input("\n\tState your bookmark/chapter location: ")
        print("\n\tSet bookmark to %s."%(self.bookmark))

    # set name
    def set_name(self):
        self.name = input("\n\tState new name: ")
        print("\n\tChanged name.")

    # set description
    def set_description(self):
        self.description = input("\n\tState new description: ")
        print("\n\tChanged description.")

    # set link
    def set_link(self):
        self.link = input("\n\tEnter the new link: ")
        print("\n\tChanged link to %s."%(self.link))

    # add task
    def add_task(self,year, month, day, hour, minute, description, status, course):
        task_time = datetime.time(hour, minute)
        task_date = datetime.date(year, month, day)
        self.tasks.append(Task(description, task_date, task_time, status, course))

    # user add task
    def user_add_task(self):
        task_description = input("\n\tState Task: ")
        date = get_date()
        self.tasks.append(Task(task_description, date[0], date[1], False, self.name)) 

    # delete a task
    def remove_task(self, pos):
        print("\n\tDeleting %s"%(self.tasks[pos]))
        del self.tasks[pos]

    # user requested infromation

    # print the archived tasks
    def get_archived_tasks(self):
        print("\n%s\n\tARCHIVED TASKS:"%(self.name))
        for task in self.tasks:
            if task.status == True:
                print("\n\t\t%s"%(task.description))

    # return the active tasks
    def get_active_tasks(self):
        active_tasks = []
        for task in self.tasks:
            if task.status == False:
                active_tasks.append(task)

        return active_tasks

    # string representation of course object
    def __repr__(self):
        return "\tCOURSE:%s, YEAR: %s"%(self.name, self.year)


    def describe_course(self):
        print("\n\tCourse: %s\n\tDescription: %s\n\tBookmark: %s\n\tWorkload: %s\n\tYear: %s\n\tLink: %s\n\tStatus: %s"%(self.name, self.description, self.bookmark, self.workload, self.year, self.link, self.course_status))
        print("\n\tTasks\n")
        print("\n\t\tCurrent:\n")
        for i in self.tasks:
            if i.status == False:
                print("\t\t\t%s"%(i.description))
        print("\n\t\tArchived:\n")
        for i in self.tasks:
            if i.status == True:
                print("\t\t\t%s"%(i.description))
        print()



