from unittest import TestCase, mock

from source.rpn import RPNBuilder


class RPNTestCase(TestCase):
    def test_without_brackets_1(self):
        tokens = 'a + b * c'.split()
        expected_output = 'a b c * +'.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    def test_without_brackets_2(self):
        tokens = 'a * b + c'.split()
        expected_output = 'a b * c +'.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    def test_without_brackets_3(self):
        tokens = 'a + b * c / d'.split()
        expected_output = 'a b c * d / +'.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    def test_with_brackets_1(self):
        tokens = '( a + b ) * c'.split()
        expected_output = 'a b + c *'.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    def test_with_brackets_2(self):
        tokens = 'a + b * ( c + d ) * ( e + f )'.split()
        expected_output = 'a b c d + * e f + * +'.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    def test_declare_and_assign(self):
        tokens = 'var a := b + c'.split()
        expected_output = 'a var b c + :='.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    def test_endlines(self):
        tokens = 'var a := b + c \n a := d'.split(' ')
        expected_output = 'a var b c + := a d :='.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    @mock.patch('source.rpn.generate_label_name')
    def test_if(self, mocked_generate):
        mocked_generate.return_value = '_label_1'
        tokens = 'if a > b \n a := 5 \n b := 6 \n \n print b'.split(' ')
        expected_output = 'a b > _label_1 goto_if_not a 5 := b 6 := _label_1 label b print'.split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    @mock.patch('source.rpn.generate_label_name')
    def test_nested_if(self, mocked_generate):
        mocked_generate.side_effect = ['_label_1', '_label_2']
        tokens = ('if a > b \n '
                  'a := 5 \n '
                  'if b < 3 \n '
                  'b := 6 \n \n \n '
                  'print b').split(' ')
        expected_output = ('a b > _label_1 goto_if_not '
                           'a 5 := '
                           'b 3 < _label_2 goto_if_not '
                           'b 6 := _label_2 label _label_1 label '
                           'b print').split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)

    @mock.patch('source.rpn.generate_label_name')
    def test_nested_if_2(self, mocked_generate):
        mocked_generate.side_effect = ['_label_1', '_label_2']
        tokens = ('if a > b \n '
                  'a := 5 \n '
                  'if b < 3 \n '
                  'b := 6 \n \n '
                  'print a \n \n '
                  'print b').split(' ')
        expected_output = ('a b > _label_1 goto_if_not '
                           'a 5 := '
                           'b 3 < _label_2 goto_if_not '
                           'b 6 := _label_2 label '
                           'a print '
                           '_label_1 label '
                           'b print').split()
        self.assertEqual(RPNBuilder(tokens).build(), expected_output)
