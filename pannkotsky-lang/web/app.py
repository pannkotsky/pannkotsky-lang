from io import StringIO

from flask import Flask, render_template, request

from source.errors import PKLanguageError
from source.helpers import (get_language_tokens_table, get_scan_output_table,
                            get_program_tokens_table, get_idents_table, get_contants_table,
                            get_labels_table, get_rpn_table)
from source.scan import Scanner
from source.syntax import SyntaxAnalyzer
from source.rpn import RPNBuilder
from source.exec import Executor

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    context = {
        'tokens_table': get_language_tokens_table(),
    }
    if request.method == 'POST':
        program = request.form['program'].replace('\r\n', '\n')
        context['program'] = program

        inp = StringIO(program)
        scanner = Scanner(inp)
        error = None

        try:
            scan_tokens = scanner.scan()
        except PKLanguageError as e:
            error = e
        else:
            context.update({
                'scan_output_table': get_scan_output_table(scanner),
                'program_tokens_table': get_program_tokens_table(scanner),
                'idents_table': get_idents_table(scanner),
                'contants_table': get_contants_table(scanner),
                'labels_table': get_labels_table(scanner),
            })
        finally:
            inp.close()

        if error is None:
            syntax_analyzer = SyntaxAnalyzer(scan_tokens)
            try:
                syntax_tokens = syntax_analyzer.run()
            except PKLanguageError as e:
                error = e
            else:
                context['syntax_success'] = True

        if error is None:
            rpn_builder = RPNBuilder(syntax_tokens)
            rpn_tokens = rpn_builder.build()
            context.update({
                'rpn_steps_table': get_rpn_table(rpn_builder),
                'rpn_tokens': ' '.join(rpn_tokens),
            })

            if 'input' in rpn_tokens:
                error = 'Input operator is not supported in web interface'
            else:
                executor = Executor(rpn_tokens)
                output = executor.execute()
                context['executor_output'] = output

        context['error'] = error

    return render_template('index.html', **context)
