import http
from flask_restplus import Resource
from flask_restplus import reqparse
from flask_restplus import fields
from newjob_app.app import api
from newjob_app.services.job_service import job_service
from newjob_app.constants import job_constant


ns = api.namespace("jobs", description="Jobs operations")

job = api.model("job", {
    job_constant.JOB_INFO: fields.String(required=True, description="Company name and job title"),
    job_constant.SALARY: fields.String(required=True, description="Salary range"),
    job_constant.LINK: fields.String(required=True, description="Job detail link")
})

jobs_info = api.model("jobs_info", {
    "jobs": fields.List(fields.Nested(job), required=True),
    "jobs_count": fields.Integer(required=True),
    "source": fields.String(required=True)
})

parser = reqparse.RequestParser()
parser.add_argument("skill_tags", type=str, action="append")
parser.add_argument("intersect", type=int, default=0, choices=[0, 1])
parser.add_argument("expected_monthly_salary", type=int, default=None)
parser.add_argument("expected_annual_salary", type=int, default=None)


@ns.route("")
class TodoList(Resource):
    @ns.marshal_with(jobs_info)
    @ns.expect(parser)
    def get(self):
        """get jobs"""
        args = parser.parse_args()
        skill_tags = args["skill_tags"]
        intersect = args["intersect"]
        expected_monthly_salary = args["expected_monthly_salary"]
        expected_annual_salary = args["expected_annual_salary"]
        jobs = job_service.get_jobs(
            skill_tags=skill_tags,
            intersect=intersect,
            expected_monthly_salary=expected_monthly_salary,
            expected_annual_salary=expected_annual_salary
        )
        result = {
            "jobs": jobs,
            "source": job_service.get_file_name(),
            "jobs_count": len(jobs)
        }
        return result, http.HTTPStatus.OK


@ns.route("/skill-tags")
class TodoList(Resource):
    def get(self):
        """get skill tags"""
        return job_service.get_skill_tags(), http.HTTPStatus.OK
