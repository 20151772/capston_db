import csv, os

class FileNameChanger:
    # 원래 KETI01 등 무슨 수화인지 알 수 없었던 영상 이름을 csv파일을 읽고, 원래 수화 뜻에 맞게 변경
    def readCsvFile(self, file_name, video_path, last_number):
        # csv 파일 열기
        file = open(file_name, 'r')
        rdr = csv.reader(file)

        # 필요한 정의
        count = 0
        dict = {}

        # csv 읽고, dict = {영상이름: 수화뜻} 을 구함
        for line in rdr:
            # 첫번째 줄 생략
            if count == 0:
                count += 1
            # 두번째 줄부터 지정된 줄까지
            elif count < last_number:
                dict[line[5].replace('MOV', 'avi')] = line[6]  # KETI01.MOV -> KETI01.avi : 0

                #dict[line[6]] = line[5]
                #print(dict[line[6]])

                #file_name = line[5].replace('MOV', 'avi')
                #motion.getHolisticData(file_name, line[6])

                count += 1
            else:
                break

        # 영상 폴더를 열고, 실제 영상의 이름을 위에서 구한 dict에 따라 변경
        video_names = os.listdir(video_path)
        for name in video_names:
            if name in dict:
                src = os.path.join(video_path, name)
                dst = dict[name] + '.avi'
                dst = os.path.join(video_path, dst)
                os.rename(src, dst)

        file.close()
