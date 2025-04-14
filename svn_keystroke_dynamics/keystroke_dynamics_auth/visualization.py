"""
키스트로크 데이터 시각화 유틸리티
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_keystroke_features(user_data, impostor_data, feature_names=None):
    """
    사용자와 비정상 사용자의 키스트로크 특징을 시각화

    Args:
        user_data (list): 정상 사용자의 키스트로크 특징 데이터
        impostor_data (list): 비정상 사용자의 키스트로크 특징 데이터
        feature_names (list, optional): 특징 이름 목록
    """
    plt.figure(figsize=(12, 6))

    # 데이터 준비
    user_means = np.mean(user_data, axis=0)
    user_stds = np.std(user_data, axis=0)

    impostor_means = np.mean(impostor_data, axis=0)
    impostor_stds = np.std(impostor_data, axis=0)

    # 특징 이름이 없으면 기본 이름 생성
    if feature_names is None:
        feature_names = []
        for i in range(len(user_means) // 2):
            feature_names.extend([f"Flight_{i}", f"Dwell_{i}"])
        if len(user_means) % 2 == 1:
            feature_names.append(f"Dwell_{len(user_means) // 2}")

    # x축 위치
    x = np.arange(len(user_means))

    # 막대 그래프 그리기
    width = 0.35
    plt.bar(x - width / 2, user_means, width, label="정상 사용자", yerr=user_stds, alpha=0.7, capsize=10)
    plt.bar(x + width / 2, impostor_means, width, label="비정상 사용자", yerr=impostor_stds, alpha=0.7, capsize=10)

    # 그래프 꾸미기
    plt.xlabel("특징")
    plt.ylabel("값 (초)")
    plt.title("사용자와 비정상 사용자의 키스트로크 특징 비교")
    plt.xticks(x, feature_names, rotation=45)
    plt.legend()

    plt.tight_layout()
    return plt.gcf()


def plot_authentication_results(results, threshold=0.7):
    """
    인증 결과를 시각화

    Args:
        results (list): (사용자_ID, 실제_레이블, 예측_확률) 튜플 목록
        threshold (float): 인증 임계값
    """
    plt.figure(figsize=(10, 6))

    # 결과 준비
    user_ids = [r[0] for r in results]
    actual = [r[1] for r in results]
    probs = [r[2] for r in results]

    # 데이터프레임 생성
    df = pd.DataFrame(
        {
            "user_id": user_ids,
            "actual": actual,
            "probability": probs,
            "authenticated": [p >= threshold for p in probs],
            "correct": [actual[i] == (probs[i] >= threshold) for i in range(len(probs))],
        }
    )

    # 정렬
    df = df.sort_values("probability", ascending=False)

    # 그래프 그리기
    colors = ["green" if c else "red" for c in df["correct"]]
    markers = ["o" if a == 1 else "x" for a in df["actual"]]

    plt.scatter(range(len(df)), df["probability"], c=colors, marker="o", s=100, alpha=0.7)
    plt.axhline(y=threshold, color="r", linestyle="--", alpha=0.7, label=f"임계값 ({threshold})")

    # 그래프 꾸미기
    plt.xlabel("샘플")
    plt.ylabel("인증 확률")
    plt.title("키스트로크 다이내믹스 인증 결과")
    plt.grid(True, alpha=0.3)
    plt.ylim(-0.05, 1.05)

    # 범례 추가
    plt.legend(["인증 확률", "임계값"])

    plt.tight_layout()
    return plt.gcf(), df
