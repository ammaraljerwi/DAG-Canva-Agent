import requests


def get_design(token, designId):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data = {"design_id": designId, "format": {"type": "jpg", "quality": 100}}

    try:
        response = requests.post(
            "https://api.canva.com/rest/v1/exports", headers=headers, json=data
        )
        response.raise_for_status()
    except Exception as E:
        print(E)

    job = response.json()["job"]

    res = get_job_status(token, job["id"])

    return res


def get_job_status(token, jobid):
    maxattempts = 15
    attempts = 0
    while attempts < maxattempts:
        try:
            response = requests.get(
                f"https://api.canva.com/rest/v1/exports/{jobid}",
                headers={"authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
        except Exception as E:
            print(E)
        res = response.json()["job"]
        print(res)
        if res["status"] == "success":
            return res["urls"]
        elif res["status"] == "in_progress":
            attempts += 1
        elif res["status"] == "failed":
            return res["error"]
