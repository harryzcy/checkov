import os
import unittest

from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
from checkov.terraform.checks.resource.aws.AWSCodeGuruHasCMK import check


class TestAWSCodeGuruHasCMK(unittest.TestCase):

    def test(self):
        runner = Runner()
        current_dir = os.path.dirname(os.path.realpath(__file__))

        test_files_dir = os.path.join(current_dir, "example_AWSCodeGuruHasCMK")
        report = runner.run(root_folder=test_files_dir,
                            runner_filter=RunnerFilter(checks=[check.id]))
        summary = report.get_summary()

        passing_resources = {
            'aws_codegurureviewer_repository_association.pass'
        }
        failing_resources = {
            'aws_codegurureviewer_repository_association.ckv_unittest_fail_no_encryption_option',
            'aws_codegurureviewer_repository_association.ckv_unittest_fail_no_kms_key_details',
            'aws_codegurureviewer_repository_association.ckv_unittest_fail_encryption_option_OWNED',
        }
        skipped_resources = {}

        passed_check_resources = set([c.resource for c in report.passed_checks])
        failed_check_resources = set([c.resource for c in report.failed_checks])

        self.assertEqual(summary['passed'], len(passing_resources))
        self.assertEqual(summary['failed'], len(failing_resources))
        self.assertEqual(summary['skipped'], len(skipped_resources))
        self.assertEqual(summary['parsing_errors'], 0)

        self.assertEqual(passing_resources, passed_check_resources)
        self.assertEqual(failing_resources, failed_check_resources)


if __name__ == '__main__':
    unittest.main()