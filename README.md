# BMR 기초대사량 계산기

<p align="center">
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=mariadb&logoColor=white" />
  <img src="https://img.shields.io/badge/matplotlib-11557c?style=for-the-badge&logo=matplotlib&logoColor=white" />
  <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/jquery-0769AD?style=for-the-badge&logo=jquery&logoColor=white" />
</p>

## 프로젝트 기간
기간 : 25/03/11~25/03/12

## 프로젝트 개요
이 프로젝트는 사용자가 입력한 개인 정보를 기반으로 기초대사량을 계산하고, 데이터베이스에 저장하며, 저장된 데이터를 통해 연령대별 평균 BMR과 사용자의 BMR을 비교 시각화하는 웹 애플리케이션입니다.

## 시연영상

[BMR Calculator 시연 영상](https://www.youtube.com/watch?v=06BQE0mELiY)


## 주요 기능

- **BMR 계산**: 성별, 나이, 키, 체중 및 생활습관에 따른 기초대사량 계산
- **데이터 시각화**: 연령대별 평균 BMR과 사용자 BMR 비교 그래프 제공
- **기록 관리**: 사용자의 BMR 계산 기록 저장 및 조회
- **페이징 처리**: 대량의 기록 데이터 효율적인 탐색 기능
- **검색 기능**: 저장된 BMR 기록 데이터 검색 기능

## 기술 스택

| 영역 | 기술 |
|------|------|
| 백엔드 | Flask, Python |
| 프론트엔드 | HTML, CSS, JavaScript |
| 데이터베이스 | MariaDB/MySQL |
| 데이터 시각화 | Matplotlib, NumPy |

## 시스템 아키텍처

```
├── app.py                  # 메인 애플리케이션 파일
├── bmr.py                  # BMR 계산 로직
├── db.py                   # 데이터베이스 관리
├── static/
│   └── style.css           # CSS 스타일링
├── templates/
│   ├── team02_index.html   # 입력 폼 페이지
│   ├── team02_result.html  # 결과 표시 페이지
│   └── team02_history.html # 기록 및 시각화 페이지
└── README.md               # 프로젝트 설명서
```

## BMR 계산 방식

BMR(Basal Metabolic Rate, 기초대사량)은 다음 공식을 사용하여 계산됩니다:

- **남성**:
  ```
  BMR = 447.6 + (9.2 × 체중(kg)) + (3.1 × 키(m)) - (4.3 × 나이(세))
  ```

- **여성**:
  ```
  BMR = 88.36 + (13.4 × 체중(kg)) + (4.8 × 키(m)) - (5.7 × 나이(세))
  ```

생활습관에 따른 활동 계수:
- 좌식(운동을 거의 또는 전혀 하지 않음): 1.2
- 가벼운 활동(가벼운 운동/스포츠 1-3일/주): 1.375
- 적당히 활동적(중간 정도의 운동/스포츠 3-5일/주): 1.55
- 매우 활동적인(일주일에 6-7일 격렬한 운동/스포츠): 1.725
- 매우 활동적인 경우(매우 힘든 운동/스포츠 및 육체노동): 1.9

## 역할 분담

| 이름 | 역할 |
|------|------|
| 권순규 | 팀장 ,프로젝트 총괄 |
| 석송이 | 데이터 정렬화, 페이징처리, 검색기능 |
| 송지연 | 계산기 로직 구현, 차트 |

<artifacts>
<artifact id="profile-cards" type="text/markdown">
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/SK-Kwon90">
        <img src="https://github.com/SK-Kwon90.png" width="100px;" alt="권순규 프로필"/>
        <br />
        <sub><b>권순규</b></sub>
      </a>
      <br />
    </td>
    <td align="center">
      <a href="https://github.com/songyiseok">
        <img src="https://github.com/songyiseok.png" width="100px;" alt="석송이 프로필"/>
        <br />
        <sub><b>석송이</b></sub>
      </a>
      <br />
    </td>
    <td align="center">
      <a href="https://github.com/ssuuoo12">
        <img src="https://github.com/ssuuoo12.png" width="100px;" alt="송지연 프로필"/>
        <br />
        <sub><b>송지연</b></sub>
      </a>
      <br />
    </td>
  </tr>
</table>
</artifact>
</artifacts>

## 설치 방법

### 사전 요구사항
- Python 3.10.6
- MariaDB

### 설치 과정

1. 저장소 복제:
   ```bash
   git clone https://github.com/songyiseok/BMR_Calculator.git
   cd BMR_Calculator
   ```
2. 필요한 패키지 설치:
   ```bash
   pip install flask pymysql matplotlib numpy pandas
   ```

3. 데이터베이스 설정:
   - MariaDB/MySQL에 `test` 데이터베이스 생성
   - `bmr_records 테이블.sql` 스크립트 실행
   - (필요시) `db.py` 파일에서 데이터베이스 연결 정보 업데이트

4. 애플리케이션 실행:
   ```bash
   python app.py
   ```

5. 웹 브라우저에서 접속:
   ```
   http://localhost:5050
   ```
