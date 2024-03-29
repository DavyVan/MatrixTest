# MatrixTest: Make your machine busy, make you idle.

[![PyPI](https://img.shields.io/pypi/v/MatrixTest)](https://pypi.org/project/MatrixTest/)
[![GitHub](https://img.shields.io/github/license/DavyVan/MatrixTest)](https://github.com/DavyVan/MatrixTest)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/MatrixTest)](https://pypi.org/project/MatrixTest/)
[![Read the Docs](https://img.shields.io/readthedocs/matrixtest)](https://matrixtest.readthedocs.io/en/latest/)

`MatrixTest` is a tool for matrix test where you have to run a cluster of similar shell commands.
When these commands have similar pattern, they are just combinations of different arguments (including argument 0, the executable itself).
Using `MatrixTest`, the only a few things you need to do are: configure, run, and output.
By providing a formatted command template string, all the possible arguments, and a function to parse the standard output, `MatrixTest` will handle the rest for you.
After that, just wait and find the results in the Excel.

__*This tutorial only show the very basic usage, for full functionalities, please refer to the [API Documentation](https://matrixtest.readthedocs.io/en/latest/).*__

# How to use

---


`MatrixTest` is a pure Python module so that you need to install and import it into your Python test script.

In the following How-tos, a toy script will be used as the executable.
It can accept any arguments and echo them out.
The source code is as simple as below:

```python
import sys

for item in sys.argv:
    print(item)
```

It can be executed with:

```shell
python cmd_example_program.py arg1 arg2 arg3    # You can add more
```

This will output:
```text
cmd_example_program.py      # argv[0]
arg1                        # argv[1]
arg2                        # argv[2]
arg3                        # argv[3]
```

## Install

---


```shell
pip install MatrixTest
```

Then you can import it in your script as:
```python
import MatrixTest
```

## Configure `MatrixTestRunner`

---

`MatrixTestRunner` is the main component of `MatrixTest` package.
You need to pass all the required information via its constructor:

```python
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
```

`cmd_template` is the command line template string.
`MatrixTest` uses Python's `string.format_map()` to generate generate executable command lines.
The template string includes mutable parts braced with `{key}` where the `key` is the name for that specific place and it will be replaced before actual execution.

`args` is a `dict` storing all possible values for all the keys. For example, 6 commands will be generated from the above configuration:
```text
python E:\MatrixTest\cmd_example_program.py arg1_1 arg2_1 arg3_1
python E:\MatrixTest\cmd_example_program.py arg1_1 arg2_2 arg3_1
python E:\MatrixTest\cmd_example_program.py arg1_1 arg2_3 arg3_1
python E:\MatrixTest\cmd_example_program.py arg1_2 arg2_1 arg3_1
python E:\MatrixTest\cmd_example_program.py arg1_2 arg2_2 arg3_1
python E:\MatrixTest\cmd_example_program.py arg1_2 arg2_3 arg3_1
```

`parser` is a parser function that takes textual `stdout` of each command and output parsed result(s). 
For example, you may want to get the numeric execution time from "Data processed in 2.333 seconds".
You can return a single or multiple result(s) from the parser function.
In the example above, we output multiple results in a dict.

Finally, just pass all three parameters into the `MatrixTestRunner` constructor and then it will check the parameters and do some initialization works.

## Run

---

To start testing, call the `run()` function with a integer indicating how many times you would like to execute repeatly:

```python
    mtr.run()                           # repeat once by default
    mtr.run(3)                          # repeat three times
```

## Aggregate (statistics result)

---

After getting the raw data, you may calculate the aggregated results from it. Take arithmetic mean as the example here:

```python
    mtr.average(["random", "lineCount"])        # only calculate mean for designated keys, 
                                                # remember we return these from the parser function
    mtr.average()                               # calculate mean for all keys
```

For now, we support the following aggregation operators:

* average (arithmetic mean)

## Access the results

---

We use `pandas.DataFrame` to store all the results for the current run.
Both raw data and aggregated data are stored in a single DataFrame.

### Data layout

The structure of the result table is like below:

| cmd_full                                                         | arg1   | arg2   | arg3   | attempt1_lineCount | attempt1_programName                 | attempt1_random | attempt2_lineCount | ... | avg_random | avg_lineCount |
|------------------------------------------------------------------|--------|--------|--------|--------------------|--------------------------------------|-----------------|--------------------|-----|------------|---------------|
| python E:\MatrixTest\cmd_example_program.py arg1_1 arg2_1 arg3_1 | arg1_1 | arg2_1 | arg3_1 | 4                  | E:\MatrixTest\cmd_example_program.py | 6               | 4                  |     | 3          | 4             |
| ...                                                              |        |        |        |                    |                                      |                 |                    |     |            |               |

The table starts with the full command and arguments, followed by results for every attempt.
The columns are named after `attempt<No.repeat>_<key from parser>`.
Finally, aggregated results in those `avg_<key from parser & params of average()>` columns.

Data types are inferred by `pandas`.

### Access the internal data structure

You can directly access the `DataFrame` by calling `mtr.get_last_result()`.

### Output to Excel

Generally, we recommend you to output your data to an Excel spreadsheet for further inspection.

```python
    mtr.to_excel("E:\\MatrixTest\\example_output.xlsx", include_agg=True, include_raw=True)
```

The first parameter is the output file path. Also, you can choose whether include raw/aggregated data in the Excel or not via the last two parameters.

## Email Notification Service

---

From version `1.3.0`, you have the option to send an email to a designated email address when the experiments finished (i.e. at the end of `run()`)
or when the Excel file is generated (i.e. at the end of `to_excel()`) then you will find the Excel file in the attachment.

### How to enable email notification

First, you need to instantiate a `EmailProvider`:
```python
    email_provider = MatrixTest.EmailService.MailjetProvider(api_key='xxxx',
                                                             api_secret='xxxx')
```

For now we only support the [Mailjet](https://mailjet.com) as the email service vendor.

__Please note:__ There is a key pair in the `example.py` that you can use for free. But please __DO NOT__ send more than
200 emails per day. That is the limit of Mailjet free account. We encourage you to create your own account and then replace
the keys if you expect to receive a lot of emails.

Then, register the provider to `MatrixTestRunner` and enable the feature:
```python
    mtr.register_email_service(email_provider, "example@example.com")
    mtr.enable_email_notification()
```
Only one recipient is allowed.

You can also do this at initialization, refer to the [doc](https://matrixtest.readthedocs.io/en/latest/MatrixTestRunner.html#MatrixTest.MatrixTestRunner.MatrixTestRunner.__init__).

__Please note:__ By enabling this, you will only receive a notification which includes the argument matrix for your reference.
Keep reading if you want to receive the Excel file.

To receive a copy of the generate Excel file, just set the `send_by_email` argument to `True`. However, you still need to 
register the provider and recipient.
```python
    mtr.to_excel("./example_output.xlsx", send_by_email=True)
```

__Please note:__ You will receive two emails if you enable both of above. Usually, if you want to receive the Excel file,
just enable it once when you call `to_excel()`.

# Contributing

Any of your comments, issues, PRs are welcome and appreciated.

# Dependencies

* Pandas
* openpyxl
* colorama