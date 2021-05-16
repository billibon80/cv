from flask import Flask, render_template
import json
from datetime import date as dt
from datetime import datetime

with open('static/assets/stories.json', encoding="utf-8") as file:
    posts = json.loads(file.read())[::-1]

with open('static/assets/novel.json', encoding="utf-8") as file:
    novel = json.loads(file.read())[-1]

show_story = 1
name_button = "Older Story →"
story_page = 1

# date = datetime.date.fromisoformat('2021-05-16')
# print(date.strftime('%b ru_RU.UTF-8'))

app = Flask(__name__, static_folder='static')


@app.route('/')
@app.route('/home')
def get_new_posts():
    global name_button
    global story_page
    global show_story

    show_story = 1
    story_page = 1
    name_button = "Older Story →"

    return render_template("index.html", all_posts=posts[:1], dt=dt, name_button=name_button,
                           story_page=story_page, datetime=datetime)


@app.route('/<int:index>')
def get_old_posts(index):
    global show_story
    global name_button
    global story_page

    story_page = index + 1
    number_open_stories = 2

    if show_story < len(posts):
        previous_page = show_story
    else:
        previous_page = len(posts) - 1

    if show_story + number_open_stories < len(posts):
        show_story += number_open_stories
    else:
        show_story = len(posts)
        story_page -= 1
        name_button = "The End of Stories"

    return render_template("index.html", all_posts=posts[previous_page:show_story], dt=dt,
                           name_button=name_button, story_page=story_page, datetime=datetime)


@app.route('/about')
def get_about():
    return render_template('about.html', datetime=datetime)


@app.route('/novel')
def get_novel():
    return render_template('novel.html', novel=novel, datetime=datetime, dt=dt)


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post['id'] == index:
            requested_post = blog_post
    return render_template('post.html', post=requested_post, datetime=datetime, dt=dt)


@app.route('/contact')
def get_contact():
    return render_template('contact.html', datetime=datetime)


if __name__ == "__main__":
    app.run(debug=True)
