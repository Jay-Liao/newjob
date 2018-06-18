from newjob_app.constants import job_constant


class JobService(object):
    def __init__(self):
        self.__file_name, self.__jobs = JobService.__get_jobs_from_file()
        self.__skill_tags = self.__get_skill_tags()
        self.__job_map = self.__build_job_map()
        self.__skill_tag_map = self.__build_skill_tag_map()

    def __reload_jobs(self):
        latest_file_name = JobService.__get_latest_file_name()
        if self.__file_name != latest_file_name:
            self.__init__()

    def get_file_name(self):
        return self.__file_name

    def get_jobs(self, skill_tags, intersect):
        self.__reload_jobs()
        if skill_tags is None:
            return self.__jobs
        skill_tags = [tag.lower() for tag in skill_tags if len(tag) > 0]
        job_filters = list()
        for skill_tag in skill_tags:
            job_ids = self.__skill_tag_map.get(skill_tag, None)
            if job_ids is not None:
                job_filters.append(set(job_ids))
        if len(job_filters) == 0:
            return list()
        the_job_filter = job_filters[0]
        for job_filter in job_filters:
            if intersect:
                the_job_filter = the_job_filter.intersection(job_filter)
            else:
                the_job_filter = the_job_filter.union(job_filter)
        filter_job_ids = list(the_job_filter)
        jobs = list()
        for job_id in filter_job_ids:
            jobs.append(self.__job_map[job_id])
        return jobs

    def get_skill_tags(self):
        self.__reload_jobs()
        return self.__skill_tags

    def __build_skill_tag_map(self):
        skill_tag_map = dict()
        for job in self.__jobs:
            tags = job.get(job_constant.SKILL_TAGS, list())
            for tag in tags:
                tag_name = tag[job_constant.TAG_NAME].lower()
                if tag_name not in skill_tag_map:
                    skill_tag_map[tag_name] = list()
                skill_tag_map[tag_name].append(job[job_constant.ID])
        return skill_tag_map

    def __build_job_map(self):
        job_map = dict()
        for job in self.__jobs:
            job_map[job[job_constant.ID]] = job
        return job_map

    def __get_skill_tags(self):
        skill_tags = dict()
        for job in self.__jobs:
            tags = job.get(job_constant.SKILL_TAGS, list())
            for tag in tags:
                field = tag[job_constant.SKILL_FIELD]
                if field not in skill_tags:
                    skill_tags[field] = set()
                skill_tags[field].add(tag[job_constant.TAG_NAME])

        for k, v in skill_tags.items():
            skill_tags[k] = list(skill_tags[k])
        return skill_tags

    @staticmethod
    def __get_latest_file_name():
        import os
        from newjob_app.app import app
        from newjob_app.constants import config_constant

        file_names = os.listdir(app.config[config_constant.JOB_DIRECTORY])
        file_names = [file_name for file_name in file_names if file_name.isdigit()]
        file_name_numbers = [int(file_name) for file_name in file_names]
        latest_file_name = str(max(file_name_numbers)) if len(file_name_numbers) > 0 else "default"
        return latest_file_name

    @staticmethod
    def __get_jobs_from_file():
        import os
        from newjob_app.app import app
        from newjob_app.utils import file_util
        from newjob_app.constants import config_constant

        latest_file_name = JobService.__get_latest_file_name()
        jobs = file_util.read_dict_from_json_file(
            os.path.join(app.config[config_constant.JOB_DIRECTORY], latest_file_name)
        )
        return latest_file_name, jobs


job_service = JobService()
