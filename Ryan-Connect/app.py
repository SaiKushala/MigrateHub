from app import create_app
from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
app = create_app()
@app.route('/about')
def about():
      return render_template('about.html')
@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Example logic for processing the contact form data
    print(f"Name: {name}, Email: {email}, Message: {message}")

    # Redirect after form submission
    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)





