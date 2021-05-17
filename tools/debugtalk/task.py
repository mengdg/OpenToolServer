import os
import sys
import copy
import shutil
import unittest
from celery import shared_task

from tools.debugtalk.utils import get_time_stamp, dump_python_file, dump_yaml_file
from tools.debugtalk.testcase import TestcaseLoader
from tools.debugtalk.exceptions import ObjectDoesNotExist
from tools.debugtalk.compat import is_py3

from tools.debugtalk import logger, testcase, utils, exceptions, runner


# from app.models import ToolInfo, DebugTalk

class TestCase(unittest.TestCase):
    """ create a testcase.
    """
    def __init__(self, test_runner, testcase_dict):
        super(TestCase, self).__init__()
        self.test_runner = test_runner
        self.testcase_dict = copy.copy(testcase_dict)

    def runTest(self):
        """ run testcase and check result.
        """
        try:
            self.test_runner.run_test(self.testcase_dict)
        except exceptions.MyBaseFailure as ex:
            self.fail(repr(ex))
        finally:
            if hasattr(self.test_runner.http_client_session, "meta_data"):
                self.meta_data = self.test_runner.http_client_session.meta_data
                self.meta_data["validators"] = self.test_runner.context.evaluated_validators
                self.test_runner.http_client_session.init_meta_data()


class TestSuite(unittest.TestSuite):
    """ create test suite with a testset, it may include one or several testcases.
        each suite should initialize a separate Runner() with testset config.
    @param
        (dict) testset
            {
                "name": "testset description",
                "config": {
                    "name": "testset description",
                    "parameters": {},
                    "variables": [],
                    "request": {},
                    "output": []
                },
                "testcases": [
                    {
                        "name": "testcase description",
                        "parameters": {},
                        "variables": [],    # optional, override
                        "request": {},
                        "extract": {},      # optional
                        "validate": {}      # optional
                    },
                    testcase12
                ]
            }
        (dict) variables_mapping:
            passed in variables mapping, it will override variables in config block
    """
    def __init__(self, testset, variables_mapping=None, http_client_session=None):
        super(TestSuite, self).__init__()
        self.test_runner_list = []

        self.config = testset.get("config", {})
        self.output_variables_list = self.config.get("output", [])
        self.testset_file_path = self.config.get("path")
        # config_dict_parameters = self.config.get("parameters", [])
        #
        # config_dict_variables = self.config.get("variables", [])
        # variables_mapping = variables_mapping or {}
        # config_dict_variables = utils.override_variables_binds(config_dict_variables, variables_mapping)
        #
        # config_parametered_variables_list = self._get_parametered_variables(
        #     config_dict_variables,
        #     config_dict_parameters
        # )
        self.testcase_parser = testcase.TestcaseParser()
        testcases = testset.get("testcases", [])

        # for config_variables in config_parametered_variables_list:
            # config level
        # self.config["variables"] = config_variables
        test_runner = runner.Runner(self.config, http_client_session)
        print(test_runner)

        for testcase_dict in testcases:
            testcase_dict = copy.copy(testcase_dict)
            # testcase level
            testcase_parametered_variables_list = self._get_parametered_variables(
                testcase_dict.get("variables", []),
                testcase_dict.get("parameters", [])
            )
            print(testcase_dict, testcase_parametered_variables_list)
            for testcase_variables in testcase_parametered_variables_list:
                testcase_dict["variables"] = testcase_variables

                # eval testcase name with bind variables
                variables = utils.override_variables_binds(
                    config_variables,
                    testcase_variables
                )
                self.testcase_parser.update_binded_variables(variables)
                try:
                    testcase_name = self.testcase_parser.eval_content_with_bindings(testcase_dict["name"])
                except (AssertionError, exceptions.ParamsError):
                    logger.log_warning("failed to eval testcase name: {}".format(testcase_dict["name"]))
                    testcase_name = testcase_dict["name"]
                self.test_runner_list.append((test_runner, variables))

                self._add_test_to_suite(testcase_name, test_runner, testcase_dict)

    def _get_parametered_variables(self, variables, parameters):
        """ parameterize varaibles with parameters
        """
        cartesian_product_parameters = testcase.parse_parameters(
            parameters,
            self.testset_file_path
        ) or [{}]

        parametered_variables_list = []
        for parameter_mapping in cartesian_product_parameters:
            parameter_mapping = parameter_mapping or {}
            variables = utils.override_variables_binds(
                variables,
                parameter_mapping
            )

            parametered_variables_list.append(variables)

        return parametered_variables_list

    def _add_test_to_suite(self, testcase_name, test_runner, testcase_dict):
        if is_py3:
            TestCase.runTest.__doc__ = testcase_name
        else:
            TestCase.runTest.__func__.__doc__ = testcase_name

        test = TestCase(test_runner, testcase_dict)
        [self.addTest(test) for _ in range(int(testcase_dict.get("times", 1)))]

    @property
    def output(self):
        outputs = []

        for test_runner, variables in self.test_runner_list:
            out = test_runner.extract_output(self.output_variables_list)
            if not out:
                continue

            in_out = {
                "in": dict(variables),
                "out": out
            }
            if in_out not in outputs:
                outputs.append(in_out)

        return outputs


