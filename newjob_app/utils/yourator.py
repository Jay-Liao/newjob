from newjob_app.constants import job_constant
from newjob_app.constants import config_constant


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
    from newjob_app.app import app

    params["page"] = page
    jobs = list()
    response = None
    try:
        response = requests.get(
            url=app.config[config_constant.YOURATOR_JOBS_URL],
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
    from newjob_app.app import app

    response = requests.get(
        url=app.config[config_constant.YOURATOR_JOBS_URL],
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
    from newjob_app.app import app

    url = f"{app.config[config_constant.YOURATOR_BASE_URL]}{job[job_constant.PATH]}"
    print(url)
    salary = find_salary(url=url)
    brand = job[job_constant.COMPANY][job_constant.BRAND]
    job_title = job[job_constant.NAME]
    time.sleep(random.uniform(0.5, 1.3))
    job[job_constant.JOB_INFO] = f"[{brand}] {job_title}"
    job[job_constant.LINK] = url
    job[job_constant.SALARY] = salary
    return job
    # return {
    #     job_constant.JOB_INFO: f"[{brand}] {job_title}",
    #     job_constant.LINK: url,
    #     job_constant.SALARY: salary
    # }


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
        # "skillTag[]": [13]  # Python: 13
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

    filtered_jobs = [job for job in total_jobs if job[job_constant.HAS_SALARY]]
    added_salary_jobs = [do_salary_task(job) for job in filtered_jobs]
    filename = str(int(time.time()))
    print(os.path.join(app.config[config_constant.JOB_DIRECTORY], filename))
    file_util.save_dict_as_json_file(
        file_path=os.path.join(app.config[config_constant.JOB_DIRECTORY], filename),
        dict_data=added_salary_jobs
    )
    return filename


if __name__ == "__main__":
    print(download_jobs())
