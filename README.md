# Hiring Process Database

This project is a database system designed to help companies manage their hiring process more efficiently. It covers everything from job postings and applicant tracking to interviews, skill evaluations, and job offers. Built using **PostgreSQL**, the database includes advanced features like custom data types, indexing for better performance, and complex queries to handle real-world hiring scenarios.

## What’s This Project About?

The hiring process can be complicated, but this database simplifies it by breaking it down into clear, manageable parts:

1. **Job Positions and Openings**: Define job roles (like Software Engineer or Data Analyst) and create openings for those roles. Each opening includes details like how many people are needed and what skills are required.
2. **Applicants (Requesters)**: People applying for jobs can submit their resumes and salary expectations through the system.
3. **Interviews**: Applicants go through different interview stages, each with a specific format (e.g., technical or behavioral interviews). Interviewers evaluate applicants based on their skills.
4. **Offers**: If an applicant does well, they receive a job offer with details like salary recommendations.
5. **Skill Evaluations**: Interviewers score applicants on specific skills and leave comments to help with decision-making.
6. **Indexing**: To make sure everything runs smoothly, we’ve added indexing to speed up the database when handling large amounts of data.

---

## How the Database is Structured

The database is made up of several tables that work together to manage the hiring process. Here’s a quick overview of the main tables:

- **job_position**: Stores different job roles (e.g., Software Engineer, Data Analyst).
- **job_openning**: Tracks open positions for each role, including details like how many people are needed and what skills are required.
- **skills**: A list of skills that might be needed for different jobs.
- **job_openning_skills**: Connects skills to specific job openings.
- **hiring_process**: Manages the hiring process for each job opening.
- **person**: Stores personal information about applicants and employees.
- **requester**: Tracks applicants who have applied for jobs.
- **employee**: Stores information about current employees, like their job roles and salaries.
- **interviewer**: Manages the interviewers, who are employees with special access to evaluate applicants.
- **interviewee**: Tracks applicants who have been selected for interviews.
- **offer**: Manages job offers made to applicants.
- **stages**: Defines the different stages of the hiring process (e.g., initial screening, technical interview).
- **interview_type**: Specifies the types of interviews (e.g., behavioral, technical) for each stage.
- **interview**: Tracks interview sessions, including their status and timing.
- **skill_evaluation**: Records how applicants perform on specific skills during interviews.
- **interviewer_comments**: Stores comments and scores from interviewers about each skill.
- **discussion**: Manages discussions between interviewers about applicants.
- **discussion_member**: Tracks who participated in discussions and what they said.

---

## Key Features

- **Custom Data Types**: The database uses custom data types to handle complex information, like the status of job offers or interview sessions.
- **Complex Queries**: The project includes 10 detailed SQL queries to show how the database can handle real-world hiring scenarios.
- **Indexing**: We’ve added indexing to make the database faster and more efficient, especially when dealing with large amounts of data.
- **Random Data Generation**: A script is included to fill the database with random data, making it easy to test and experiment.

---

## Queries

The project includes 10 SQL queries that demonstrate how the database can be used in real-world situations. These queries cover things like finding job openings, tracking applicants, evaluating interview results, and managing job offers. They’re designed to show off the database’s flexibility and power.

---

## Indexing for Better Performance

To make sure the database runs smoothly, we’ve added indexing to the most important columns. This helps speed up queries, especially when dealing with large amounts of data. The results of this indexing, including how much faster the database performs, are documented in the project.

---

## How to Get Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/hiring-process-database.git
   cd hiring-process-database
   ```

2. **Set Up the Database**:
   - Run the `hiring_process.sql` script to create the database and tables:
     ```bash
     psql -U your-username -d your-database -f hiring_process.sql
     ```

3. **Insert Random Data**:
   - Use the provided script to fill the database with random data for testing.

4. **Run Queries**:
   - Try out the 10 complex queries to see how the database works.

5. **Check Indexing Results**:
   - Take a look at the documentation to see how indexing improved the database’s performance.
