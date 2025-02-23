import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname="hiring", user="postgres", password="alooEsfenaj", host="localhost", port="5432"
    )

# Function to insert random persons
def insert_persons(cursor, num):
    for _ in range(num):
        cursor.execute(
            """
            INSERT INTO person (person_name, email, national_number, phone_number)
            VALUES (%s, %s, %s, %s)
            RETURNING person_id;
            """,
            (fake.name(), fake.unique.email(), fake.random_number(digits=10), f"09{random.randint(100000000, 999999999)}"),
        )

# Function to insert job positions
def insert_job_positions(cursor, num):
    for _ in range(num):
        cursor.execute("INSERT INTO job_position (title) VALUES (%s) RETURNING job_id;", (fake.unique.job()[:50],))

# Function to insert job openings
def insert_job_openings(cursor, num):
    cursor.execute("SELECT job_id FROM job_position;")
    job_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(num):
        cursor.execute(
            """
            INSERT INTO job_openning (job_position_id, title, details, openning_time, capacity)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING job_openning_id;
            """,
            (random.choice(job_ids), fake.unique.job()[:50], fake.text(), fake.date_time_this_year(), random.randint(1, 10)),
        )

# Function to insert skills
def insert_skills(cursor, skills):
    for skill in skills:
        cursor.execute("INSERT INTO skills (title) VALUES (%s) RETURNING skill_id;", (skill,))

def insert_job_openning_skills(cursor, num_records):
    # Get all job_openning_id
    cursor.execute("SELECT job_openning_id FROM job_openning")
    job_openning_ids = cursor.fetchall()
    job_openning_ids = [item[0] for item in job_openning_ids]

    # Get all skill_id
    cursor.execute("SELECT skill_id FROM skills")
    skill_ids = cursor.fetchall()
    skill_ids = [item[0] for item in skill_ids]

    for _ in range(num_records):
        job_openning_id = random.choice(job_openning_ids)
        skill_id = random.choice(skill_ids)

        # Check if the combination already exists
        cursor.execute("""
            SELECT COUNT(*) FROM job_openning_skills
            WHERE job_openning_id = %s AND skill_id = %s
        """, (job_openning_id, skill_id))
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
                INSERT INTO job_openning_skills (job_openning_id, skill_id)
                VALUES (%s, %s)
            """, (job_openning_id, skill_id))

# Function to insert requesters
def insert_requesters(cursor, num):
    cursor.execute("SELECT person_id FROM person;")
    person_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT job_openning_id FROM job_openning;")
    job_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(num):
        cursor.execute(
            """
            INSERT INTO requester (person_id, job_openning_id, person_resume, salary_expectation)
            VALUES (%s, %s, %s, %s);
            """,
            (random.choice(person_ids), random.choice(job_ids), fake.binary(length=100), random.randint(1000, 10000)),
        )

# Function to insert interviewees
def insert_interviewees(cursor):
    cursor.execute("SELECT requester_id FROM requester;")
    requester_ids = [row[0] for row in cursor.fetchall()]
    for requester_id in requester_ids:
        cursor.execute(
            """
            INSERT INTO interviewee (requester_id, interviewee_status)
            VALUES (%s, %s);
            """,
            (requester_id, random.choice(['accepted', 'rejected', 'withdrawed'])),
        )

# Function to insert offers
def insert_offers(cursor):
    cursor.execute("SELECT interviewee_id FROM interviewee;")
    interviewee_ids = [row[0] for row in cursor.fetchall()]
    for interviewee_id in interviewee_ids:
        cursor.execute(
            """
            INSERT INTO offer (interviewee_id, job_openning_id, recommended_payment, offer_status)
            VALUES (%s, (SELECT job_openning_id FROM job_openning ORDER BY RANDOM() LIMIT 1), %s, ROW(%s, %s));
            """,
            (interviewee_id, random.randint(1000, 10000), random.choice(['accepted', 'rejected', 'withdrawed']), fake.date_time_this_year()),
        )

# Function to insert employees
def insert_employees(cursor, num):
    cursor.execute("SELECT person_id FROM person;")
    person_ids = [row[0] for row in cursor.fetchall()]
    for i in range(num):
        cursor.execute(
            """
            INSERT INTO employee (person_id, salary, job_position_title, start_time)
            VALUES (%s, %s, %s, %s)
            RETURNING employee_id;
            """,
            (person_ids[i], random.randint(3000, 10000), fake.job()[:50], fake.date_time_this_year()),
        )

# Function to insert interviewers
def insert_interviewers(cursor):
    cursor.execute("SELECT employee_id FROM employee;")
    employee_ids = [row[0] for row in cursor.fetchall()]
    for employee_id in employee_ids:
        cursor.execute(
            """
            INSERT INTO interviewer (interviewer_id, interviewer_password)
            VALUES (%s, %s);
            """,
            (employee_id, fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)),
        )

# Function to insert hiring processes
def insert_hiring_processes(cursor):
    cursor.execute("SELECT job_openning_id FROM job_openning;")
    job_openning_ids = [row[0] for row in cursor.fetchall()]
    for job_openning_id in job_openning_ids:
        cursor.execute(
            """
            INSERT INTO hiring_process (job_openning_id)
            VALUES (%s)
            RETURNING hiring_process_id;
            """,
            (job_openning_id,),
        )

# Function to insert stages
def insert_stages(cursor, num):
    cursor.execute("SELECT hiring_process_id FROM hiring_process;")
    hiring_process_ids = [row[0] for row in cursor.fetchall()]
    for hiring_process_id in hiring_process_ids:
        for stage_num in range(1, num + 1):
            cursor.execute(
                """
                INSERT INTO stages (hiring_process_id, stage_number, stage_title, stage_description)
                VALUES (%s, %s, %s, %s);
                """,
                (hiring_process_id, stage_num, fake.word(), fake.text()),
            )

# Function to insert interview types
def insert_interview_types(cursor, num):
    cursor.execute("SELECT stage_id FROM stages;")
    stage_ids = [row[0] for row in cursor.fetchall()]
    for stage_id in stage_ids:
        for _ in range(num):
            cursor.execute(
                """
                INSERT INTO interview_type (stage_id, interview_type_title, time_duration)
                VALUES (%s, %s, %s);
                """,
                (stage_id, fake.word(), timedelta(minutes=random.randint(30, 90))),
            )

# Function to insert interviews
def insert_interviews(cursor):
    cursor.execute("SELECT interview_type_id FROM interview_type;")
    interview_type_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT interviewee_id FROM interviewee;")
    interviewee_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(len(interviewee_ids)):
        cursor.execute(
            """
            INSERT INTO interview (interview_type_id, interviewee_id, interview_status, enter_exit_time)
            VALUES (%s, %s, ROW(%s, %s), ROW(%s, %s));
            """,
            (random.choice(interview_type_ids), random.choice(interviewee_ids), random.choice(['accepted', 'rejected', 'canceled', 'pending']), fake.date_time_this_year(), fake.date_time_this_year(), fake.date_time_this_year() + timedelta(hours=1)),
        )

# Function to insert skill evaluations
def insert_skill_evaluations(cursor):
    cursor.execute("SELECT interview_id FROM interview;")
    interview_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT skill_id FROM skills;")
    skill_ids = [row[0] for row in cursor.fetchall()]
    for interview_id in interview_ids:
        for skill_id in random.sample(skill_ids, k=random.randint(1, len(skill_ids))):
            cursor.execute(
                """
                INSERT INTO skill_evaluation (interview_id, skill_id)
                VALUES (%s, %s);
                """,
                (interview_id, skill_id),
            )

# Function to insert interviewer comments
def insert_interviewer_comments(cursor):
    cursor.execute("SELECT interview_id, skill_id FROM skill_evaluation;")
    skill_evaluations = cursor.fetchall()
    cursor.execute("SELECT interviewer_id FROM interviewer;")
    interviewer_ids = [row[0] for row in cursor.fetchall()]
    for interview_id, skill_id in skill_evaluations:
        for interviewer_id in random.sample(interviewer_ids, k=random.randint(1, min(20, len(interviewer_ids)))):
            cursor.execute(
                """
                INSERT INTO interviewer_comments (interview_id, skill_id, interviewer_id, interviewer_score, interviewer_comment)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (interview_id, skill_id, interviewer_id, random.randint(1, 5), fake.text()),
            )

