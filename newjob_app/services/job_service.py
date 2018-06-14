class JobService(object):
    def __init__(self):
        self.__file_name, self.__jobs = JobService.__download_jobs()

    def get_file_name(self):
        return self.__file_name

    def get_jobs(self):
        return self.__jobs

    @staticmethod
    def __download_jobs():
        import os
        from newjob_app.app import app
        from newjob_app.utils import file_util
        from newjob_app.constants import config_constant

        file_names = os.listdir(app.config[config_constant.JOB_DIRECTORY])
        file_names = [file_name for file_name in file_names if file_name.isdigit()]
        file_name_numbers = [int(file_name) for file_name in file_names]
        target_file_name = str(max(file_name_numbers)) if len(file_name_numbers) > 0 else "default"
        jobs = file_util.read_dict_from_json_file(
            os.path.join(app.config[config_constant.JOB_DIRECTORY], target_file_name)
        )
        return target_file_name, jobs

job_service = JobService()
