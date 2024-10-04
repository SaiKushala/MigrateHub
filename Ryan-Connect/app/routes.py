from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify, session
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, CommentForm, SearchForm
from app.models import User, Post, Comment
import pycountry
import json

main = Blueprint('main', __name__)

@main.route("/")
def root():
    return redirect(url_for('main.login'))

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    countries = list(pycountry.countries)

    if request.method == 'POST':
        country_code = request.form.get('country')
        state_name = request.form.get('state')

        with open('app/static/js/countries+states+cities.json', encoding='utf-8') as f:
            data = json.load(f)

        country_data = next((item for item in data if item["iso2"] == country_code), None)
        states = country_data["states"] if country_data else []
        state_data = next((state for state in states if state["name"] == state_name), None)
        cities = state_data["cities"] if state_data else []

        form.state.choices = [(state["name"], state["name"]) for state in states]
        form.city.choices = [(city["name"], city["name"]) for city in cities]

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('An account with this email already exists. Please use a different email or login.', 'danger')
                return redirect(url_for('main.register'))
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                        password=hashed_password, preferred_language=form.preferred_language.data, city=form.city.data,
                        state=form.state.data, country=form.country.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('main.login'))
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    else:
        form.state.choices = []
        form.city.choices = []

    return render_template('register.html', title='Register', form=form, countries=countries)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = SearchForm()
    countries = [(country.alpha_2, country.name) for country in pycountry.countries]
    form.from_country.choices = countries
    form.to_country.choices = countries

    if request.method == 'POST':
        # Get selected country codes from form data
        from_country_code = request.form.get('from_country')
        to_country_code = request.form.get('to_country')

        # Load the states and cities data
        with open('app/static/js/countries+states+cities.json', encoding='utf-8') as f:
            data = json.load(f)

        # Set the choices for states and cities based on the selected country
        if from_country_code:
            country_data = next((item for item in data if item["iso2"] == from_country_code), None)
            if country_data:
                form.from_state.choices = [(state["name"], state["name"]) for state in country_data["states"]]
            if form.from_state.data:
                state_data = next((state for state in country_data["states"] if state["name"] == form.from_state.data), None)
                if state_data:
                    form.from_city.choices = [(city["name"], city["name"]) for city in state_data["cities"]]

        if to_country_code:
            country_data = next((item for item in data if item["iso2"] == to_country_code), None)
            if country_data:
                form.to_state.choices = [(state["name"], state["name"]) for state in country_data["states"]]
            if form.to_state.data:
                state_data = next((state for state in country_data["states"] if state["name"] == form.to_state.data), None)
                if state_data:
                    form.to_city.choices = [(city["name"], city["name"]) for city in state_data["cities"]]

        if form.validate_on_submit():
            from_location = f"{form.from_city.data or ''}, {form.from_state.data or ''}, {form.from_country.data or ''}".strip(", ")
            to_location = f"{form.to_city.data or ''}, {form.to_state.data or ''}, {form.to_country.data or ''}".strip(", ")

            post = Post.query.filter_by(from_location=from_location, to_location=to_location).first()
            if not post:
                post = Post(from_location=from_location, to_location=to_location, user_id=current_user.id)
                db.session.add(post)
                db.session.commit()

            session['post_id'] = post.id
            return redirect(url_for('main.post', post_id=post.id))

        flash('Please fill in the required fields.', 'danger')

    return render_template('dashboard.html', title='Dashboard', form=form)

@main.route("/search", methods=['POST'])
@login_required
def search():
    form = SearchForm()
    countries = [(country.alpha_2, country.name) for country in pycountry.countries]
    form.from_country.choices = countries
    form.to_country.choices = countries

    if request.method == 'POST':
        from_country_code = request.form.get('from_country')
        to_country_code = request.form.get('to_country')

        with open('app/static/js/countries+states+cities.json', encoding='utf-8') as f:
            data = json.load(f)

        if from_country_code:
            country_data = next((item for item in data if item["iso2"] == from_country_code), None)
            if country_data:
                form.from_state.choices = [(state["name"], state["name"]) for state in country_data["states"]]
            if form.from_state.data:
                state_data = next((state for state in country_data["states"] if state["name"] == form.from_state.data), None)
                if state_data:
                    form.from_city.choices = [(city["name"], city["name"]) for city in state_data["cities"]]

        if to_country_code:
            country_data = next((item for item in data if item["iso2"] == to_country_code), None)
            if country_data:
                form.to_state.choices = [(state["name"], state["name"]) for state in country_data["states"]]
            if form.to_state.data:
                state_data = next((state for state in country_data["states"] if state["name"] == form.to_state.data), None)
                if state_data:
                    form.to_city.choices = [(city["name"], city["name"]) for city in state_data["cities"]]

        if form.validate_on_submit():
            from_location = f"{form.from_city.data or ''}, {form.from_state.data or ''}, {form.from_country.data or ''}".strip(", ")
            to_location = f"{form.to_city.data or ''}, {form.to_state.data or ''}, {form.to_country.data or ''}".strip(", ")

            post = Post.query.filter_by(from_location=from_location, to_location=to_location).first()
            if not post:
                post = Post(from_location=from_location, to_location=to_location, user_id=current_user.id)
                db.session.add(post)
                db.session.commit()

            session['post_id'] = post.id
            return redirect(url_for('main.post', post_id=post.id))

        flash('Please fill in the required fields.', 'danger')

    return redirect(url_for('main.dashboard'))

@main.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    reply_form = CommentForm(prefix="reply")

    if form.validate_on_submit() and not reply_form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.post', post_id=post.id))

    if reply_form.validate_on_submit() and request.form.get('parent_id'):
        parent_id = request.form.get('parent_id')
        parent_comment = Comment.query.get_or_404(parent_id)
        reply = Comment(content=reply_form.content.data, user_id=current_user.id, post_id=post.id, parent_id=parent_comment.id)
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been added!', 'success')
        return redirect(url_for('main.post', post_id=post.id))

    comments = Comment.query.filter_by(post_id=post.id, parent_id=None).order_by(Comment.date_posted.desc()).all()
    similar_posts = find_similar_posts(post)

    return render_template('post.html', title='Post', post=post, form=form, reply_form=reply_form, comments=comments, similar_posts=similar_posts)

def find_similar_posts(post):
    similar_posts = []

    from_country = post.from_location.split(', ')[-1]
    to_country = post.to_location.split(', ')[-1]

    results = Post.query.join(Comment).filter(
        Post.from_location.like(f"%{from_country}%"),
        Post.to_location.like(f"%{to_country}%"),
        Post.id != post.id
    ).distinct().all()

    seen_posts = set()
    filtered_results = [res for res in results if res.id not in seen_posts]
    if filtered_results:
        seen_posts.update([res.id for res in filtered_results])
        similar_posts = filtered_results

    return similar_posts

@main.route("/location_data", methods=['GET'])
def location_data():
    with open('app/static/js/countries+states+cities.json', encoding='utf-8') as f:
        data = json.load(f)

    country_code = request.args.get('country')
    state_name = request.args.get('state')

    if country_code:
        country_data = next((item for item in data if item["iso2"] == country_code), None)
        if country_data:
            if state_name:
                state_data = next((state for state in country_data["states"] if state["name"] == state_name), None)
                if state_data:
                    return jsonify(state_data["cities"])
                return jsonify([])
            return jsonify(country_data["states"])
    return jsonify([])
