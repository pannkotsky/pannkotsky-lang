from io import StringIO

from flask import Flask, render_template, request

from source.errors import PKLanguageError
from source.helpers import (get_language_tokens_table, get_scan_output_table,
                            get_program_tokens_table, get_idents_table, get_contants_table,
                            get_labels_table)
from source.scan import Scanner
from source.syntax import SyntaxAnalyzer

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
            scanner.scan()
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
            syntax_analyzer = SyntaxAnalyzer(scanner.scan_tokens)
            try:
                syntax_analyzer.run()
            except PKLanguageError as e:
                error = e
            else:
                context['syntax_success'] = True

        context['error'] = error

    return render_template('index.html', **context)
