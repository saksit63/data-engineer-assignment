"""
หลักการทำงาน คือ เมื่อรันไฟล์ python โดยใช้คำสั่ง 'python main.py'
มันจะค้นหาไฟล์ config.json ที่กำหนด source และ target ของไฟล์ 
หากหาไม่เจอจะดูที่ command ตอนเรารันไฟล์ 
คือ 'python main.py <source_file> <target_file>'
ถ้าไม่ได้กำหนดก็จะยกเลิกการรันไฟล์ python นี้
"""


import sys
import json


# Class สำหรับ input/output ไฟล์ หรือจัดการไฟล์
class FileReadWrite:

    def __init__(self):
        self.source = None
        self.target = None

    def read_file(self, file_name):
        self.source = file_name
        with open(self.source, 'r', encoding='utf-8') as file:
            return str(file.read())

    def write_file(self, text, file_name):
        self.target = file_name
        with open(self.target, 'w', encoding='utf-8') as file:
            file.write(text)


# Class สรำหรับแปลงข้อความจากไฟล์
class TextTransform:
    
    def transform(self, text):
        transform_text = text.lower().replace('\t', '____').replace('    ', '____')
        return transform_text


# Class สำหรับคำนวณค่าต่างๆ
class TextStatistics:

    def count_alphabets(self, text):
        result = {}
        for value in text:
            if value.isalpha():
                if value in result.keys():
                    result[value] = result[value] + 1 
                else:
                    result[value] = 1
        return result
    
    def total_alphabets(self, text): #นับตัวอักษรทั้งหมด
        result = []
        for value in text:
            if value.isalpha():
                result.append(value)
        return len(result)
    

# Class สำหรับกำหนดว่าจะรันแบบ CLI หรือใช้ไฟล์สำรหับกำหนด source และ target
class Config:

    def __init__(self):
        self.source = None
        self.target = None

    def cli_argument(self): #ฟังก์ชันกำหนด config ใน cli
        if len(sys.argv) != 3:
            print('ให้ใช้คำสั่งนี้: python <python_file> <source_file> <target_file>')
            exit(1) # ออกจากโปรแกรมทันทีเนื่องจากมีข้อผิดพลาด
        self.source = sys.argv[1]
        self.target = sys.argv[2]

    def json_argument(self, config_file): #ตัวอย่างการเพิ่ม config ใน json
        with open(config_file, 'r') as file:
            config = json.load(file)
            self.source = config['source']
            self.target = config['target']


# class สำหรับการทำงานทั้งหมด
class App:
    
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def run(self): #ฟังก์ชันในการรันทั้งหมด
        
        #อ่านไฟล์
        file = FileReadWrite()
        input_text = file.read_file(self.source)

        #แปลงข้อความ
        trans = TextTransform()
        transformed_text = trans.transform(input_text)

        #นับจำนวนตัวอักษรแต่ละตัว และนับตัวอักษรทั้งหมด
        statatic = TextStatistics()
        count_alphabet = statatic.count_alphabets(transformed_text)
        total_alphabet = statatic.total_alphabets(transformed_text)


        #แสดงข้อความที่แปลงและจำนวนตัวอักษรแต่ละตัว
        text = 'Sanitized Text :\n' + transformed_text\
            + '\n\nCount Text :\n' + '\n'.join([f'{key} : {val}' for key, val in count_alphabet.items()])\
            + '\n\nTotal Text : ' + str(total_alphabet) + '\n'
        print(text)
        
        #เขียนไฟล์
        file.write_file(text, self.target)

def main():
    config = Config()
    config_json_file = 'config.json'
    try: #ลองหาไฟล์ที่ชื่อ config.json
        config.json_argument(config_json_file)
    except FileNotFoundError: #หากเกิดเออเร่อหาไฟล์ไม่เจอ
        config.cli_argument()

    #รัน App
    app = App(config.source, config.target)
    app.run()


if __name__ == '__main__':
    main()
