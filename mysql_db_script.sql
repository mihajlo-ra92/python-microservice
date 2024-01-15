CREATE DATABASE users_db;

USE users_db;

CREATE TABLE Users (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(30) NOT NULL UNIQUE,
password VARCHAR(30) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
user_type ENUM ('WORKER', 'EMPLOYER', 'ADMIN') NOT NULL
);

CREATE DATABASE jobs_db;

USE jobs_db;

CREATE TABLE Jobs (
id VARCHAR(255) PRIMARY KEY,
employer_id VARCHAR(255) NOT NULL,
worker_id VARCHAR(255),
job_name VARCHAR(50) NOT NULL,
job_desc VARCHAR(255),
pay_in_euro FLOAT,
completed BOOL
);

CREATE DATABASE applications_db;

USE applications_db;

CREATE TABLE Applications (
    id VARCHAR(60) PRIMARY KEY,
    worker_id VARCHAR(60) NOT NULL,
    job_id VARCHAR(60) NOT NULL,
    description VARCHAR(500) NOT NULL,
    status ENUM('PENDING', 'APPROVED', 'REJECTED') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE DATABASE users_db_test;
USE users_db_test;

CREATE TABLE Users (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(30) NOT NULL UNIQUE,
password VARCHAR(30) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
user_type ENUM ('WORKER', 'EMPLOYER', 'ADMIN') NOT NULL
);

CREATE DATABASE jobs_db_test;
USE jobs_db_test;

CREATE TABLE Jobs (
id VARCHAR(255) PRIMARY KEY,
employer_id VARCHAR(255) NOT NULL,
worker_id VARCHAR(255),
job_name VARCHAR(50) NOT NULL,
job_desc VARCHAR(255),
pay_in_euro FLOAT,
completed BOOL
);

CREATE DATABASE applications_db_test;

USE applications_db_test;

CREATE TABLE Applications (
    id VARCHAR(60) PRIMARY KEY,
    worker_id VARCHAR(60) NOT NULL,
    job_id VARCHAR(60) NOT NULL,
    description VARCHAR(500) NOT NULL,
    status ENUM('PENDING', 'APPROVED', 'REJECTED') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
