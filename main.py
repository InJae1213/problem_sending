import requests
import json

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

def send_problems_to_kakao(problems):
    token = "eb0217dc013841d207beb684a8223b5b"  # 카카오 API 토큰
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "object_type": "text",
        "text": problems,
        "link": {
            "web_url": "https://school.programmers.co.kr",
            "mobile_web_url": "https://school.programmers.co.kr"
        },
        "button_title": "문제 보러가기"
    }
    response = requests.post("https://kapi.kakao.com/v2/api/talk/memo/default/send", headers=headers, data={"template_object": json.dumps(data)})
    if response.status_code != 200:
        print(f"Failed to send Kakao message: HTTP {response.status_code}")
    else:
        print("Message sent successfully!")

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
    problems_text = get_problems_text()
    send_problems_to_kakao(problems_text)

if __name__ == "__main__":
    main()
