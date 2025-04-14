"""
키스트로크 다이내믹스 인증 시스템 CLI
"""

import argparse
import os
import sys
import time

from .auth import KeystrokeDynamicsAuth
from .data_collection import collect_keystroke_data, generate_impostor_data


def get_args():
    """
    명령행 인수 파싱
    """
    parser = argparse.ArgumentParser(description="키스트로크 다이내믹스 인증 시스템")

    subparsers = parser.add_subparsers(dest="command", help="명령")

    # 학습 명령
    train_parser = subparsers.add_parser("train", help="사용자 타이핑 패턴 학습")
    train_parser.add_argument("--user-id", "-u", required=True, help="사용자 ID")
    train_parser.add_argument("--phrase", "-p", required=True, help="학습에 사용할 패스프레이즈")
    train_parser.add_argument("--samples", "-s", type=int, default=20, help="학습 샘플 수")
    train_parser.add_argument("--output", "-o", help="모델 저장 경로")

    # 인증 명령
    auth_parser = subparsers.add_parser("authenticate", help="사용자 인증")
    auth_parser.add_argument("--user-id", "-u", required=True, help="사용자 ID")
    auth_parser.add_argument("--phrase", "-p", required=True, help="인증에 사용할 패스프레이즈")
    auth_parser.add_argument("--model", "-m", required=True, help="모델 파일 경로")
    auth_parser.add_argument("--threshold", "-t", type=float, default=0.7, help="인증 임계값 (0~1)")

    return parser.parse_args()


def train_command(args):
    """
    학습 명령 처리
    """
    print(f"사용자 '{args.user_id}'에 대한 타이핑 패턴 학습을 시작합니다...")
    print(f"패스프레이즈: '{args.phrase}'")
    print(f"학습 샘플 수: {args.samples}")

    # 인증 시스템 초기화
    auth_system = KeystrokeDynamicsAuth()

    # 정상 사용자 데이터 시뮬레이션
    print("정상 사용자 데이터 생성 중...")
    user_data = [collect_keystroke_data(args.phrase) for _ in range(args.samples)]

    # 비정상 사용자 데이터 시뮬레이션
    print("비정상 사용자 데이터 생성 중...")
    non_user_data = [generate_impostor_data(args.phrase) for _ in range(args.samples)]

    # 모델 학습
    print("모델 학습 중...")
    accuracy, report = auth_system.train(user_data, non_user_data, args.user_id)

    print(f"\n모델 정확도: {accuracy:.4f}")
    print("\n분류 보고서:")
    print(report)

    # 모델 저장
    if args.output:
        output_path = args.output
    else:
        # 기본 저장 경로
        os.makedirs("models", exist_ok=True)
        output_path = f"models/{args.user_id}_model.pkl"

    auth_system.save_model(args.user_id, output_path)
    print(f"\n모델 저장 완료: {output_path}")

    return 0


def authenticate_command(args):
    """
    인증 명령 처리
    """
    print(f"사용자 '{args.user_id}' 인증을 시작합니다...")

    # 인증 시스템 초기화
    auth_system = KeystrokeDynamicsAuth()

    # 모델 로드
    if not auth_system.load_model(args.user_id, args.model):
        print(f"오류: 모델 파일 '{args.model}'을 로드할 수 없습니다.")
        return 1

    print(f"모델 로드 완료: {args.model}")
    print(f"패스프레이즈를 입력하세요: '{args.phrase}'")

    # 키스트로크 데이터 수집 (실제로는 사용자 입력 받기)
    keystroke_data = collect_keystroke_data(args.phrase)

    # 인증 수행
    is_authentic, confidence = auth_system.authenticate(keystroke_data, args.user_id, threshold=args.threshold)

    print("\n인증 결과:")
    print(f"인증 {'성공' if is_authentic else '실패'}")
    print(f"신뢰도: {confidence:.4f} (임계값: {args.threshold})")

    return 0 if is_authentic else 1


def main():
    """
    메인 함수
    """
    args = get_args()

    if args.command == "train":
        return train_command(args)
    elif args.command == "authenticate":
        return authenticate_command(args)
    else:
        print("명령을 지정해주세요. 'train' 또는 'authenticate'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
