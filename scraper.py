import os
import time
from newjob_app import setting
from newjob_app.utils import yourator
from newjob_app.utils import job_util
from newjob_app.utils import file_util

MINUTE = 60
HOUR = 60 * MINUTE
# EIGHT_HOURS = 8 * HOUR
EIGHT_HOURS = 30

if __name__ == "__main__":
    while True:
        job_files = job_util.get_job_files()
        # remove out of date job files
        if len(job_files) > 1:
            job_files = [int(job_file) for job_file in job_files]
            job_files = sorted(job_files, reverse=True)
            for index in range(1, len(job_files)):
                file_path = os.path.join(setting.JOB_DIRECTORY, str(job_files[index]))
                file_util.remove_file(file_path=file_path)
                print(f"remove old job files: {file_path}")
        print("start download jobs")
        time.sleep(EIGHT_HOURS)
        file_name = yourator.download_jobs()
        print(f"file_name: {file_name}")
