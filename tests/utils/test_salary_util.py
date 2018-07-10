import unittest
from newjob_app.constants import job_constant
from newjob_app.utils import salary_util


class TestSalaryUtil(unittest.TestCase):

    def test_parse_salary_interval_with_salary_interval(self):
        test_data = "NT$ 60,000 - 80,000 (月薪)"
        min_salary, max_salary = salary_util.parse_salary_interval(test_data)
        self.assertEqual(60000, min_salary)
        self.assertEqual(80000, max_salary)

    def test_parse_salary_interval_with_only_base_salary(self):
        test_data = "NT$ 60,000 - (月薪)"
        min_salary, max_salary = salary_util.parse_salary_interval(test_data)
        self.assertEqual(60000, min_salary)
        self.assertEqual(job_constant.DEFAULT_MAX_SALARY, max_salary)

    def test_parse_salary_interval_with_no_comma(self):
        test_data = "NT$ 60000 - (月薪)"
        min_salary, max_salary = salary_util.parse_salary_interval(test_data)
        self.assertEqual(60000, min_salary)
        self.assertEqual(job_constant.DEFAULT_MAX_SALARY, max_salary)

    def test_parse_salary_type_with_monthly_type(self):
        test_data = "NT$ 60,000 - 80,000 (月薪)"
        self.assertEquals("月薪", salary_util.parse_salary_type(test_data))

    def test_parse_salary_type_with_annual_type(self):
        test_data = "NT$ 1,400,000 - 2,000,000 (年薪)"
        self.assertEquals("年薪", salary_util.parse_salary_type(test_data))

if __name__ == "__main__":
    unittest.main()
