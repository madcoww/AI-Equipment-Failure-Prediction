"""03-02 실습: sensor anomaly shapes, operating context, and event history."""

from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parent
DATA = BASE / "03-02_센서_고장_판별_이상구간샘플.csv"
EVENTS = BASE / "03-02_센서_고장_판별_정비알람이력.csv"

df = pd.read_csv(DATA, parse_dates=["timestamp"])
events = pd.read_csv(EVENTS, parse_dates=["event_time"])
print("shape:", df.shape)
print(df.isna().sum())
print(events.to_string(index=False))

# TODO 1: MTR02 / HYD02 / FUR02 케이스 중 하나를 골라 물리량과 단위를 정리하세요.
# TODO 2: 결측 구간, 가동 중 최장 동일값 반복, 최대값 반복 횟수, 구간별 변동 폭을 계산하세요.
# TODO 3: 같은 물리량 센서끼리 비교하고 알람·정비 이력과 시각을 대조하세요.
# TODO 4: 각 이상을 설비 현상 / 센서 이상 / 판단 보류로 나누고 근거·추가 자료·처리 방침을 작성하세요.

