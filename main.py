import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# 현재 문제의 인덱스를 추적하기 위한 변수
current_indices = {0: 0, 1: 0, 2: 0}

def fetch_problems_by_level(level):
    url = f"https://school.programmers.co.kr/api/v2/school/challenges/?perPage=20&levels[]={level}&order=recent&search=&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [problem['title'] for problem in data['result']]
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}")
        return []

def send_email(subject, body, to_addr, from_addr, password):
    # 이메일 서버 설정 (Gmail 예시)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # MIME 메시지 생성
    message = MIMEMultipart()
    message["From"] = from_addr
    message["To"] = to_addr
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # 이메일 서버에 연결
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # TLS 보안 시작
    server.login(from_addr, password)
    
    # 이메일 전송
    server.sendmail(from_addr, to_addr, message.as_string())
    
    # 연결 종료
    server.quit()

def get_problems_text():
    problems_text = "<<<오늘의 코테 문제>>>\n"
    levels_count = {0: 2, 1: 2, 2: 1}
    for level, count in levels_count.items():
        problems = fetch_problems_by_level(level)
        start_index = current_indices[level]
        end_index = start_index + count
        selected_problems = problems[start_index:end_index]
        current_indices[level] += count
        if selected_problems:
            problems_text += f"{level} - " + ", ".join(selected_problems) + "\n"
    return problems_text

def main():
    # 환경 변수로부터 이메일 정보를 불러옴
    from_addr = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')
    to_addr = "shininjae1213@naver.com"  # 수정할 필요가 있으면 여기를 변경하세요.
    subject = "이번주 코테 문제"
    problems_text = get_problems_text()
    send_email(subject, problems_text, to_addr, from_addr, password)

if __name__ == "__main__":
    main()
