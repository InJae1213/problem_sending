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
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # MIME 메시지 생성
    message = MIMEMultipart()
    message["From"] = from_addr
    message["To"] = to_addr
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # 이메일 서버에 연결
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # TLS 보안 시작
        server.login(from_addr, password)
        
        # 이메일 전송
        server.sendmail(from_addr, to_addr, message.as_string())
        
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print("이메일 전송에 실패하였습니다:", e)
    finally:
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
    from_addr = "mcsniper1213@gmail.com"
    #os.environ.get('EMAIL_USER')
    password = "hpqymvtkqhbbtdyz"
    #os.environ.get('EMAIL_PASSWORD')
    to_addr_list = [
        ("신인재", "shininjae1213@naver.com"),
        ("김성권", "skdkim26@gmail.com"),
        ("김희숙", "rz3210@naver.com"),
        ("류지선", "jsryu2043@naver.com"),
        ("장유진", "email.com"),
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
