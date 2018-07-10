import re


def parse_base_salary(salary):
    salary_reg = re.compile("\d+(?:,\d{3})*")
    reg_results = salary_reg.findall(salary)
    if len(reg_results) == 0:
        raise RuntimeError(f"Invalid salary: {salary}")
    raw_base_salary = reg_results[0]
    base_salary = int(raw_base_salary.replace(",", ""))
    return base_salary


def parse_salary_type(salary):
    chinese_word_reg = re.compile("[\u4e00-\u9fff]+")
    reg_results = chinese_word_reg.findall(salary)
    if len(reg_results) == 0:
        raise RuntimeError(f"Invalid salary: {salary}")
    return reg_results[0]
