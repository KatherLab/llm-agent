from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(script_dir, 'GPT4_summaries.db')
app.config['SQLALCHEMY_BINDS'] = {
    'scores': 'sqlite:///' + os.path.join(script_dir, 'scores.db')
}
app.secret_key = 'your_secret_key'  # replace with your own secret key

db = SQLAlchemy(app)

def convert_to_html_bullets(text):
    """Convert a text with bullet points into HTML list."""
    points = text.split('-')
    points = [point.strip() for point in points if point]  # remove empty strings
    html_bullets = '<ul>'
    for point in points:
        html_bullets += f'<li>{point}</li>'
    html_bullets += '</ul>'
    return html_bullets

class Summary(db.Model):
    __tablename__ = 'Summaries'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    task_index = db.Column(db.String(50))
    eu_prompt = db.Column(db.String(50))
    repetition_index = db.Column(db.Integer)
    truncation_index = db.Column(db.Integer)
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
    timestamp = db.Column(db.DateTime, default=func.now())


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
        # record the timestamp
        timestamp = datetime.now()

        new_score = Score(author=author, summary_id=summary_id, detailed=detailed, creative=creative, specific=specific,
                          prevention=prevention, detection=detection, societies=societies, involvement=involvement,
                          red_flags=red_flags, timestamp=timestamp)
        db.session.add(new_score)
        db.session.commit()

        # Save author in the session
        session['author'] = author

        return redirect('/')
    else:
        author = session.get('author')
        print("author: ", author)



        if author is not None:
            # Get all the summary_ids in the Score table that this author has already evaluated
            evaluated_summaries = [score.summary_id for score in Score.query.filter_by(author=author).all()]

            # Get a summary not yet evaluated by this author (not in the Score table)
            summary = Summary.query.filter(Summary.id.notin_(evaluated_summaries)).order_by(func.random()).first()

            if summary is None:
                return render_template('change_author.html')
            else:
                summary.main_ideas = convert_to_html_bullets(summary.main_ideas)
                summary.main_finding = convert_to_html_bullets(summary.main_finding)
                return render_template('index.html', summary=summary, author=author)
        else:
            summary = Summary.query.order_by(func.random()).first()

            if summary is None:
                return "No summary found in the database."
            else:
                summary.main_ideas = convert_to_html_bullets(summary.main_ideas)
                summary.main_finding = convert_to_html_bullets(summary.main_finding)
                return render_template('index.html', summary=summary)

@app.route('/change_author', methods=['POST'])
def change_author():
    # Remove the current author from the session
    session.pop('author', None)

    # Redirect back to the main page
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
