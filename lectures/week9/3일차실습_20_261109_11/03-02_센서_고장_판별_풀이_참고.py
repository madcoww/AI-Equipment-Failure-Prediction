"""03-02 실습8 풀이 참고용 (원본 실습 파일은 수정하지 않음).

실행: 이 파일이 있는 폴더에서 실행하거나, 아래 BASE 경로가 CSV 폴더를 가리키는지 확인.
"""

from pathlib import Path

import pandas as pd


# __file__을 사용하므로 .py 파일로 실행할 때만 동작한다 (주피터는 BASE를 직접 지정).
BASE = Path(__file__).resolve().parent
DATA = BASE / "03-02_센서_고장_판별_이상구간샘플.csv"
EVENTS = BASE / "03-02_센서_고장_판별_정비알람이력.csv"

df = pd.read_csv(DATA, parse_dates=["timestamp"]).set_index("timestamp")
events = pd.read_csv(EVENTS, parse_dates=["event_time"])

# ── TODO 1: 케이스 선택 (이 풀이는 케이스 A: 모터 계통, MTR02) ──
# MTR02_TEMP / MTR02_TEMP_B : 베어링 온도 두 센서 (℃)
# MTR02_VIB_H               : 진동 (단위는 자료에 없음 → 확인 필요)
# MTR02_CURRENT             : 모터 전류 (A 추정, 자료에 단위 없음)
# MTR02_RUN                 : 가동 상태 (1=운전, 0=정지)
run = df["MTR02_RUN"] == 1

# ── TODO 2: 구간별 계산 ──
# 결측 구간 (진동)
vib_nan = df.index[df["MTR02_VIB_H"].isna()]
print("[진동 결측] 개수:", len(vib_nan), "/ 구간:", vib_nan.min(), "~", vib_nan.max())

# 정지 구간 (MTR02_RUN == 0)
stop = df.index[~run]
print("[정지 구간]", stop.min(), "~", stop.max(), "/ 개수:", len(stop))

# 온도 차이 (MTR02_TEMP - MTR02_TEMP_B) : 시간에 따라 벌어지는지 확인
temp_gap = df["MTR02_TEMP"] - df["MTR02_TEMP_B"]
print("[온도차] 시작:", temp_gap.iloc[0], "/ 끝:", temp_gap.iloc[-1])

# ── TODO 3: 같은 물리량끼리 비교 + 이력 대조 ──
# 가동 중(run) 구간에서 압력 동일값이 가장 길게 이어진 구간 찾기
press = df["HYD02_PRESS"]
groups = (press != press.shift()).cumsum()
run_lengths = press.groupby(groups).size()
top_group = run_lengths.idxmax()
top_idx = press.index[groups == top_group]
print(
    "[HYD02_PRESS 최장 동일값] 값:", press.loc[top_idx[0]],
    "/ 개수:", len(top_idx),
    "/ 구간:", top_idx.min(), "~", top_idx.max(),
    "/ 가동 중 여부(run 전체 True?):", bool(run.loc[top_idx].all()),
)

# HYD02_PRESS_ACC 최대값 반복 횟수
acc = df["HYD02_PRESS_ACC"]
acc_max = acc.max()
acc_top = acc.index[acc == acc_max]
print("[HYD02_PRESS_ACC 최대값]", acc_max, "/ 개수:", len(acc_top),
      "/ 구간:", acc_top.min(), "~", acc_top.max())

# HYD02_FLOW 변동폭: 가동 중에만, 전반/후반 비교
flow_run = df.loc[run, "HYD02_FLOW"]
half = len(flow_run) // 2
print("[HYD02_FLOW 표준편차] 전반:", round(flow_run.iloc[:half].std(), 2),
      "/ 후반:", round(flow_run.iloc[half:].std(), 2))

# FUR02_TEMP_Z1 순간 상승 시점
fur = df["FUR02_TEMP_Z1"]
spike_idx = fur.index[fur > 1300]
print("[FUR02_TEMP_Z1 급등 시점]", list(spike_idx.strftime("%Y-%m-%d %H:%M")))

# 정비 이력과 시각 대조
print("\n[정비·알람 이력]")
print(events.to_string(index=False))

# ── TODO 4: 판정 초안 (최종 판단은 근거와 추가 자료를 함께 보고 결정) ──
# 아래는 데이터 모양 기준 1차 판정 초안이며, 확정 판정이 아니다.
draft = [
    ("MTR02_VIB_H 결측 18개", "센서 이상 후보 (통신장애)", "이력: 2026-04-02 06:00~09:00 통신장애 기록과 시각 일치"),
    ("MTR02_RUN 0 구간 18:00~20:50", "운전현상 (계획 정지)", "이력: 소재 교체 계획 정지와 시각 일치 → 정지 중 값 일정은 정상"),
    ("MTR02_TEMP vs TEMP_B 차이 증가", "판단 보류 (센서 드리프트 후보)", "이력: 2026-03-15 교정, 보정량 미기재 → 교정 기록 확인 필요"),
    ("HYD02_PRESS 36개 동일값", "판단 보류 (고착 후보)", "가동 중 동일값 지속 → 센서 고착인지 실제 압력 안정인지 확인 필요, 이력: 공급 압력 변동 없음 경고"),
    ("HYD02_PRESS_ACC 160 × 16개", "운전현상 가능성 (상한 도달)", "이력: 2026-04-02 12:00 어큐뮬레이터 압력 상한 도달과 시각 대응"),
    ("HYD02_FLOW 후반 흔들림 증가", "판단 보류 (노이즈 증가 후보)", "이력: 유량계 교체는 2026-02-20로 데이터 기간(4/1~4/2) 이전 → 이 이력만으로 원인 설명 불가, 교체 후 계측 점검 필요"),
    ("FUR02_TEMP_Z1 1450 순간 상승", "센서 이상 후보 (스파이크)", "3회 모두 1450 값 (08:20, 22:50, 14:50), 08:20은 전후 1195~1196℃로 복귀 → 1샘플 튐이면 스파이크 후보. 가열 이상이면 연속성이 있어야 함"),
]
print("\n[1차 판정 초안]")
for item, verdict, basis in draft:
    print(f"- {item} → {verdict}\n    근거: {basis}")
