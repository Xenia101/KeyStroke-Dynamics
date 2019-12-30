# User Verification based on Keystroke Dynamics 
<p align="center">
  <a href="http://nichijou.kr:5073/"><img src="https://github.com/Xenia101/KeyStroke-Dynamics/blob/master/img/logo2.png?raw=true"></a>
</p>

사용자 인증 시 개인마다의 고유한 키보드 입력 패턴을 분석하여 사용자에 대한 인증을 수행하는 서비스입니다.

### Key-Stroke Dynamics 란?
> Keystroke dynamics, keystroke biometrics, typing dynamics and lately typing biometrics, is the detailed timing information which describes exactly when each key was pressed and when it was released as a person is typing at a computer keyboard.
[WIKIPEDIA](https://en.wikipedia.org/wiki/Keystroke_dynamics)

## 설치 방법
해당 프로젝트는 웹 기반으로 동작합니다.
- Python Flask
- k-NN Based

## 동작 방식

Key-Stroke Dynamics 기반 사용자 인증 방식과 기존 Legacy와의 비교 동작 방식입니다.

<p align="center">
  <img src="https://github.com/Xenia101/Key-Stroke-Dynamics/blob/master/img/frame.png?raw=true">
</p>

## 검증 결과
- **k-NN 기반 사용자 식별 및 최적의 운영 파라미터 설정**

  - Euclidean distance 방식의 거리측정

  - 정확한 데이터분석을 위해 Cross-Validation 이용
  
  - 다수의 최적화 시험을 통해 k=3에서의 majority 기반 사용자 식별 진행

  <p align="center">
    <img src="https://github.com/Xenia101/KeyStroke-Dynamics/blob/master/img/cross-validation.png?raw=true">
    <img src="https://github.com/Xenia101/KeyStroke-Dynamics/blob/master/img/graph.png?raw=true">
  </p>
  
  > ↑ 해당 모델의 Cross-Validation 동작 프레임과 결과 그래프 예시
  >
  > k값이 3일 경우 오류가 가장 적게 발생한다는 것을 알 수 있다. 
  >
  > 따라서 이 모델에 적합한 k값을 구할 수 있다.

- **5-Cross Validation 기반 분석결과**

  97.6%, 92.2%, 97.1%, 100%, 97.1% 으로 평균 Accuracy **96.8%** 결과 산출


## 대용량 데이터 운영방안 (Fast kNN)

- <strong>Hash bit 길이</strong>

  > Google은 80억 개의 웹 페이지의 경우 Simhash 64 bit면 충분하다고 함

  Google의 논문은 전체 웹 페이지를 64 비트 지문으로 매핑하는 f = 64 사용해 k값(Hamming distance) 검증 실험 진행

- <strong>Hamming distance</strong>

  - Google은 k=1~10까지 변화시켜 실험 진행
  
  - K값이 매우 낮으면 거의 중복되는 것이 없고, 매우 높은 값은 잘못된 웹페이지를 중복으로 지정함
  
  - Precision(정밀도)과 Recall이 0.75에 가까운 k=3을 선택하는 것이 타당함

<p align="center">
  <img width="400" src="https://github.com/Xenia101/Key-Stroke-Dynamics/blob/master/img/hamming_distance_graph.png?raw=true">
</p>

  **64비트의 Simhash의 경우 3비트 이내로 다를 때 두개의 웹 페이지를 거의 중복으로 판단하면 높은 정확도 도출 가능**

- <strong>Simhash 고속분석(permutation and prefix matching)</strong>

  - 4bit Simhash, hamming distance 4 이하 검색 시
  
  - Simhash를 5개 영역으로 구분(13, 13, 13, 13, 12 bit)
  
  - hamming distance 4이하면, 5개 block 중 최소한 1개는 일치해야 함
  
  - 1개 block이 일치할 경우, 전수검색하여 분석

  |  |  <center>a</center> |  <center>b</center> |  <center>c</center> | <center>d</center> | <center>e</center> |
  |:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|
  |**d1** | <center>0100101010001</center> | <center>1101001010010</center> | <center>0100101100111</center> | <center>0100010101001</center> | <center>010010110010</center> |


- <strong>Example</strong>

  - 100억개 data, 64bit Simhash, hamming distacne 4일때

  - 5개 block 중 가장 작은것은 12bit로 구성되며, 4,096개 값 존재 
    * 즉, 100억개 data는 4,096개 값 중 하나로 매핑됨(1개값에는 약 24,414개 data 존재))
    
  - 총 5개 block이므로, 최대 12만여개로 100억 대비 0.0012% 비교로 분석가능

## 사용 방법 [http://nichijou.kr:5073](http://nichijou.kr:5073/)
### 회원가입 

1. ID/Password가 존재하는지 확인

<p align="center">
  <img src="https://github.com/Xenia101/Key-Stroke-Dynamics/blob/master/img/sign%20up/1.PNG?raw=true">
</p>

2. ID/Password 30번씩 입력

<p align="center">
  <img src="https://github.com/Xenia101/Key-Stroke-Dynamics/blob/master/img/sign%20up/2.PNG?raw=true">
</p>

### 로그인

1. 로그인 시도

<p align="center">
  <img src="https://github.com/Xenia101/Key-Stroke-Dynamics/blob/master/img/sign%20in/2.PNG?raw=true">
</p>

