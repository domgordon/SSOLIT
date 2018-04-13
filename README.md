# SSOLIT

Dominique Gordon dlg2156 and Andres Aguayo aa3642
SSOLIT

1) PostgreSQL account: aa3642
   
   Password: 5693
   
   If it's helpful: psql -U aa3642 -h 35.227.79.146 -d proj1part2

2) run the following command within the SSOLIT directory:
   python server.py
   Find our website at: 
   http://35.196.244.207:8111/

3) Breakdown of implementation of the proposal:

SSOLIT is a revised version of Columbia’s SSOL for students and professors, specifically the registration section. It will allow you (as a student) to see lists of available courses by department or professor: IMPLEMENTED -- this is our application and we think our app fulfills this purpose 

You then can either enroll yourself in the course if the course is not yet at capacity: IMPLEMENTED -- if you attempt to enroll in a course that is at capacity, you will be redirected to your profile page and shown a message explaining that the course is full at the top of the page

Registration capability will be dictated by various restrictions concerning the graduation year, school affiliation, and/or major of the student: NOT IMPLEMENTED -- because SSOLIT is for the students, not the professors/people posting courses so there was no place this could be specified. We also did not implement our databases this way in Part 2. We emailed Felipe for approval on leaving this feature out.

However, as an expansion of the original SSOL, there will be various additional features that the students might find helpful: IMPLEMENTED -- see below

For example, clicking on a professor’s name will show other courses and sections taught by that professor: IMPLEMENTED -- there is a search by professor last bar at the top of the all courses page that returns all the courses taught by the searched professors name. This uses the same query that the proposal version would have used. We emailed Felipe for approval on this change.

clicking on a course name will show the other available sections;: IMPLEMENTED -- similar to above, there is a search by course name bar at the top of the all courses page that returns all the available sections of courses that contain the search keyword (try searching just 'databases' for example). This uses the same query that the proposal version would have used. We emailed Felipe for approval on this change.

clicking on a department will show all courses listed for that department;: IMPLEMENTED -- similar to above, there is a search by department bar at the top of the all courses page that returns all the courses listed for that department. This uses the same query that the proposal version would have used. We emailed Felipe for approval on this change.

and clicking on the capacity of the course will show which students are already enrolled.: IMPLEMENTED -- if you radio select a course in All Courses and hit 'See more about this course,' a list of students who are already enrolled is included on this page. This uses the same query that the proposal version would have used.

Any invalid enrollments will throw a detailed error to the student about which specific restriction is at work.: IMPLEMENTED -- if a student attempts to enroll in a course that is at capacity, from a previous semester (not Spring 18 or Fall 18), or a course they are already enrolled in they will be redirected to their profile page to see the courses they are enrolled in and shown an error at the top of the page detailing why they weren't able to enroll in this course.

 There will be an advanced search function which a student will be able to use to search for a course by filling out any amount of fields such as course number, professor, course name, etc.: IMPLEMENTED -- as seen by all of the search and filter features at the top of the all courses page.

ADDITIONALLY IMPLEMENTED FEATURES:
- A profile/my courses page displaying the user's UNI, First Name, Last Name, and School
- Divisions on the profile page between current courses, future courses, and past courses
- Login Signup and Logout features
- Ability to filter by semester
- Ability to filter by number of credits
- Ability to enroll from both the all courses page and the more information page

4)
Our website contains the following web pages
- home
- sign up
- log in
- all courses
- more information
- my courses

We would have to say that of the above, the two webpages that contain the most interesting database operations are all courses and more information. 

In all courses, the filter features each require a different query that filters by varying attributes. Furthermore, the listing of courses links together the courses_offered, sections_available_taught, and the professor_works tables.

Also on all courses, the more information button passes through only the significant information the more function (course name, section number, semester), which we think is pretty cool. 

The radio options with two different submit buttons was a challenge to implement, but was very rewarding, and we think the way the information is passed between the pages (all courses and more information) is interesting in a multidimensional array.

Both pages use the enroll function, one of our best which calls upon various queries to make sure the enrollment is valid (not already enrolled, course isn't at capacity, course is for current or future semester) before ultimately calling upon a final query to enroll the student in the course.

On the more information page, the students enrolled are all displayed which is an interesting query linking students_attends and enrolled_in.


