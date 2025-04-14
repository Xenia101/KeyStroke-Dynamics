"""
키스트로크 다이내믹스 인증 시스템 데모 예제
"""

import os
import sys

import matplotlib.pyplot as plt

# 모듈 경로 추가 (로컬 개발 환경용)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from keystroke_dynamics_auth.auth import KeystrokeDynamicsAuth
from keystroke_dynamics_auth.data_collection import (
    collect_keystroke_data,
    generate_impostor_data,
)
from keystroke_dynamics_auth.visualization import (
    plot_authentication_results,
    plot_keystroke_features,
)


def run_demo():
    """
    키스트로크 다이내믹스 인증 시스템 데모 실행
    """
    print("키스트로크 다이내믹스 인증 시스템 데모 시작")

    # 키스트로크 인증 시스템 초기화
    auth_system = KeystrokeDynamicsAuth()

    # 샘플 패스프레이즈
    passphrase = "my secure password"

    # 정상 사용자 데이터 시뮬레이션 (여러 번 타이핑)
    print("정상 사용자 데이터 생성 중...")
    user_data = [collect_keystroke_data(passphrase) for _ in range(20)]

    # 비정상 사용자 데이터 시뮬레이션 (다른 타이핑 패턴)
    print("비정상 사용자 데이터 생성 중...")
    non_user_data = [generate_impostor_data(passphrase) for _ in range(20)]

    # 모델 학습
    print("모델 학습 중...")
    user_id = "user123"
    accuracy, report = auth_system.train(user_data, non_user_data, user_id)

    print(f"모델 정확도: {accuracy:.4f}")
    print("분류 보고서:")
    print(report)

    # 인증 테스트를 위한 샘플 생성
    test_cases = []

    # 정상 사용자 테스트 케이스
    for i in range(5):
        test_cases.append((user_id, 1, collect_keystroke_data(passphrase)))  # 실제 레이블 (정상 사용자)

    # 비정상 사용자 테스트 케이스
    for i in range(5):
        test_cases.append((user_id, 0, generate_impostor_data(passphrase)))  # 실제 레이블 (비정상 사용자)

    # 인증 테스트 수행
    print("\n인증 테스트 수행 중...")
    results = []

    for tc in test_cases:
        user_id, actual_label, keystroke_data = tc
        is_authentic, confidence = auth_system.authenticate(keystroke_data, user_id)
        results.append((user_id, actual_label, confidence))
        print(
            f"테스트 {len(results):2d}: 실제={actual_label}, 인증={'성공' if is_authentic else '실패'} (신뢰도: {confidence:.4f})"
        )

    # 특징 시각화
    print("\n키스트로크 특징 시각화 중...")
    user_features = [auth_system.extract_features(data) for data in user_data[:5]]
    impostor_features = [auth_system.extract_features(data) for data in non_user_data[:5]]

    feature_fig = plot_keystroke_features(user_features, impostor_features)

    # 인증 결과 시각화
    print("인증 결과 시각화 중...")
    results_fig, results_df = plot_authentication_results(results)

    # 모델 저장 및 로드 테스트
    print("\n모델 저장 및 로드 테스트...")
    os.makedirs("models", exist_ok=True)
    model_path = "models/demo_model.pkl"
    auth_system.save_model(user_id, model_path)
    print(f"모델 저장 완료: {model_path}")

    new_auth_system = KeystrokeDynamicsAuth()
    if new_auth_system.load_model(user_id, model_path):
        print("모델 로드 성공")

        # 새 모델로 인증 테스트
        legitimate_test = collect_keystroke_data(passphrase)
        is_authentic, confidence = new_auth_system.authenticate(legitimate_test, user_id)
        print(f"모델 로드 후 인증: {'성공' if is_authentic else '실패'} (신뢰도: {confidence:.4f})")
    else:
        print("모델 로드 실패")

    # 그래프 표시
    plt.show()


if __name__ == "__main__":
    run_demo()
