import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='localhost',
                database='test',  # test 데이터베이스 사용
                user='root',
                password='1111',  # mariadb 설치 당시의 패스워드, 실제 환경에서는 보안을 위해 환경변수 등을 사용
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")

    def save_bmr_record(self, gender, age, weight, height, life_style, expectation_bmr):
        """BMR 기록을 데이터베이스에 저장"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return False
                
            with self.connection.cursor() as cursor:
                query = """
                INSERT INTO bmr_records(gender, age, height, weight, life_style, expectation_bmr) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (gender, age, weight, height, life_style, expectation_bmr))
            
            self.connection.commit()
            print("BMR 기록이 성공적으로 저장되었습니다.")
            return True
        except Error as e:
            print(f"데이터 저장 중 오류 발생: {e}")
            return False

    def get_bmr_records(self, limit=10, offset=0):
        """페이징 처리된 BMR 기록을 가져옴"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT * FROM bmr_records
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """
                cursor.execute(query, (limit, offset))
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []

    def get_avgbmr_by_AgeGroup(self, limit=10):
        """연령대별 BMR 묶어서 가져옴"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with self.connection.cursor() as cursor:
                query = """
                SELECT 
                CASE 
                    WHEN age BETWEEN 10 AND 19 THEN '10대'
                    WHEN age BETWEEN 20 AND 29 THEN '20대'
                    WHEN age BETWEEN 30 AND 39 THEN '30대'
                    WHEN age BETWEEN 40 AND 49 THEN '40대'
                    WHEN age BETWEEN 50 AND 59 THEN '50대'
                    ELSE '60대 이상'
                END AS age_group,
                AVG(expectation_bmr) AS avg_bmr
            FROM bmr_records
            GROUP BY age_group
            ORDER BY age_group
                """
                cursor.execute(query, (limit,))
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []
    
    def count_bmr_records(self):
        """BMR 기록 개수 반환"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return 0
                
            with self.connection.cursor() as cursor:
                query = "SELECT COUNT(*) AS total FROM bmr_records"
                cursor.execute(query)
                result = cursor.fetchone() # 쿼리 결과의 첫 번째 행을 가져옵니다.
                return result['total'] if result else 0
        except Error as e:
            print(f"데이터 개수 조회 중 오류 발생: {e}")
            return 0
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")  