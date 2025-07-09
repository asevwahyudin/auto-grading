print("Script sudah berjalan!")
import requests

API_URL = "https://lms.guru.kemendikdasmen.go.id"
API_TOKEN = "S8q6OE6eEErGyGd8aSYK0G1KGzHk0E1sKPI4LGHpXtHpnYactbjYOLFr80kpNPAk"
COURSE_ID = 78689
ASSIGNMENT_ID = [2115018, 2115019]

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

for assignment_id in ASSIGNMENT_ID:
    url = f"{API_URL}/api/v1/courses/{COURSE_ID}/assignments/{assignment_id}/submissions"
    params = {"per_page": 100}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        submissions = response.json()
        for submission in submissions:
            if submission['submitted_at']:  # hanya yang sudah submit
                user_id = submission['user_id']
                grade_url = f"{url}/{user_id}"
                payload = {"submission[posted_grade]": "100"}
                grade_response = requests.put(grade_url, headers=headers, data=payload)
                if grade_response.status_code == 200:
                    print(f"User {user_id} di assignment {assignment_id} sudah diberi nilai 100.")
                else:
                    print(f"Gagal memberi nilai untuk User {user_id} di assignment {assignment_id}.")
    else:
        print(f"Gagal mengambil data submission untuk assignment {assignment_id}.")
