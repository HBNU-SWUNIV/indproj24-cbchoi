## 1. Ricoh Theta V  설정
1. [Ricoh Theta V 드라이버 설치(Windows만)](https://topics.theta360.com/ko/faq/c_00_z1/304_1/)


## 2. 가상환경 설정
1. python 3.8 버전 설치 필요
   
2. python 가상환경 설정 (3.8) pytnon -m venv venv
   
3. 가상환경 실행
   1. 윈도우 : `venv\Scripts\activate`
   2. 리눅스, 맥 : `source venv/bin/activate`
   
4. 다음 명령어로 라이브러리 설치
```
pip3 install -r requirements.txt
```
## 3. 실행 환경 설정

1. config.py
```python

SIGNALING_SERVER_URL :str = "Server IP Address" --> IP주소
HOST :str = "Your IP ADDRESS" --> IP주소

```

2. 카메라 스트리밍 명령어
```
python offer.py
```