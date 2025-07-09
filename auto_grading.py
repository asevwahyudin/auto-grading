import httpx

API_URL = "https://lms.guru.kemendikdasmen.go.id/api/v1"
ACCESS_TOKEN = "SHlV2fJXdPeJRnZ8N5oj4qXncD7cwd7MmHnCGvZrpl5I15i5lN2VSVcYYoNPpH6T"
COURSE_ID = "78689"
ASSIGNMENT_IDS = ["2115018", "2115019"]  # ← Bisa tambah ID lain di sini

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "User-Agent": "curl/8.0",
    "Accept": "*/*"
}

def get_submissions(client, assignment_id):
    url = f"{API_URL}/courses/{COURSE_ID}/assignments/{assignment_id}/submissions"
    response = client.get(url, headers=headers)
    print(f"Status GET submissions for assignment {assignment_id}: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Gagal mengambil submissions untuk assignment {assignment_id}.")
        return []

def auto_grade(client, submissions, assignment_id):
    for submission in submissions:
        user_id = submission['user_id']
        submitted = submission['submitted_at']
        if submitted:
            grade_url = f"{API_URL}/courses/{COURSE_ID}/assignments/{assignment_id}/submissions/{user_id}"
            payload = {
                "submission[posted_grade]": "100"
            }
            response = client.put(grade_url, headers=headers, data=payload)
            print(f"User {user_id} di assignment {assignment_id} dinilai 100, status: {response.status_code}")
        else:
            print(f"User {user_id} di assignment {assignment_id} belum submit, dilewati.")

with httpx.Client(http2=True, verify=True) as client:
    for assignment_id in ASSIGNMENT_IDS:
        submissions = get_submissions(client, assignment_id)
        auto_grade(client, submissions, assignment_id)