def init_test_suites(path_or_testsets, mapping=None, http_client_session=None):
    """ initialize TestSuite list with testset path or testset dict
    @params
        testsets (dict/list): testset or list of testset
            testset_dict
            or
            [
                testset_dict_1,
                testset_dict_2,
                {
                    "config": {},
                    "api": {},
                    "testcases": [testcase11, testcase12]
                }
            ]
        mapping (dict):
            passed in variables mapping, it will override variables in config block
    """
    if not testcase.is_testsets(path_or_testsets):
        TestcaseLoader.load_test_dependencies()
        testsets = TestcaseLoader.load_testsets_by_path(path_or_testsets)
    else:
        testsets = path_or_testsets

    # TODO: move comparator uniform here
    mapping = mapping or {}

    if not testsets:
        raise exceptions.TestcaseNotFound

    if isinstance(testsets, dict):
        testsets = [testsets]

    test_suite_list = []
    for testset in testsets:
        test_suite = TestSuite(testset, mapping, http_client_session)
        test_suite_list.append(test_suite)
    return test_suite_list


class ToolRunner(object):

    def __init__(self, **kwargs):
        self.failfast = kwargs.get('failfast')
        self.runner = unittest.TextTestRunner(**kwargs)

    def run(self, path_or_testsets, mapping=None):
        """ start to run test with varaibles mapping
        @param path_or_testsets: YAML/JSON testset file path or testset list
            path: path could be in several type
                - absolute/relative file path
                - absolute/relative folder path
                - list/set container with file(s) and/or folder(s)
            testsets: testset or list of testset
                - (dict) testset_dict
                - (list) list of testset_dict
                    [
                        testset_dict_1,
                        testset_dict_2
                    ]
        @param (dict) mapping:
            if mapping specified, it will override variables in config block
        """
        try:
            test_suite_list = init_test_suites(path_or_testsets, mapping)
        except exceptions.TestcaseNotFound:
            logger.log_error("Testcases not found in {}".format(path_or_testsets))
            sys.exit(1)

        self.summary = {
            "success": True,
            "stat": {},
            "time": {},
            "details": []
        }

        def accumulate_stat(origin_stat, new_stat):
            """ accumulate new_stat to origin_stat
            """
            for key in new_stat:
                if key not in origin_stat:
                    origin_stat[key] = new_stat[key]
                elif key == "start_at":
                    # start datetime
                    origin_stat[key] = min(origin_stat[key], new_stat[key])
                else:
                    origin_stat[key] += new_stat[key]

        for test_suite in test_suite_list:
            result = self.runner.run(test_suite)
        #     test_suite_summary = get_summary(result)
        #
        #     self.summary["success"] &= test_suite_summary["success"]
        #     test_suite_summary["name"] = test_suite.config.get("name")
        #     test_suite_summary["base_url"] = test_suite.config.get("request", {}).get("base_url", "")
        #     test_suite_summary["output"] = test_suite.output
        #     print_output(test_suite_summary["output"])
        #
        #     accumulate_stat(self.summary["stat"], test_suite_summary["stat"])
        #     accumulate_stat(self.summary["time"], test_suite_summary["time"])
        #
        #     self.summary["details"].append(test_suite_summary)

        return self


def run_by_single(index, path):
    """
    1. 数据库中读取工具信息
    2. 将debugtalk文件写入.py文件中
    """
    config = {
        'config': {
            'id': 0,
            'name': ''
        },
    }
    testcase_list = []

    # try:
    #     obj = ToolInfo.objects.get(id=index)
    # except ObjectDoesNotExist:
    #     return testcase_list
    #
    # function_meta = eval(obj.function_meta)
    # name = obj.name
    # tool_id = obj.id

    # config['config']['id'] = tool_id
    # config['config']['name'] = name
    # config['config']['func_meta'] = function_meta
    name = '查询用户信息'
    function_meta = eval("[{'name':'用户信息列表','func':'${test($one)', 'extract':'list', 'setup_hooks': '${sleep(3)}', 'teardown_hooks': '${sleep(3)}'}]")
    config['config']['id'] = 1
    config['config']['name'] = name

    testcase_list.append(config)

    testcase_dir_path = os.path.join(path, name)

    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

        try:
            # debugtalk = DebugTalk.query.filter_by(tool_id=tool_id).debugtalk
            debugtalk = """# !/usr/bin/env python
from time import sleep
def test(one):
    return one
def sleep(text):
    return sleep(text)
"""
        except ObjectDoesNotExist:
            debugtalk = ''

        dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'), debugtalk)

    for test_info in function_meta:
        # func_dict = dict()
        # func_dict['name'] = test_info['name']
        # func_dict['func'] = test_info['func']
        # func_dict['extract'] = test_info['extract']
        testcase_list.append({'test': test_info})

    dump_yaml_file(os.path.join(testcase_dir_path, name + '.yml'), testcase_list)


@shared_task
def talk_run(id, mapping=None):
    logger.setup_logger('INFO')

    kwargs = {
        "failfast": False
    }
    runner = ToolRunner(**kwargs)

    testcase_dir_path = os.path.join(os.getcwd(), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    run_by_single(id, testcase_dir_path)

    runner.run(testcase_dir_path, mapping)

    # shutil.rmtree(testcase_dir_path)

    # print(runner.summary)


talk_run(1, mapping={'one': 1})
