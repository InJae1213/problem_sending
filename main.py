import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

# 현재 문제의 인덱스를 파일에서 로드하고 저장하는 함수들
def save_indices(indices):
    with open("indices.json", "w") as file:
        json.dump(indices, file)

def load_indices():
    try:
        with open("indices.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {0: 0, 1: 0, 2: 0}

current_indices = load_indices()

def update_and_save_indices():
    save_indices(current_indices)

# 문제 데이터를 가져오는 함수
def fetch_problems_by_level(level):
    url = f"https://school.programmers.co.kr/api/v2/school/challenges/?perPage=20&levels[]={level}&order=recent&search=&page=1"
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
        start_index = current_indices[level]
        end_index = start_index + count
        selected_problems = problems[start_index:end_index]
        current_indices[level] = end_index
        if selected_problems:
            problems_text += f"{level} - " + ", ".join(selected_problems) + "\n"
    update_and_save_indices()
    return problems_text

# 메인 함수
def main():
    from_addr = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')
    to_addr_list = [
        # Email 수신자 리스트
    ]
    subject = "이번주 코테 문제"
    problems_text = get_problems_text()
    for recipient_name, recipient_email in to_addr_list:
        send_email(subject, problems_text, recipient_email, from_addr, password)

if __name__ == "__main__":
    main()
