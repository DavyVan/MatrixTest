import MatrixTest


def parser(stdout: str) -> str:
    lines = stdout.splitlines()
    print(lines)
    return "hello"


def main():
    mt = MatrixTest.MatrixTest("dir F:\\坚果云\\CRPG-Book-Chinese\\{path}", {"path": ["宣传材料", "归档"]}, parser)
    mt.run()
    mt.run(3)


if __name__ == '__main__':
    main()

