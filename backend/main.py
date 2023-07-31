from urllib import request
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
db_name = 'fibonacci_numbers.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
db.init_app(app)

class Fibonacci_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.BigInteger, nullable = False)

@app.route('/fibonacci', methods=['POST'])
def fibonacci_saver():
    n = request.json['n']
    final_sequence = []
    fib_list = [0, 1]

    while len(fib_list) < n:
        fib = fib_list[-1] + fib_list[-2]
        fib_list.append(fib)

    for i in range(1, n + 1):
        exists = Fibonacci_table.query.get(i)
        if exists:
            final_sequence.append(exists.value)
        else:
            new_n = Fibonacci_table(id=i, value=fib_list[i - 1])
            db.session.add(new_n)
            final_sequence.append(fib_list[i - 1])

    db.session.commit()
    return jsonify(final_sequence)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)