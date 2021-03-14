import MatrixTest
import random
import pandas as pd


def parser(stdout: str):
    lines = stdout.splitlines()
    result = {}
    result["lineCount"] = len(lines)
    result["programName"] = lines[0]
    result["random"] = random.randint(1, 10)
    # return len(lines)
    return result


def main():
    args = {
        "arg1": ["arg1_1", "arg1_2"],
        "arg2": ["arg2_1", "arg2_2", "arg2_3"],
        "arg3": ["arg3_1"]
    }
    mt = MatrixTest.MatrixTest("python E:\\MatrixTest\\cmd_example_program.py {arg1} {arg2} {arg3}", args, parser)
    # mt.run()
    mt.run(3)
    results = mt.get_last_result()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(results)
    mt.average(["random", "lineCount"])
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(results)


if __name__ == '__main__':
    main()
