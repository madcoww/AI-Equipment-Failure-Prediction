"""Generate raw and reduced time-series samples for the Day 3 information-loss lab."""

from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path(__file__).resolve().parent


def pressure_samples():
    rng = np.random.default_rng(20261103)
    time = pd.date_range("2026-04-03 09:00:00", periods=600, freq="s")
    pressure = 150 + rng.normal(0, 0.15, len(time))
    pressure[273:276] = [176, 191, 170]
    raw = pd.DataFrame({"timestamp": time, "pressure_bar": pressure.round(2)})
    processed = raw.set_index("timestamp").resample("1min").mean().reset_index()
    return raw, processed


def temperature_samples():
    time = pd.date_range("2026-04-03 10:00:00", periods=180, freq="10s")
    seconds = np.arange(len(time)) * 10
    temp = 1180 + 0.1 * (seconds // 60) + 0.05 * np.sin(seconds / 90)
    temp[89:92] += [1.0, 2.0, 1.0]
    raw = pd.DataFrame({"timestamp": time, "furnace_temp_c": temp.round(2)})
    aggregate = raw.set_index("timestamp").resample("5min").mean().reset_index()
    deadband_rows = []
    last = None
    for row in aggregate.itertuples(index=False):
        value = row.furnace_temp_c
        if last is None or abs(value - last) >= 0.5:
            deadband_rows.append((row.timestamp, round(value, 1)))
            last = round(value, 1)
    reduced = pd.DataFrame(deadband_rows, columns=["timestamp", "furnace_temp_c"])
    return raw, aggregate, reduced


def main():
    pressure_raw, pressure_saved = pressure_samples()
    temp_raw, temp_aggregate, temp_deadband = temperature_samples()
    files = {
        "03-02_압력_고속원본.csv": pressure_raw,
        "03-02_압력_1분평균_가공본.csv": pressure_saved,
        "03-02_온도_10초원본.csv": temp_raw,
        "03-02_온도_5분집계_가공본.csv": temp_aggregate,
        "03-02_온도_데드밴드가공본.csv": temp_deadband,
        "03-02_데이터출처_메타데이터.csv": pd.DataFrame(
            [
                {
                    "tag": "PRESS01",
                    "원천계층": "PLC 고속 샘플",
                    "원래주기_sec": 1,
                    "저장주기_sec": 60,
                    "집계방식": "1분 산술평균",
                    "deadband": "없음",
                    "품질코드": "제공되지 않음",
                    "메모": "3초 서지 검출을 위해 고속 원본 또는 최소/최대값 요청",
                },
                {
                    "tag": "FUR01_TEMP",
                    "원천계층": "온도 입력 모듈",
                    "원래주기_sec": 10,
                    "저장주기_sec": 300,
                    "집계방식": "5분 산술평균",
                    "deadband": "별도 가공본은 0.5 degC 변화 시 저장",
                    "품질코드": "제공되지 않음",
                    "메모": "원시주기·집계법·데드밴드·강제저장 조건 확인",
                },
            ]
        ),
    }
    for name, frame in files.items():
        frame.to_csv(OUT / name, index=False, encoding="utf-8-sig")
    print("생성 완료:", ", ".join(f"{name} ({len(frame)}행)" for name, frame in files.items()))


if __name__ == "__main__":
    main()
