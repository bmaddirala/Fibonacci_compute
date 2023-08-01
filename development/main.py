from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
app = Flask(__name__)
db_name = 'fibonacci_numbers.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
db.init_app(app)

CORS(app)

class Fibonacci_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.BigInteger, nullable = False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        n = request.form.get('input', type=int)
        return redirect(url_for('fibonacci_saver', n=n))
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def fibonacci_checker():
    if request.method == 'POST':
        n = request.form.get('n', type=int)
    else:
        n = request.args.get('n', default=1, type=int)
    final_sequence = []
    fib_list = [0, 1]

    while len(fib_list) < n:
        fib = fib_list[-1] + fib_list[-2]
        fib_list.append(fib)

    for num in range(1, n + 1):
        exists = Fibonacci_table.query.get(num)
        if exists:
            final_sequence.append(exists.value)
        else:
            new_number = Fibonacci_table(id=num, value=fib_list[num - 1])
            db.session.add(new_number)
            final_sequence.append(fib_list[num - 1])

    db.session.commit()
    return render_template('result.html', fibonacci_sequence=', '.join(map(str, final_sequence)))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
