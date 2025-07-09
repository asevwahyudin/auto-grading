import httpx

API_URL = "https://lms.guru.kemendikdasmen.go.id/api/v1"
ACCESS_TOKEN = "SHlV2fJXdPeJRnZ8N5oj4qXncD7cwd7MmHnCGvZrpl5I15i5lN2VSVcYYoNPpH6T"
COURSE_ID = "78689"
ASSIGNMENT_ID = "2115018"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "User-Agent": "curl/8.0",
    "Accept": "*/*"
}

def get_submissions(client):
    url = f"{API_URL}/courses/{COURSE_ID}/assignments/{ASSIGNMENT_ID}/submissions"
    response = client.get(url, headers=headers)
    print("Status GET submissions:", response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        print("Gagal mengambil submissions.")
        return []

def auto_grade(client, submissions):
    for submission in submissions:
        user_id = submission['user_id']
        submitted = submission['submitted_at']
        if submitted:
            grade_url = f"{API_URL}/courses/{COURSE_ID}/assignments/{ASSIGNMENT_ID}/submissions/{user_id}"
            payload = {
                "submission[posted_grade]": "100"
            }
            response = client.put(grade_url, headers=headers, data=payload)
            print(f"User {user_id} dinilai 100, status: {response.status_code}")
        else:
            print(f"User {user_id} belum submit, dilewati.")

with httpx.Client(http2=True, verify=True) as client:
    submissions = get_submissions(client)
    auto_grade(client, submissions)
