CREATE DATABASE users_db;

USE users_db;

CREATE TABLE Users (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(30) NOT NULL UNIQUE,
password VARCHAR(30) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
user_type ENUM ('WORKER', 'EMPLOYER', 'ADMIN') NOT NULL
);

INSERT INTO Users (id, username, password, email, user_type)
VALUES 
('1bb53018-b1dc-11ed-875c-45eb8b791582', 'miki', '123', 'miki@gmail.com', 'EMPLOYER'),
('6a54a320-b1dc-11ed-875c-45eb8b791582', 'marko', '123', 'marko@gmail.com','WORKER'),
('7247bc7a-b1dc-11ed-875c-45eb8b791582', 'nikola', '123', 'nikola@gmail.com', 'EMPLOYER'),
('7bd3a8e4-b1dc-11ed-875c-45eb8b791582', 'vanja', '123', 'vanja@gmail.com', 'WORKER');

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

INSERT INTO Jobs (id, employer_id, worker_id, job_name, job_desc, pay_in_euro, completed)
VALUES 
('15ae30c6-b1fe-11ed-875c-45eb8b791582','1bb53018-b1dc-11ed-875c-45eb8b791582', '7bd3a8e4-b1dc-11ed-875c-45eb8b791582', 'Leaf Raking', 'I need someone to rake the leaves in my backyard', 20.0, false),
('4e29f00a-b200-11ed-875c-45eb8b791582','1bb53018-b1dc-11ed-875c-45eb8b791582', '6a54a320-b1dc-11ed-875c-45eb8b791582', 'Grass mowing', 'I need someone to mow the grass in my backyard', 25.0, true),
('59ff3e4e-b200-11ed-875c-45eb8b791582','1bb53018-b1dc-11ed-875c-45eb8b791582', NULL, 'Apple picking', 'I need someone to pick the apples in my backyard', 10.0, false),
('24b4af14-b1fe-11ed-875c-45eb8b791582','7247bc7a-b1dc-11ed-875c-45eb8b791582', '6a54a320-b1dc-11ed-875c-45eb8b791582', 'Mopping', 'I need someone to mop the floor of my auto shop', 35.0, true),
('2c5d4f28-b1fe-11ed-875c-45eb8b791582','7247bc7a-b1dc-11ed-875c-45eb8b791582', '7bd3a8e4-b1dc-11ed-875c-45eb8b791582', 'Overnight security', 'I need someone to watch my auto shop during the night', 15.0, false);

CREATE DATABASE users_test_db;
USE users_test_db;

CREATE TABLE Users (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(30) NOT NULL UNIQUE,
password VARCHAR(30) NOT NULL,
email VARCHAR(50) NOT NULL UNIQUE,
user_type ENUM ('WORKER', 'EMPLOYER', 'ADMIN') NOT NULL
);

CREATE DATABASE jobs_test_db;
USE jobs_test_db;

CREATE TABLE Jobs (
id VARCHAR(255) PRIMARY KEY,
employer_id VARCHAR(255) NOT NULL,
worker_id VARCHAR(255),
job_name VARCHAR(50) NOT NULL,
job_desc VARCHAR(255),
pay_in_euro FLOAT,
completed BOOL
);