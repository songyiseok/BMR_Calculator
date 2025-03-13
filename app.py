# 사전 설치 : pip install flask pymysql
from flask import Flask, render_template, request, redirect, url_for, Response
from bmr import BMRCalculator
from db import Database
import atexit
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd



app = Flask(__name__)
db = Database()

# 애플리케이션 종료 시 DB 연결 종료
atexit.register(db.close)

@app.route('/', methods=['GET'])
def index():
    return render_template('team02_index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        gender = request.form.get('gender', '')  # KeyError 방지
        if not gender:  # 성별이 선택되지 않은 경우
            return render_template("team02_index.html", error="성별을 체크하세요.")
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        life_style = request.form['life_style']  # 문자열 그대로 유지
        
        # 🔥 입력값 확인용 출력 (디버깅)
        print(f"입력값 확인 - 성별: {gender}, 나이: {age}, 키: {height}, 체중: {weight}, 생활습관: {life_style}")

        # 숫자로 변환 (ValueError 발생 가능)
        age = int(age)
        height = float(height)
        weight = float(weight)
        
        # 입력값 유효성 검사
        if weight <= 0 or height <= 0 or age <= 0:
            return render_template('team02_index.html', error="나이, 체중, 신장은 양수여야 합니다.")
        
        # BMR 계산
        calculator = BMRCalculator(gender, age, height, weight, life_style)
        result = calculator.get_result()
        
        # 데이터베이스에 저장
        db.save_bmr_record(gender, age, height, weight, life_style,
                           expectation_bmr=result["expectation_bmr"])
        
        return render_template('team02_result.html',
                              expectation_bmr=result["expectation_bmr"],
                              gender=gender,
                              age=age,
                              height=height,
                              weight=weight,
                              life_style=life_style)
    except ValueError:
        return render_template('team02_index.html', error="유효한 숫자를 입력해주세요.")

@app.route('/history')
def history():
    page = request.args.get('page', 1, type=int)  # 기본 페이지는 1 / URL에서 page 값을 가져옴
    per_page = 10  # 한 페이지당 표시할 데이터 개수
    offset = (page - 1) * per_page  # SQL OFFSET 값 계산 / 몇 개를 건너뛸지 정하는 숫자

    # ✅ 전체 기록 개수 조회
    total_records = db.count_bmr_records() # 데이터베이스에서 총 기록 개수를 가져와요
    total_pages = (total_records + per_page - 1) // per_page  # 총 페이지 수 계산

    # ✅ 페이징 처리된 데이터 가져오기
    records = db.get_bmr_records(limit=per_page, offset=offset)  # 모든 데이터를 가져오지 않고, 필요한 만큼만 가져오는 것

    return render_template(
        'team02_history.html',
        records=records,
        page=page,
        total_pages=total_pages
    )


@app.route('/plot/male')
def plot_male_bmr():
    return generate_bmr_plot(gender='남성')

@app.route('/plot/female')
def plot_female_bmr():
    return generate_bmr_plot(gender='여성')

def generate_bmr_plot(gender): # 입력된 성별에 따라 사용자 BMR 데이터를 가져와서 평균과 비교하는 그래프를 생성
    records = db.get_bmr_records(10) # 데이터베이스(db)에서 최근 10개의 BMR 데이터를 가져오고 records는 BMR 관련 데이터를 담고 있는 리스트
    
    ages = np.array([10, 20, 30, 40, 50, 60])
    avg_bmr = np.array([1500, 1600, 1550, 1500, 1450, 1400]) if gender == '남성' else np.array([1350, 1450, 1400, 1350, 1300, 1250])
    # avg_bmr 배열에는 각 연령대의 평균 BMR 값이 저장
    user_bmr = np.zeros(len(ages)) # 각 나이대의 사용자 평균 BMR 값을 저장할 배열.
    count = np.zeros(len(ages)) # [0, 0, 0, 0, 0, 0]으로 저장 , .zero() : 0으로 초기화하여 저장
    
    
    for record in records:
        age = int(record['age'])
        bmr = float(record['expectation_bmr'])
        record_gender = record['gender']
        if record_gender == gender:
            age_group = np.searchsorted(ages, age, side='right') -1  # argmin():최소값의 인덱스를 반환,사용자 나이랑 ages의 차이를 가장 작은 그룹 찾기 
            user_bmr[age_group] += bmr # 해당 연령대의 user_bmr 증가
            count[age_group] += 1 # 해당 연령대의 사용자 수 증가
    
    user_bmr = np.divide(user_bmr, count, out=np.zeros_like(user_bmr), where=count!=0) 
    # 나이대별로 누적된 user_bmr 값을 count로 나누어 평균을 계산.
    # where=count!=0을 사용하여 해당 연령대에 사용자가 없을 경우 0으로 유지
    # user_bmr / count 수행.
    # count != 0인 경우에만 나눗셈을 수행하고, count == 0이면 0을 유지.
    # out=np.zeros_like(user_bmr): 결과를 0으로 초기화된 같은 크기의 배열에 저장, ZeroDivisionError 방지
# ex) user_bmr = np.divide([0, 4800, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0], out=[0, 0, 0, 0, 0, 0], where=[False, True, False, False, False, False])

    
    # 한국어 폰트 설정 한글 꺠짐 방지
    # rc 함수로 글꼴 설정
    plt.rc('font', family='Malgun Gothic')  

    
    fig, ax = plt.subplots(figsize=(6,6))
    bar_width = 0.4 
    x_indexes = np.arange(len(ages)) # 0~5출력, X축에서 막대의 중심 위치를 나타내는 배열


    
    # 평균 막대 :
    # ax.bar() : 막대 그래프(바 차트)를 그리는 함수
    ax.bar(x_indexes - bar_width/2, avg_bmr, width=bar_width, color='gray', alpha=0.5, label='평균 BMR')
    # x_indexes - bar_width/2: X축에서 평균 BMR 막대의 위치를 왼쪽 배치
    # avg_bmr: 각 나이대의 평균 BMR 값을 Y축 값으로 설정
    # alpha : 투명도

    # 사용자 막대 :
    ax.bar(x_indexes + bar_width/2, user_bmr, width=bar_width, color='blue' 
           if gender == '남성' else 'red', alpha=0.7, label='사용자 BMR')
    # 오른쪽으로 배치, user_bmr : y축 값으로 설정, 
    
    ax.set_xlabel('연령', labelpad=10)
    ax.set_ylabel('BMR (kcal/day)', labelpad=10)
    ax.set_title(f'{gender} 평균 vs 사용자 BMR', pad=15)
    ax.set_xticks(ticks=x_indexes)
    ax.set_xticklabels(ages)
    ax.legend(loc='upper right', fontsize=10)
    # .legend() 범례 추가하는 함수
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # y축 방향으로 점선을 그리기
    img = io.BytesIO()
    # 그래프를 BytesIO 객체로 저장하여 메모리에서 바로 이미지로 변환
    
    # savefig : 그래프를 이미지 파일로 저장
    plt.savefig(img, format='png', bbox_inches='tight')
    # bbox_inches='tight' : 공백을 최소화
    img.seek(0)

    return Response(img.getvalue(), mimetype='image/png')
    # Flask의 Response 객체를 사용해 이미지를 image/png 형식으로 HTTP 응답으로 반환
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)