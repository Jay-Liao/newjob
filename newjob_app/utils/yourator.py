def find_salary(url):
    import re
    import requests
    from bs4 import BeautifulSoup

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
    import time
    import random

    url = job["url"]
    salary = find_salary(url=url)
    brand = job["company"]["brand"]
    job_title = job["name"]
    time.sleep(random.uniform(0.5, 1.3))
    return {
        "job_info": f"[{brand}] {job_title}",
        "link": url,
        "salary": salary
    }


def download_jobs():
    import os
    import math
    import time
    from newjob_app.app import app
    from newjob_app.utils import file_util
    from newjob_app.constants import config_constant

    # make sure directory exists
    file_util.make_dirs(app.config[config_constant.JOB_DIRECTORY])
    filter_params = {
        "position[]": 1,  # full-time
        "skillTag[]": [13]  # Python: 13
    }

    total_jobs = list()
    page_size = 20
    result = find_jobs(params=filter_params)
    total_count = result["total"]
    jobs = result["jobs"]
    total_jobs.extend(jobs)
    pages = math.ceil(total_count / page_size)
    if pages > 1:
        for page in range(2, pages + 1):
            jobs_in_the_page = find_jobs_by_page(page=page, params=filter_params)
            if len(jobs_in_the_page) > 0:
                total_jobs.extend(jobs_in_the_page)

    filtered_jobs = [job for job in total_jobs if job["has_salary_info"]]
    for job in filtered_jobs:
        url_prefix = "https://www.yourator.co"
        path = job["path"]
        url = f"{url_prefix}{path}"
        job["url"] = url
    added_salary_jobs = [do_salary_task(job) for job in filtered_jobs]
    filename = str(int(time.time()))
    file_util.save_dict_as_json_file(
        file_path=os.path.join(app.config[config_constant.JOB_DIRECTORY], filename),
        dict_data=added_salary_jobs
    )
    return filename
