def get_job_files():
    import os
    from newjob_app import setting

    file_names = os.listdir(setting.JOB_DIRECTORY)
    file_names = [file_name for file_name in file_names if file_name.isdigit()]
    return file_names


def get_latest_job_file():
    job_files = get_job_files()
    job_files = [int(job_file) for job_file in job_files]
    latest_job_file = str(max(job_files)) if len(job_files) > 0 else "default"
    return latest_job_file
