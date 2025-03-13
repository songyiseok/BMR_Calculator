USE test;  

-- 테이블 생성
CREATE TABLE IF NOT EXISTS bmr_records(
	id INT AUTO_INCREMENT PRIMARY KEY,
	gender varchar(20) NOT NULL,
	age INT NOT NULL,
	height FLOAT NOT NULL,
	weight FLOAT NOT NULL,
	life_style varchar(100) NOT NULL,
	expectation_bmr FLOAT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);