from unittest import TestCase

from source.exec import Executor
from tests.helpers import captured_output


class ExecutorTestCase(TestCase):
    def test_execute(self):
        tokens = ('a var '
                  'b var 34 := '
                  '12 11 > 24 goto_if_not '
                  'a 5 := '
                  '4 13 < 22 goto_if_not '
                  'b 6 := '
                  'a print '
                  'b print').split()
        executor = Executor(tokens)
        with captured_output() as (out, err):
            executor.execute()

        output = out.getvalue()
        self.assertEqual(output, '5\n6\n')

    def test_execute_with_false_condition_1(self):
        tokens = ('a var '
                  'b var 34 := '
                  '11 12 > 24 goto_if_not '
                  'a 5 := '
                  '4 13 < 22 goto_if_not '
                  'b 6 :='
                  'a print '
                  'b print').split()
        executor = Executor(tokens)
        with captured_output() as (out, err):
            executor.execute()

        output = out.getvalue()
        self.assertEqual(output, '34\n')

    def test_execute_with_false_condition_2(self):
        tokens = ('a var '
                  'b var 34 := '
                  '12 11 > 24 goto_if_not '
                  'a 5 := '
                  '13 4 < 22 goto_if_not '
                  'b 6 := '
                  'a print '
                  'b print').split()
        executor = Executor(tokens)
        with captured_output() as (out, err):
            executor.execute()

        output = out.getvalue()
        self.assertEqual(output, '5\n34\n')
