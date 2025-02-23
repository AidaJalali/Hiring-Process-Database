-- 401106674 :یسنا نوشیروانی 
-- آیدا جلالی : 401170542

-- CREATE DATABASE hiring;

CREATE Type acceptence_status_type AS ENUM ('accepted','rejected','withdrawed');
CREATE TYPE session_status_type AS ENUM('accepted','rejected','canceled','pending');

CREATE TYPE offer_status_type AS(
    acceptence_status acceptence_status_type,
    offer_status_time TIMESTAMP
);

CREATE TYPE enter_exit_time_type As(
    enter_time TIMESTAMP,
    exit_time TIMESTAMP
);

CREATE TYPE interview_status_type As(
    session_status session_status_type,
    session_status_time TIMESTAMP
);

CREATE TABLE job_position(
    job_id SERIAL PRIMARY KEY,
    title VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE job_openning(
    job_openning_id SERIAL PRIMARY KEY,
    job_position_id INT REFERENCES job_position(job_id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(50) UNIQUE NOT NULL,
    details TEXT,
    openning_time TIMESTAMP,
    capacity INT,
    UNIQUE(job_position_id,title)
);

CREATE TABLE skills(
    skill_id SERIAL PRIMARY KEY,
    title VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE job_openning_skills(
    skill_id INT REFERENCES skills(skill_id) ON DELETE CASCADE NOT NULL,
    job_openning_id INT REFERENCES job_openning(job_openning_id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE hiring_process(
    hiring_process_id SERIAL PRIMARY KEY,
    job_openning_id INT REFERENCES job_openning(job_openning_id) ON DELETE CASCADE UNIQUE NOT NULL
);

CREATE TABLE person(
    person_id SERIAL PRIMARY KEY,
    person_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~ '^[^@]+@[^@]+\.[^@]+$'),
    national_number VARCHAR(20) UNIQUE CHECK (national_number ~ '^\d+$'),
    phone_number VARCHAR(20) NOT NULL UNIQUE CHECK (phone_number ~  '^(0|\\+98)?9[0-9]{9}$')
);

CREATE TABLE requester(
    requester_id SERIAL PRIMARY KEY,
    person_id INT REFERENCES person(person_id) ON DELETE CASCADE NOT NULL,
    job_openning_id INT REFERENCES job_openning(job_openning_id) ON DELETE CASCADE NOT NULL,
    person_resume BYTEA NOT NULL,
    salary_expectation DECIMAL(10,0)
);

CREATE TABLE employee(
    employee_id SERIAL PRIMARY KEY,
    person_id INT REFERENCES person(person_id) ON DELETE CASCADE UNIQUE NOT NULL,
    salary DECIMAL(10,0),
    job_position_title VARCHAR(50),
    start_time TIMESTAMP
);

CREATE TABLE interviewer(
    interviewer_id INT PRIMARY KEY REFERENCES employee(employee_id) ON DELETE CASCADE,
    interviewer_password VARCHAR(100) CHECK (interviewer_password ~ '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?":{}|<>+_]).{8,}$')
);

CREATE TABLE interviewee(
    interviewee_id SERIAL PRIMARY KEY,
    requester_id INT REFERENCES requester(requester_id) ON DELETE CASCADE UNIQUE NOT NULL,
    interviewee_status acceptence_status_type
);

CREATE TABLE offer(
    offer_id SERIAL PRIMARY KEY,
    interviewee_id INT REFERENCES interviewee(interviewee_id) ON DELETE CASCADE NOT NULL,
    job_openning_id INT REFERENCES job_openning(job_openning_id) ON DELETE CASCADE NOT NULL,
    recommended_payment DECIMAL(10,0),
    offer_status offer_status_type
);

CREATE TABLE stages(
    stage_id SERIAL PRIMARY KEY,
    hiring_process_id INT REFERENCES hiring_process(hiring_process_id) ON DELETE CASCADE NOT NULL,
    stage_number INT NOT NULL,
    stage_title VARCHAR(20) NOT NULL,
    stage_description TEXT,
    UNIQUE(stage_number,hiring_process_id)
);


CREATE TABLE interview_type(
    interview_type_id SERIAL PRIMARY KEY,
    stage_id INT REFERENCES stages(stage_id) ON DELETE CASCADE NOT NULL,
    interview_type_title VARCHAR(20),
    time_duration INTERVAL
);

CREATE TABLE interview(
    interview_id SERIAL PRIMARY KEY,
    interview_type_id INT REFERENCES interview_type(interview_type_id) ON DELETE CASCADE NOT NULL,
    interviewee_id INT REFERENCES interviewee(interviewee_id) ON DELETE CASCADE NOT NULL,
    interview_status interview_status_type,
    enter_exit_time enter_exit_time_type
);

CREATE TABLE skill_evaluation(
    interview_id INT REFERENCES interview(interview_id) ON DELETE CASCADE NOT NULL,
    skill_id INT REFERENCES skills(skill_id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (interview_id,skill_id)
);

CREATE TABLE interviewer_comments(
    interview_id INT NOT NULL,
    skill_id INT NOT NULL,
    interviewer_id INT REFERENCES interviewer(interviewer_id) ON DELETE CASCADE NOT NULL,
    interviewer_score INT NOT NULL,
    interviewer_comment TEXT,
    PRIMARY KEY (interview_id,skill_id,interviewer_id),
    FOREIGN KEY (interview_id,skill_id) REFERENCES skill_evaluation(interview_id,skill_id) ON DELETE CASCADE
);

CREATE TABLE discussion(
    discussion_id SERIAL PRIMARY KEY,
    interviewee_id INT REFERENCES interviewee(interviewee_id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE discussion_member(
    discussion_member SERIAL PRIMARY KEY,
    discussion_id INT REFERENCES discussion(discussion_id) ON DELETE CASCADE NOT NULL,
    interviewer_id INT REFERENCES interviewer(interviewer_id) ON DELETE CASCADE NOT NULL,
    interviewer_text TEXT,
    interviewer_text_date TIMESTAMP
);