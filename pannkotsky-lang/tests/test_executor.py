from unittest import TestCase

from source.exec import Executor
from tests.helpers import captured_output


class ExecutorTestCase(TestCase):
    def test_prepare_and_execute(self):
        tokens = ('a var '
                  'b var 34 := '
                  '12 11 > _label_1 goto_if_not '
                  'a 5 := '
                  '4 13 < _label_2 goto_if_not '
                  'b 6 := _label_2 label '
                  'a print '
                  '_label_1 label '
                  'b print').split()
        executor = Executor(tokens)
        expected_prepared_tokens = {
            0: 'a',
            1: 'var',
            2: 'b',
            3: 'var',
            4: '34',
            5: ':=',
            6: '12',
            7: '11',
            8: '>',
            9: 28,
            10: 'goto_if_not',
            11: 'a',
            12: '5',
            13: ':=',
            14: '4',
            15: '13',
            16: '<',
            17: 24,
            18: 'goto_if_not',
            19: 'b',
            20: '6',
            21: ':=',
            24: 'a',
            25: 'print',
            28: 'b',
            29: 'print',
        }
        self.assertEqual(executor.tokens, expected_prepared_tokens)
        with captured_output() as (out, err):
            executor.execute()

        output = out.getvalue()
        self.assertEqual(output, '5\n6\n')

    def test_execute_with_false_condition_1(self):
        tokens = ('a var '
                  'b var 34 := '
                  '11 12 > _label_1 goto_if_not '
                  'a 5 := '
                  '4 13 < _label_2 goto_if_not '
                  'b 6 := _label_2 label '
                  'a print '
                  '_label_1 label '
                  'b print').split()
        executor = Executor(tokens)
        with captured_output() as (out, err):
            executor.execute()

        output = out.getvalue()
        self.assertEqual(output, '34\n')

    def test_execute_with_false_condition_2(self):
        tokens = ('a var '
                  'b var 34 := '
                  '12 11 > _label_1 goto_if_not '
                  'a 5 := '
                  '13 4 < _label_2 goto_if_not '
                  'b 6 := _label_2 label '
                  'a print '
                  '_label_1 label '
                  'b print').split()
        executor = Executor(tokens)
        with captured_output() as (out, err):
            executor.execute()

        output = out.getvalue()
        self.assertEqual(output, '5\n34\n')
