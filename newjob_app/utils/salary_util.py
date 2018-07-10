import re
from newjob_app.constants import job_constant


def parse_salary_interval(salary):
    salary_reg = re.compile("\d+(?:,\d{3})*")
    reg_results = salary_reg.findall(salary)
    if len(reg_results) == 1:
        return int(reg_results[0].replace(",", "")), job_constant.DEFAULT_MAX_SALARY
    elif len(reg_results) == 2:
        return int(reg_results[0].replace(",", "")), int(reg_results[1].replace(",", ""))
    else:
        raise RuntimeError(f"Invalid salary: {salary}")


def parse_salary_type(salary):
    chinese_word_reg = re.compile("[\u4e00-\u9fff]+")
    reg_results = chinese_word_reg.findall(salary)
    if len(reg_results) == 0:
        raise RuntimeError(f"Invalid salary: {salary}")
    return reg_results[0]
