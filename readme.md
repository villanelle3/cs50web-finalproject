# Quick guide

## Download required libraries

```commandline
pip install -r requirements.txt
```

## Run django app
How to run the application:

```commandline
python manege.py runserver
```
Make and apply migrations by running
```commandline
python manage.py makemigrations
```
 and

 ```commandline
python manage.py migrate
```

Go to website address and register an account.

## Requirements

Final project: CS50W: Web Programming with Python and JavaScript

Demo video: https://www.youtube.com/watch?v=vEbGA9JNWnw

Project title: Eduworld

## About this project

My final project is an educational platform that aims to simplify communication between students and teachers, distributing and grading assignments. In addition to providing a tool where students can ask questions and discuss educational issues and doubts in all subjects with all users.

the project was inspired by Google classroom, which was used a lot during the time I had online classes in college, and by Edmodo, an old platform for K-12 schools and teachers.

Eduworld enables teachers to share content, distribute assignments, and manage communication with students and colleagues.

The project was built using Django as a backend framework and JavaScript as a frontend programming language. All generated information are saved in database (SQLite by default).

All webpages of the project are mobile-responsive, using Bootstrap and custom CSS.


## Distinctiveness and Complexity

This project is different from the others carried out during the course and more complex.

The project is based on an original idea that has no similarity to any of the projects built as part of the CS50W course. Despite also allowing posts, which may be similar to what was done in Project 4, this is not the main functionality of the app. In addition to now being used a Rich Text editor, to enable improvement in the style of posts and facilitate communication. User profiles will also be created, but this time there is no possibility to follow or add users. Connections will be made automatically, based on which classes the user is enrolled in (if they are a student) or in which classes they teach (if they are a teacher). It will also be possible to add profile pictures directly from os. There are also 2 different types of user accounts, one for teachers and one for students, with different features in each of them.

On the teachers home page it is possible to create a new classroom by clicking on a button. Each class has a unique code, automatically generated by the backend. This code is used by students to enter the class. Checks are made to prevent the student from entering the same class twice. On the students' home page it is possible to enter classes by providing the correct code. The classes that the student/teacher is part of are highlighted on the homepage. Only student accounts are able to enroll in classes and only teacher accounts are able to create classes. Checks are done on all paths.

Entering the class page, we have a one page application, created using javascript:
* The most recent announcements posted in the class are displayed in the 'Stream' tab. Older posts are loaded on a button click, using Jquery, following the [documentation](https://api.jquery.com/). Both students and teachers can post announcements and both can respond. Comments are public to everyone in the classroom.

* The 'Classwork' tab displays all the assignments requested by the teacher for that class, with the title of the assignment, the due date, and a link that redirects to the assignment page, shown in a list. In the teacher account, this tab also contains the button to create a new assignment and buttons to cancel each assignment. In the student account, the status of the assignment is also highlighted, showing whether the student has already turned in the assignment, whether it has already been graded by the teacher or whether the student missed the deadline. Assignments due within 1 week are automatically highlighted on the classroom page sidebar, in order to alert students of deadlines and missing assignments.

    Teachers can create assignments at the click of a button. Then, the Assignment Title, Due date, Assignment description will be defined, in addition to the assignment itself being attached, which is expected to be a PDF file. All students are automatically given the 'Not submitted yet' status on this assignment.

    By clicking on the 'assignment details' button, users are redirected to another tab. Here, students can read the description, title and deadline of the work in detail, having the option of downloading the PDF or viewing it in a new tab.
If it is still within the deadline, this is also where students can submit their assignments, also attaching a PDF file. When the teacher assigns the grade, it can also be viewed here.
Students here can write comments, these are private and will only be seen by the commenter and the teacher.
Teachers on this page can edit information, view and reply to each private comment. They also have access to another 'Student Work' tab. In it, the teacher visualizes the work of each student and assigns grades.



* In the 'People' tab it is shown who the teacher of the class is, along with their photo and a link to their profile, and it is also shown each student who is enrolled in the class. In the teacher account it is possible to remove students, if necessary.

* In the teacher account we have an additional tab, 'Grades'. here is shown a table with the name of each student and each grade given to them. This makes it easy to keep track of each student.

Teachers can also edit classroom title and description.

The 'Forum' tab was designed to be a space for interaction between students. They can post questions and other users can respond. The most voted answers are highlighted.

Each question is in the most suitable category. You can use filters and search for specific categories. Here also jQuery was used.

In the navbar of the site there is a search option. this search shows profiles of students, professors and posts in forums compatible with the searched words.

In total, 14 models are used, more than 30 paths, in addition to many functions in python.



## Functionalities
Login is required!
1. Index page - `http://127.0.0.1:8000/`

2. Profile page - `http://127.0.0.1:8000/profile/${userid}`

3. Forum page - `http://127.0.0.1:8000/forum`

3. Classroom page - `http://127.0.0.1:8000/classroom/${classid}`

## Models

There are 14 models for the Eduworld database:

`User` : An extension of Django's `AbstractUser`

`Aluno`: Stores information about the student such as first name, last name, name of their school, and also education level (Primary [elementary] School, Midle School, Secondary [high] School or Postsecondary [tertiary] Education)

`Teacher`: Stores information about the teacher such as first name, last name, and also how they prefer to be called (Miss, Professor, Mrs., Mr., Dr.)

`Classe`: Stores information about the class such as the students who are enrolled and the teacher.

`ForumPost`: Model that stores data about the forum post

`ReplyForumComments`: Model that stores data from replies to forum posts

`Complementos`: Stores extra information about users such as profile pictures, connections, gadgets

`Gadgets`: Symbolic rewards for users. when conquered they are displayed in the profile. Extra gadgets will still be added

`ClassePosts`: Model that stores data about the classroom post


`ReplyPosts`: Model that stores data from replies to classroom posts

`PDFAssignments`: Stores details of assignments

`StatusAluno`: Stores grades and status of each student in each activity assigned to them.

`PrivateComments`: Stores private student-teacher comments

`ReplyPrivateComments`: Stores private Teacher-Student comments

## Files and directories

* `eduworld` - main application directory
** `static/eduworld` - contains all static content. Here are stored the CSS file and JS files used in the app. JavaScript files used in project:

        * `script.js` - script that run the LoadMore button in the classroom page.
        * `classePost.js` - script that post new comments.
        * `filter.js` - Filter forum posts by category.
        * `forumajax.js` - Post answers to forum posts.
        * `login.js` - Complements the login page, to differentiate students and teachers.
        * `newassig.js` - Handles the one page app of the assignment page for teacher.

    More scripts have been written into the HTML files themselves, for convenience.

    ** `templates/eduworld` - contains all application templates.

    * `admin.py` - used to determine models which will be used in the Django Admin Interface.

    * `models.py` - Definitive source of information about the data. It contains the essential fields and behaviors of the data stored. Each model maps to a single database table.

    * `urls.py` - defines all application paths.
    * `views.py` - contains all application views.

* `school` - project directory.

* `media` - stores user profile photos in addition to classroom PDF files.

### Features to be added in the future

* Create new Gadgets and clearer ways to conquer them
* Create new forms of interactions between students, such as communities, interactive games, among others.
* Enable the creation of multiple choice tests by teachers
* Create notification and email notification systems
