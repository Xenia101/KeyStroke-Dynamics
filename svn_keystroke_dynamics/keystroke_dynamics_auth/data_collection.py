"""
키스트로크 데이터 수집을 위한 유틸리티 함수
"""

import time

import numpy as np


def collect_keystroke_data(phrase, simulated=True):
    """
    키스트로크 데이터 수집 함수
    실제 환경에서는 키보드 이벤트 리스너로 대체해야 함

    Args:
        phrase (str): 입력할 문장 또는 패스워드
        simulated (bool): 시뮬레이션 모드 활성화 여부

    Returns:
        list: 키스트로크 데이터 (키, 누름 시각, 뗌 시각 정보)
    """
    if simulated:
        # 시뮬레이션된 키스트로크 데이터
        keystroke_data = []
        base_time = time.time()

        for i, char in enumerate(phrase):
            # 랜덤한 타이핑 패턴 생성 (실제로는 실제 사용자 타이핑 데이터 수집 필요)
            press_time = base_time + i * (0.1 + np.random.normal(0, 0.02))
            release_time = press_time + np.random.normal(0.08, 0.01)  # 평균 80ms의 키 누름 시간

            keystroke_data.append({"key": char, "press_time": press_time, "release_time": release_time})

        return keystroke_data
    else:
        # 여기서는 실제 데이터 수집 로직 구현 필요
        raise NotImplementedError("실제 키스트로크 수집 기능은 아직 구현되지 않았습니다.")


def generate_impostor_data(phrase, variation_factor=0.05):
    """
    비정상 사용자 데이터 생성 함수

    Args:
        phrase (str): 입력할 문장 또는 패스워드
        variation_factor (float): 변형 정도 (높을수록 차이가 큼)

    Returns:
        list: 비정상 사용자의 키스트로크 데이터
    """
    # 비정상 사용자는 타이핑 패턴이 다름 (더 빠르거나 느리게 타이핑)
    data = collect_keystroke_data(phrase)

    # 타이핑 패턴 변형
    for i in range(len(data)):
        # 키 누름 시간 변형
        data[i]["press_time"] += np.random.normal(variation_factor, variation_factor * 0.6)
        data[i]["release_time"] += np.random.normal(variation_factor, variation_factor * 0.6)

    return data
