import cv2

# 360도 비디오 로딩
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    
    # 비디오 재생 확인
    if not ret:
        break
    
    # 360도 비디오 표시
    cv2.namedWindow("360 Video", cv2.WINDOW_NORMAL)
    cv2.imshow("360 Video", frame)
    
    # q를 누르면 비디오 재생 중지
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows()