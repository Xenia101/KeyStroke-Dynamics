"""
키스트로크 다이내믹스 인증 시스템의 핵심 클래스
"""

import os
import pickle

import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


class KeystrokeDynamicsAuth:
    def __init__(self):
        self.model = svm.SVC(kernel="rbf", probability=True)
        self.user_profiles = {}

    def extract_features(self, keystroke_data):
        """
        키스트로크 데이터에서 특징 추출
        - 키 간 시간 간격 (flight time)
        - 키 누름 시간 (dwell time)
        """
        features = []

        for i in range(1, len(keystroke_data)):
            # 키 간 시간 간격 (현재 키 누름 시각 - 이전 키 누름 시각)
            flight_time = keystroke_data[i]["press_time"] - keystroke_data[i - 1]["press_time"]

            # 키 누름 시간 (키 뗌 시각 - 키 누름 시각)
            dwell_time = keystroke_data[i - 1]["release_time"] - keystroke_data[i - 1]["press_time"]

            features.extend([flight_time, dwell_time])

        # 마지막 키의 누름 시간 추가
        last_dwell = keystroke_data[-1]["release_time"] - keystroke_data[-1]["press_time"]
        features.append(last_dwell)

        return features

    def train(self, user_data, non_user_data, user_id):
        """사용자와 비사용자 데이터로 SVM 모델 학습"""
        X = []
        y = []

        # 사용자 데이터에 레이블 1 할당
        for data in user_data:
            features = self.extract_features(data)
            X.append(features)
            y.append(1)  # 정상 사용자

        # 비사용자 데이터에 레이블 0 할당
        for data in non_user_data:
            features = self.extract_features(data)
            X.append(features)
            y.append(0)  # 비정상 사용자

        # 학습/테스트 데이터 분할
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # 모델 학습
        self.model.fit(X_train, y_train)

        # 테스트 세트에서 성능 평가
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        # 사용자 프로필 저장
        self.user_profiles[user_id] = {"model": self.model, "accuracy": accuracy, "report": report}

        return accuracy, report

    def authenticate(self, keystroke_data, user_id, threshold=0.7):
        """
        사용자 인증 수행
        threshold: 인증 임계값 (0~1 사이)
        """
        if user_id not in self.user_profiles:
            return False, 0

        features = self.extract_features(keystroke_data)
        model = self.user_profiles[user_id]["model"]

        # 사용자일 확률 계산
        prob = model.predict_proba([features])[0][1]

        return prob >= threshold, prob

    def save_model(self, user_id, filepath):
        """사용자 모델 저장"""
        if user_id in self.user_profiles:
            with open(filepath, "wb") as f:
                pickle.dump(self.user_profiles[user_id], f)
            return True
        return False

    def load_model(self, user_id, filepath):
        """사용자 모델 로드"""
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.user_profiles[user_id] = pickle.load(f)
            return True
        return False
