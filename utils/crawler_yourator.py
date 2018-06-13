import re
from gevent import monkey
from bs4 import BeautifulSoup


monkey.patch_all()


def find_salary(url):
    import requests

    salary = "Unknown"
    response = None
    try:
        response = requests.get(
            url=url,
            timeout=180
        )
        if response is None or response.status_code != 200:
            print(f"find_salary({url}) fail with invalid response")
            return salary
        content = response.content
        whole_body_soup = BeautifulSoup(content, "lxml")
        pattern = re.compile("薪\)")
        article = whole_body_soup.find("article", text=pattern)
        salary = article.text
    except:
        print(f"find_salary({url}) fail.")
    finally:
        if response is not None:
            response.close()
        return salary


def find_jobs_by_page(page, params):
    import requests

    search_job_url = "https://www.yourator.co/api/v2/jobs"
    params["page"] = page
    jobs = list()
    response = None
    try:
        response = requests.get(
            url=search_job_url,
            params=params,
            timeout=60
        )
        result = response.json()
        jobs = result["jobs"]
    except:
        print(f"find_jobs() fail.")
    finally:
        if response is not None:
            response.close()
        return jobs


def find_jobs(params):
    import requests
    search_job_url = "https://www.yourator.co/api/v2/jobs"
    response = requests.get(
        url=search_job_url,
        params=params,
        timeout=60
    )

    try:
        data = response.json()
        return data
    except:
        print(f"find_jobs() fail.")
        return list()
    finally:
        response.close()


def do_salary_task(job):
    url = job["url"]
    salary = find_salary(url=url)
    brand = job["company"]["brand"]
    job_title = job["name"]
    return {
        "job_info": f"[{brand}] {job_title}",
        "link": url,
        "salary": salary
    }
