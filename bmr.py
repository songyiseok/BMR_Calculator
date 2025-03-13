class BMRCalculator: # bmr.py
    def __init__(self, gender, age, height, weight, life_style):
        self.gender = gender
        self.age = age
        self.height = height / 100  # cm를 m로 변환
        self.weight = weight
        self.life_style = life_style
        self.expectation_bmr = self.calculate_bmr()

    def calculate_bmr(self):
        """
        기초대사량(BMR) 계산
        bmr = 447.6 + (9.2 * self.weight) + (3.1 * self.height) - (4.3 * self.age)
        bmr = 88.36 + (13.4 * self.weight) + (4.8 * self.height) - (5.7 * self.age)
        """
        # 생활습관을 활동 계수로 변환
        activity_multipliers = {
            "좌식(운동을 거의 또는 전혀 하지 않음)": 1.2,
            "가벼운 활동(가벼운 운동/스포츠 1-3일/주)": 1.375,
            "적당히 활동적(중간 정도의 운동/스포츠 3-5일/주)": 1.55,
            "매우 활동적인(일주일에 6-7일 격렬한 운동/스포츠)": 1.725,
            "매우 활동적인 경우(매우 힘든 운동/스포츠 및 육체노동)": 1.9
        }
        
        # 입력된 생활습관이 활동 계수 목록에 없으면 오류 발생
        if self.life_style not in activity_multipliers:
            raise ValueError("올바른 생활습관을 선택하세요")

        # 활동 계수 가져오기
        self.activity_multiplier = activity_multipliers[self.life_style]
        
        if self.gender == '남성':
            expectation_bmr = 447.6 + (9.2 * self.weight) + (3.1 * self.height) - (4.3 * self.age)
        elif self.gender == '여성':
            expectation_bmr = 88.36 + (13.4 * self.weight) + (4.8 * self.height) - (5.7 * self.age)
        else:
            raise ValueError("올바른 성별을 입력하세요")
        
        
        return round(expectation_bmr * self.activity_multiplier, 2)
    
    def get_result(self):
        return {
            "expectation_bmr": round(self.expectation_bmr, 1)
        }