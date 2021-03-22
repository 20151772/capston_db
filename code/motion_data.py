import cv2, time, json
import mediapipe as mp
from PyQt5.QtWidgets import *

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

class MotionData:
    # 손(손가락) + 포즈 + 얼굴 트래킹
    def getHolisticData(self, file_path):
        # 캡쳐 횟수 조절
        prev_time = 0
        fps = 5
        count = 0

        # 파일 경로 설정
        file_name = file_path.split('/')[2]
        save_path = './motion_data_file/' + file_name.replace('.avi', '')
        print(save_path)

        # OpenCV로 읽고 json 파일 생성
        cap = cv2.VideoCapture(file_path)
        with open(save_path + '.json', 'w') as f:
            pass

        # 비디오의 너비, 높이
        width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 간단한 비디오 정보
        print("\n# Video Information")
        print("Sign Language Name: " + file_name)
        print("Video Path : " + file_path)
        print("Video Width: " + str(width))
        print("Video Height: " + str(height) + '\n')

        # 비디오 재생하는 동안 반복되는 부분
        with mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            upper_body_only=True) as holistic:
            while cap.isOpened():
                success, image = cap.read()

                if not success:
                    print("\nIgnoring empty camera frame")
                    break

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # 성능을 높이기 위해 API reference에서 요구하는 부분
                image.flags.writeable = False
                results = holistic.process(image)

                # 영상에 어노테이션을 그리는 부분
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                ''' 얼굴을 그리는 부분
                mp_drawing.draw_landmarks(
                    image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
                '''
                mp_drawing.draw_landmarks(
                    image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                mp_drawing.draw_landmarks(
                    image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_holistic.UPPER_BODY_POSE_CONNECTIONS)

                # 랜드마크의 x,y 값 출력
                current_time = time.time() - prev_time
                file_data = {}

                # 일정 시간(fps)마다 랜드마크 데이터가 하나라도 있을 때, 그 데이터를 가져와 저장
                if (results.pose_landmarks or results.left_hand_landmarks or results.right_hand_landmarks) and (current_time > 1./fps):
                    prev_time = time.time()
                    count += 1

                    # json 파일 비어있는지 확인
                    with open(save_path + '.json') as f:
                        isEmpty = f.read().strip()

                    # json 파일이 있는 경우 추가
                    with open(save_path + '.json') as json_file:
                        if isEmpty:
                            file_data = json.load(json_file)

                    file_data[str(count)] = []

                    # 포즈 데이터
                    pose_data = {}
                    pose_data['pose'] = []
                    if results.pose_landmarks:
                        pose_data['pose'].append({
                            'left_shoulder[0]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                            'left_shoulder[1]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
                            'left_elbow[0]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                            'left_elbow[1]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y,
                            'right_shoulder[0]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                            'right_shoulder[1]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
                            'right_elbow[0]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                            'right_elbow[1]':results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y
                        })
                        file_data[str(count)].append(pose_data)
                    else:
                        pose_data['pose'].append({
                            'left_shoulder[0]':0, 'left_shoulder[1]':0, 'left_elbow[0]':0, 'left_elbow[1]':0,
                            'right_shoulder[0]':0, 'right_shoulder[1]':0, 'right_elbow[0]':0, 'right_elbow[1]':0
                        })
                        file_data[str(count)].append(pose_data)

                    # 오른손 데이터
                    right_hand_data = {}
                    right_hand_data['right_hand'] = []
                    if results.right_hand_landmarks:
                        right_hand_data['right_hand'].append({
                            'wrist[0]': results.right_hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                            'wrist[1]': results.right_hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
                        })
                        file_data[str(count)].append(right_hand_data)
                    else:
                        right_hand_data['right_hand'].append({
                            'wrist[0]':0, 'wrist[1]':0
                        })
                        file_data[str(count)].append(right_hand_data)

                    # 왼손 데이터
                    left_hand_data = {}
                    left_hand_data['left_hand'] = []
                    if results.left_hand_landmarks:
                        left_hand_data['left_hand'].append({
                            'wrist[0]': results.left_hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,
                            'wrist[1]': results.left_hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,
                        })
                        file_data[str(count)].append(left_hand_data)
                    else:
                        left_hand_data['left_hand'].append({
                            'wrist[0]': 0, 'wrist[1]': 0
                        })
                        file_data[str(count)].append(left_hand_data)

                    # json 파일에 쓰기
                    with open(save_path + '.json', "w") as outfile:
                        json.dump(file_data, outfile, indent='\t')

                # 결과물 표시
                cv2.imshow('Holistic', image)

                # 종료 키 받는 부분
                if cv2.waitKey(5) & 0xFF == 27:
                    break

            cap.release()