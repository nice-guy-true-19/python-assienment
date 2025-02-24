from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    entries = JournalEntry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_entry = JournalEntry(title=title, content=content)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = JournalEntry.query.get_or_404(id)  # Find entry by ID
    db.session.delete(entry)  # Delete the entry
    db.session.commit()  # Save changes
    return redirect(url_for('home'))  # Redirect to home page


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

