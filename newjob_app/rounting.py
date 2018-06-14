import http
from flask_restplus import Resource
from flask_restplus import fields
from newjob_app.app import api
from newjob_app.services.job_service import job_service


ns = api.namespace("jobs", description="Jobs operations")

job = api.model("job", {
    "job_info": fields.String(required=True, description="Company name and job title"),
    "salary": fields.String(required=True, description="Salary range"),
    "link": fields.String(required=True, description="Job detail link")
})

jobs_info = api.model("jobs_info", {
    "jobs": fields.List(fields.Nested(job), required=True),
    "jobs_count": fields.Integer(required=True),
    "source": fields.String(required=True)
})


@ns.route("/")
class TodoList(Resource):
    @ns.marshal_with(jobs_info)
    def get(self):
        """get jobs"""
        jobs = job_service.get_jobs()
        result = {
            "jobs": jobs,
            "source": job_service.get_file_name(),
            "jobs_count": len(jobs)
        }
        return result, http.HTTPStatus.OK
