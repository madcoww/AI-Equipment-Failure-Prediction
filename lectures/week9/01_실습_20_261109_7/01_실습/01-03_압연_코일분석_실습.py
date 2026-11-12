"""01-03 실습: 코일별 압연 추세를 요약하고 변화를 해석하세요."""

from pathlib import Path

import pandas as pd


DATA = Path(__file__).resolve().parent / "01-03_열연_코일별_실습데이터.csv"
df = pd.read_csv(DATA, parse_dates=["timestamp"])

print("행 수:", len(df), "/ 코일 수:", df["coil_id"].nunique())
print(df.head())

# TODO 1: rolling_force_ton, roll_gap_mm, exit_thickness_mm 컬럼을
#         설비·역할·단위에 연결하는 표를 작성하세요.

# TODO 2: 코일별 압연 하중 평균, 출측 두께 평균·표준편차를 집계하세요.
# TODO 3: 코일 순서에 따라 하중이 되돌아가는 지점과 두께 변동 구간을 찾으세요.
# TODO 4: 롤 갭(조작량), 출측 두께(제어 대상), 모터 전류(상태값)를 구분하세요.
# TODO 5: 값의 변화만으로 고장을 단정하지 말고 정비·AGC 이력을 확인하세요.




# C020 이후 하중 감소, C030 이후 두께 표준편차 증가는 이상 징후일 뿐 고장 확정이 아님.
# 나의가설 : 하중 은 마모패턴 인거같고, 급락의 이유는 장비교체로 보임.

# 확인할 것: 정비 이력, 롤 교체(roll_replaced), AGC 설정·작동 이력, 가열로 온도
