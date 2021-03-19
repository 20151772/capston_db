import csv
import motion_data as md

class DataReader:
    def read_csv_file(self, file_name, last_number):
        # csv 파일 열기
        file = open(file_name, 'r')
        rdr = csv.reader(file)

        # 필요한 정의
        motion = md.MotionData()
        #dict = {}
        count = 0

        for line in rdr:
            if count == 0:
                count += 1
            elif count < last_number:
                #dict[line[6]] = line[5]
                #print(dict[line[6]])
                file_name = line[5].replace('MOV', 'avi')
                motion.get_holistic_data(file_name, line[6])

                count += 1
            else:
                break

        file.close()
