-- Create database
CREATE DATABASE blueoptimadashboard;
USE blueoptimadashboard;

-- Create developers table
CREATE TABLE developers (
    UID INT PRIMARY KEY,
    Developer_First_name VARCHAR(100),
    Developer_Last_name VARCHAR(100),
    Collection VARCHAR(100),
    Country VARCHAR(100),
    Employer VARCHAR(100),
    Segment VARCHAR(100),
    JobRole VARCHAR(100),
    HCL_Manager_email VARCHAR(255),
    Prod_Bucket VARCHAR(100),
    Engineer_Level VARCHAR(100)
);

-- Create developers_monthly_stats table
CREATE TABLE developers_monthly_stats (
    Stat_ID INT AUTO_INCREMENT PRIMARY KEY,
    UID INT,
    Year INT,
    Month TINYINT,
    Total_BCE DECIMAL(10,2),
    BCE_Per_Day DECIMAL(10,2),
    Tenure INT,
    Percentage_BCE DECIMAL(5,2),
    FOREIGN KEY (UID) REFERENCES developers(UID)
);

-- Create developers_daily_stats table
CREATE TABLE developers_daily_stats (
    Stat_ID INT AUTO_INCREMENT PRIMARY KEY,
    UID INT,
    Stat_Date DATE,
    Total_BCE DECIMAL(10,2),
    BCE_Per_Day DECIMAL(10,2),
    Tenure INT,
    Percentage_BCE DECIMAL(5,2),
    FOREIGN KEY (UID) REFERENCES developers(UID)
);

-- Sample insert for developers_monthly_stats
INSERT INTO developers_monthly_stats (
    UID, Year, Month, Total_BCE, BCE_Per_Day, Tenure, Percentage_BCE
) VALUES (
    101, 2025, 11, 150.75, 5.02, 24, 87.50
);

-- Sample insert for developers_daily_stats
INSERT INTO developers_daily_stats (
    UID, Stat_Date, Total_BCE, BCE_Per_Day, Tenure, Percentage_BCE
) VALUES (
    101, '2025-11-28', 5.02, 5.02, 24, 87.50
);
