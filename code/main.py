import data_reader as dr

if __name__ == '__main__':
    # 필요한 모듈 불러오기
    reader = dr.DataReader()

    # csv 파일 설정하고 읽어오기
    reader.read_csv_file('./reference/data_anotation.csv', 3)
    #reader.read_csv_file('./reference/data_anotation.csv', 420)
