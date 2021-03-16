import MatrixTest
import random


def parser(stdout: str):
    lines = stdout.splitlines()
    result = {
        "lineCount": len(lines),
        "programName": lines[0],
        "random": random.randint(1, 10)
    }
    # return len(lines)
    return result


def main():
    cmd_template = "python E:\\MatrixTest\\cmd_example_program.py {arg1} {arg2} {arg3}"
    args = {
        "arg1": ["arg1_1", "arg1_2"],
        "arg2": ["arg2_1", "arg2_2", "arg2_3"],
        "arg3": ["arg3_1"]
    }
    mtr = MatrixTest.MatrixTestRunner(cmd_template, args, parser)

    # mtr.run()
    mtr.run(3)
    results = mtr.get_last_result()
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(results)

    mtr.average(["random", "lineCount"])
    # mtr.average()
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    # print(results)

    mtr.to_excel("E:\\MatrixTest\\example_output.xlsx", include_agg=True, include_raw=True)


if __name__ == '__main__':
    main()
