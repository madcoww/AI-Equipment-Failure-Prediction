"""01-02 실습: 제선 운전 데이터에서 변화 구간을 찾아 판정하세요."""

from pathlib import Path

import pandas as pd # pyright: ignore[reportMissingModuleSource]


DATA = Path(__file__).resolve().parent / "01-02_제선_12시간_실습데이터.csv"
df = pd.read_csv(DATA, parse_dates=["timestamp"])

print("행/열:", df.shape)
print(df.describe().round(2))

# TODO 1: 송풍량과 송풍압의 30분 이동평균을 추가해 변화 구간을 찾아보세요.
# TODO 2: 노정압의 30분 이동 표준편차를 계산하고 흔들림이 커진 시각을 찾으세요.
# TODO 3: 송풍기 진동이 같은 구간에서 어떻게 변했는지 확인하세요.
# TODO 4: 시작 시각, 변화 방향, 진동 근거를 포함해 판정문을 작성하세요.
# TODO 5: 신호 -> 현상 -> 원인 후보 -> 확인 자료 순서로 추적 경로를 작성하세요.



# [준비] timestamp를 인덱스로 설정하세요.
#   → df.set_index("timestamp"), 이후 df.index가 DatetimeIndex인지 확인

# TODO 1: 송풍량(blast_flow_nm3min)과 송풍압(blast_pressure_kpa)의
#         30분 이동평균 컬럼 flow_ma30, press_ma30을 추가하세요.
#   1-1. rolling("30min").mean() 사용
#   1-2. 1시간 간격(00:00, 01:00, ...)의 이동평균 값을 출력하세요.
#   1-3. 이동평균이 가장 크게 바뀌기 시작한 시각을 한 개 적으세요.
#        (힌트: flow_ma30.diff()의 절댓값이 큰 시각, 또는 그래프)

# TODO 2: 노정압(top_pressure_kpa)의 30분 이동 표준편차 컬럼 top_std30을 추가하세요.
#   2-1. rolling("30min").std() 사용  ← 괄호 () 주의
#   2-2. top_std30이 가장 큰 시각과 그 값을 출력하세요. (idxmax(), max())
#   2-3. TODO 1의 시각과 비교해 같은 시간대인지 적으세요.

# TODO 3: TODO 1에서 찾은 시각을 기준으로, 그 전 1시간과 후 1시간의
#         송풍기 진동(blower_vib_mms) 평균을 구하세요.
#   3-1. df.loc["시작":"끝"]으로 두 구간을 잘라 before, after에 저장
#   3-2. 두 평균과 차이(after - before)를 소수 둘째 자리까지 출력
#   3-3. 진동이 "증가 / 감소 / 거의 변화 없음" 중 무엇인지 적으세요.

# TODO 4: 아래 빈칸을 채워 판정문을 작성하세요.
#   "( 시각 )부터 송풍량은 ( 증가/감소 ), 송풍압은 ( 증가/감소 )했고,
#    노정압 흔들림은 ( 시각 )에 최대였다.
#    같은 구간 송풍기 진동은 ( before )→( after ) mm/s로 ( 증가/감소/유지 )했다."

# TODO 5: 아래 4칸을 채워 추적 경로를 작성하세요.
#   신호      : 어떤 컬럼의 어떤 수치가 변했나
#   현상      : 설비에서 무슨 일이 일어난 것으로 보이나
#   원인 후보 : 2개 이상 (단정 금지, "~가능성")
#   확인 자료 : 원인을 확인하려면 추가로 볼 데이터·기록



cols = [
    # 측정 시각 (시간 순서 기준, datetime으로 변환해서 사용)
    'timestamp',
    # 송풍량: 고로에 불어 넣는 바람의 양 (단위: Nm³/min, 표준상태 기준 분당 부피)
    'blast_flow_nm3min',
    # 송풍 압력: 고로로 보내는 바람의 압력 (단위: kPa)
    'blast_pressure_kpa',
    # 노정 압력: 고로 꼭대기(노정)의 가스 압력 (단위: kPa)
    'top_pressure_kpa',
    # 송풍기 진동: 송풍기(블로워)의 진동 크기 (단위: mm/s, 진동 속도)
    'blower_vib_mms',
    # 열풍 온도: 열풍로에서 데워 고로로 보내는 바람의 온도 (단위: °C)
    'hot_blast_temp_c'