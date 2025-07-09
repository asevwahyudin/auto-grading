            
print("Script sudah berjalan!")
import requests

API_URL = "https://lms.guru.kemendikdasmen.go.id/"  # ganti dengan domain Canvas kamu
API_TOKEN = "S8q6OE6eEErGyGd8aSYK0G1KGzHk0E1sKPI4LGHpXtHpnYactbjYOLFr80kpNPAk"    # tempel Access Token di sini
COURSE_ID = 78689                              # ganti dengan Course ID kamu
ASSIGNMENT_ID = 2115018, 2115019                          # ganti dengan Assignment ID kamu

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Ambil data submission
url = f"{API_URL}/api/v1/courses/{COURSE_ID}/assignments/{ASSIGNMENT_ID}/submissions"
params = {"per_page": 100}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    submissions = response.json()
    for submission in submissions:
        if submission['submitted_at']:  # hanya yang sudah submit
            user_id = submission['user_id']
            grade_url = f"{url}/{user_id}"
            payload = {"submission": {"posted_grade": "100"}}
            grade_response = requests.put(grade_url, headers=headers, json=payload)
            if grade_response.status_code == 200:
                print(f"User {user_id} sudah diberi nilai 100.")
            else:
                print(f"Gagal memberi nilai untuk User {user_id}.")
else:
    print("Gagal mengambil data submission.")
