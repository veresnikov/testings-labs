import subprocess
import unittest


def runProcess(process: str, args: str) -> str:
    output = subprocess.check_output(["python3", process] + args.split())
    return output.decode("utf-8")


class MyTestCase(unittest.TestCase):
    def test(self):
        with open('result.txt', 'w') as r:
            with open('tests.txt', 'r') as f:
                lines = f.readlines()
                i = 0
                while i < len(lines):
                    input = lines[i].replace('>', '')
                    expected = lines[i + 1]
                    i += 3
                    output = runProcess('./triangle.py', input)
                    if expected == output:
                        r.write('success\n')
                    else:
                        r.write('error\n')


if __name__ == '__main__':
    unittest.main()
