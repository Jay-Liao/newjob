import os
import time
from newjob_app.utils import job_util
from newjob_app.utils import file_util
from newjob_app.utils import yourator
from newjob_app import setting
from threading import Thread

MINUTE = 60
HOUR = 60 * MINUTE
EIGHT_HOURS = 8 * HOUR


def run_web_script():
    # start the gunicorn server with custom configuration
    # You can also using app.run() if you want to use the flask built-in server -- be careful about the port
    os.system("gunicorn -c gunicorn.conf newjob_app.app:app")


def scraper():
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
        file_name = yourator.download_jobs()
        print(f"file_name: {file_name}")
        time.sleep(EIGHT_HOURS)


def start_scheduler():
    t = Thread(target=scraper)
    t.start()


def run():
    start_scheduler()
    run_web_script()


if __name__ == '__main__':
    run()
