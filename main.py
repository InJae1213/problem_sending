import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

# 파일 경로를 현재 스크립트 파일의 위치 기준으로 설정
base_path = os.path.dirname(os.path.abspath(__file__))
indices_path = os.path.join(base_path, "indices.json")

# 현재 문제의 인덱스를 파일에서 로드하고 저장하는 함수들
def save_indices(indices):
    with open(indices_path, "w") as file:
        json.dump(indices, file)

def load_indices():
    try:
        with open(indices_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {0: 0, 1: 0, 2: 0}  # 파일이 없을 경우 초기 인덱스 설정

current_indices = load_indices()

def update_and_save_indices():
    save_indices(current_indices)

# 문제 데이터를 가져오는 함수
def fetch_problems_by_level(level):
    url = f"https://school.programmers.co.kr/api/v2/school/challenges/?perPage=100&levels[]={level}&order=recent&search=&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [problem['title'] for problem in data['result']]
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return []

# 이메일 전송 함수
def send_email(subject, body, to_addr, from_addr, password):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    message = MIMEMultipart()
    message["From"] = from_addr
    message["To"] = to_addr
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, message.as_string())
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print("이메일 전송에 실패하였습니다:", e)
    finally:
        server.quit()

# 문제 리스트를 문자열로 반환하는 함수
def get_problems_text():
    problems_text = "<<<오늘의 코테 문제>>>\n"
    levels_count = {0: 2, 1: 2, 2: 1}
    for level, count in levels_count.items():
        problems = fetch_problems_by_level(level)
        start_index = current_indices.get(str(level), 0)
        end_index = start_index + count
        selected_problems = problems[start_index:end_index]
        current_indices[str(level)] = end_index
        if selected_problems:
            problems_text += f"레벨 {level} 문제 - " + ", ".join(selected_problems) + "\n"
    update_and_save_indices()
    return problems_text

# 메인 함수
def main():
    from_addr = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')
    to_addr_list = [
        ("신인재", "shininjae1213@naver.com"),
        ("김성권", "skdkim26@gmail.com"),
        ("김희숙", "rz3210@naver.com"),
        ("류지선", "jsryu2043@naver.com"),
        ("장유진", "socommonly@gmail.com"),
        ("이치형", "deeir@naver.com"),
        ("장현욱", "gusdnr1110@naver.com"),
        ("오진솔", "znsol118@gmail.com"),
        ("최혜린", "hlin118@gmail.com")
    ]
    subject = "이번주 코테 문제"
    problems_text = get_problems_text()
    for recipient_name, recipient_email in to_addr_list:
        send_email(subject, problems_text, recipient_email, from_addr, password)

if __name__ == "__main__":
    main()
