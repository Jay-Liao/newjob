import os


"""
Project
"""
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JOB_DIRECTORY = os.path.join(BASE_DIR, "newjob_app", "jobs")

"""
Flask CONFIG
"""
# swagger
SWAGGER_UI_DOC_EXPANSION = "list"
RESTPLUS_MASK_SWAGGER = False

"""
Yourator
"""
YOURATOR_BASE_URL = "https://www.yourator.co"
YOURATOR_JOBS_URL = "https://www.yourator.co/api/v2/jobs"
