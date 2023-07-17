from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'GPT4_summaries.db')
app.config['SQLALCHEMY_BINDS'] = {
    'scores': 'sqlite:///' + os.path.join(os.getcwd(), 'scores.db')
}
db = SQLAlchemy(app)

class Summary(db.Model):
    __tablename__ = 'Summaries'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    task = db.Column(db.String(50))
    run = db.Column(db.Integer)
    table_index = db.Column(db.Integer)
    file_path = db.Column(db.String(200))
    summary = db.Column(db.Text)
    main_ideas = db.Column(db.Text)
    main_finding = db.Column(db.Text)
    novelty = db.Column(db.Integer)
    feasibility = db.Column(db.Integer)
    correctness = db.Column(db.Integer)

class Score(db.Model):
    __bind_key__ = 'scores'
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    summary_id = db.Column(db.Integer)
    detailed = db.Column(db.Integer)
    creative = db.Column(db.Integer)
    specific = db.Column(db.Integer)
    prevention = db.Column(db.Integer)
    detection = db.Column(db.Integer)
    societies = db.Column(db.Integer)
    involvement = db.Column(db.Integer)
    red_flags = db.Column(db.Integer)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        author = request.form.get('author')
        summary_id = request.form.get('summary_id')
        detailed = request.form.get('detailed')
        creative = request.form.get('creative')
        specific = request.form.get('specific')
        prevention = request.form.get('prevention')
        detection = request.form.get('detection')
        societies = request.form.get('societies')
        involvement = request.form.get('involvement')
        red_flags = request.form.get('red_flags')
        new_score = Score(author=author, summary_id=summary_id, detailed=detailed, creative=creative, specific=specific, prevention=prevention, detection=detection, societies=societies, involvement=involvement, red_flags=red_flags)
        db.session.add(new_score)
        db.session.commit()
        return redirect('/')
    else:
        #TODO: check if the author has already evaluated all the summaries, the current code is not working since the "GET" part is not reading the author fomr "POST"
        if Score is not None:
            # get all the summary_ids evaluated by the current author
            evaluated_summaries = [score.summary_id for score in
                                   Score.query.filter_by(author=request.form.get('author')).all()]
            # get a summary not yet evaluated by the current author
            summary = Summary.query.filter(Summary.id.notin_(evaluated_summaries)).order_by(func.random()).first()
            if summary is None:
                return "You have evaluated all the results."
            else:
                return render_template('index.html', summary=summary)
        else:
            summary = Summary.query.order_by(func.random()).first()
            if summary is None:
                return "No summary found in the database."
            else:
                return render_template('index.html', summary=summary)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