# Function to insert discussion members
def insert_discussion_members(cursor):
    cursor.execute("SELECT discussion_id FROM discussion;")
    discussion_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT interviewer_id FROM interviewer;")
    interviewer_ids = [row[0] for row in cursor.fetchall()]
    
    for discussion_id in discussion_ids:
        for _ in range(random.randint(1, 3)):  # Assuming 1 to 3 interviewers per discussion
            cursor.execute(
                """
                INSERT INTO discussion_member (discussion_id, interviewer_id, interviewer_text, interviewer_text_date)
                VALUES (%s, %s, %s, %s);
                """,
                (discussion_id, random.choice(interviewer_ids), fake.text(), fake.date_time_this_year())
            )

# Function to insert discussions
def insert_discussions(cursor):
    cursor.execute("SELECT interviewee_id FROM interviewee;")
    interviewee_ids = [row[0] for row in cursor.fetchall()]
    for interviewee_id in interviewee_ids:
        cursor.execute(
            """
            INSERT INTO discussion (interviewee_id)
            VALUES (%s)
            RETURNING discussion_id;
            """,
            (interviewee_id,),
        )


def main():
    conn = get_connection()
    cursor = conn.cursor()
    
    insert_persons(cursor, 2500)
    insert_job_positions(cursor, 200)
    insert_job_openings(cursor, 300)
    insert_skills(cursor, ["Python", "Java", "SQL", "Machine Learning", "Leadership", "Time management", "Customer service", "Social media management", "Financial planning",
                           "Content creation", "Copywriting", "Video editing", "Networking", "Cybersecurity", "Artificial intelligence",
                            "Statistical analysis", "Technical writing", "Database management", "Cloud computing", "Digital marketing",
                            "Sales strategies", "Teamwork", "Adaptability", "Conflict resolution",
                            "Communication", "Empathy", "Creativity", "Negotiation", "Decision making",
                            "Active listening", "Organizational skills", "Self-motivation", "Attention to detail", "Flexibility",
                            "Research", "Market analysis", "Software testing", "CAD design", "Event planning",
                            "Data visualization", "Marketing automation", "Risk management", "Customer relationship management (CRM)", 
                            "Programming in C++", "JavaScript", "HTML/CSS", "Product management", "Account management", "Financial analysis",
                            "Human resources", "Teaching", "Training", "Salesforce", "Business strategy"])
    insert_job_openning_skills(cursor, 100)
    insert_requesters(cursor, 700)
    insert_interviewees(cursor)
    insert_offers(cursor)
    insert_employees(cursor, 400)  # Number of employees
    insert_interviewers(cursor)
    insert_hiring_processes(cursor)
    insert_stages(cursor, 5)  # Number of stages
    insert_interview_types(cursor, 3)  # Number of interview types per stage
    insert_interviews(cursor)
    insert_skill_evaluations(cursor)
    insert_interviewer_comments(cursor)
    insert_discussions(cursor)
    insert_discussion_members(cursor)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Random data inserted successfully!")

if __name__ == "__main__":
    main()