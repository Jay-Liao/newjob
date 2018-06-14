import math
import time
import datetime
from newjob_app.utils import yourator
from newjob_app.utils import file_util

if __name__ == "__main__":
    filter_params = {
        "position[]": 1,  # full-time
        # "skillTag[]": [13]  # Python: 13
    }

    # filter_params = {
    #     "position[]": 1,  # full-time
    #     "category[]": 7   # Front-end Engineer
    # }

    total_jobs = list()
    page_size = 20
    result = yourator.find_jobs(params=filter_params)
    total_count = result["total"]
    jobs = result["jobs"]
    total_jobs.extend(jobs)
    pages = math.ceil(total_count / page_size)
    print(f"total_count: {total_count}")
    print(f"pages: {pages}")
    if pages > 1:
        for page in range(2, pages + 1):
            jobs_in_the_page = yourator.find_jobs_by_page(page=page, params=filter_params)
            if len(jobs_in_the_page) > 0:
                total_jobs.extend(jobs_in_the_page)
            else:
                print(f"jobs_in_the_page: {jobs_in_the_page} is []")

    filtered_jobs = [job for job in total_jobs if job["has_salary_info"]]
    print(f"len(total_jobs): {len(total_jobs)}")
    print(f"len(filtered_jobs): {len(filtered_jobs)}")
    # print(f"filtered_jobs: {filtered_jobs}")

    for job in filtered_jobs:
        url_prefix = "https://www.yourator.co"
        path = job["path"]
        url = f"{url_prefix}{path}"
        job["url"] = url

    start = time.time()
    added_salary_jobs = [yourator.do_salary_task(job) for job in filtered_jobs]
    now = datetime.datetime.now()
    time_str = now.strftime("%Y%m%d_%H%M%S")  # ex. 20180118162739
    export_filename = f"{time_str}_export_yourator_{len(added_salary_jobs)}.json"
    export_data = {
        "jobs": added_salary_jobs
    }
    file_util.save_dict_as_json_file(
        file_path=export_filename,
        dict_data=export_data
    )
    print(f"File is exported: {export_filename} {time.time() - start}")
