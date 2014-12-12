from lib import model_factory

category_list = [
    "Career",
    "Design",
    "Entertainment",
    "Productivity",
    "Programming",
    "Science",
    "Technology"
]
role_list = [
    "Developer",
    "Designer",
]
tag_list = [
    "iOS",
    "Mac",
    "iPad",
    "Task Management",
    "Productivity",
    "GTD",
    "Bullet Journal"
]

categories = {}
roles = {}
tags = {}

for category in category_list:
    categories[category] = model_factory.create_category(name = category)

for role in role_list:
    roles[role] = model_factory.create_role(name = role)

for tag in tag_list:
    tags[tag] = model_factory.create_tag(name = tag)

author = model_factory.create_user(
    email = "lukexor@gmail.com",
    defaults = {
        'full_name': "Lucas Petherbridge",
        'website': "http://lukexor.me/",
        'gravatar': "http://gravatar.com/avatar/e42eb8d925b249e73c1ca53154e38b14?s=100&r=pg&d=mm",
        'phone': "3104863143",
    }
)

article_first = model_factory.create_article(
    title = "First post",
    permalink_title = "first-post",
    defaults = {
        'author': author[0],
        'body': "<p>It's taken me awhile to get around to it, but the site is up and all pages are in a mostly complete state. There's a lot more functionality I want to add like comments and an RSS feed but this is a good start!</p>\n<p>I'll be posting articles about once a month to start with as I finish out the site, and we'll see where to go from there. Happy coding!</p>",
        'category': categories['Programming'][0],
        'minutes_to_read': 1,
        'date_published': "2014-11-18 21:29:50",
    }
)
article_lost = model_factory.create_article(
    title = "\"Lost and Found\" Series : Lessons Learned",
    permalink_title = "lost-and-found-series",
    defaults = {
        'author': author[0],
        'body': "<p>My path to software development as a profession has been a long and insightful journey. I've learned so much in so short a time and I'd like to share my experiences in this five part series I'm dubbing \"Lost and Found\". It's a story of my meandering past; highlighting the early days of my interest in code and of my going astray, only to return, years later, with an even greater passion.</p>\n<p>I hope you follow along with me as I recount the years. The software industry has such a fascinating landscape that changes almost daily. It's a wonder to me how different things are now compared to all those years ago when I first started and how much different the world is because of it. So, without further adieu!</p>\n<h3>Part 1: And so it begins...</h3>",
        'category': categories['Programming'][0],
        'minutes_to_read': 0,
        'date_published': "2014-11-18 21:29:50",
    }
)

project = model_factory.create_project(
    title = "MindYou",
    permalink_title = "mindyou",
    defaults = {
        'description': "<p><strong>MindYou</strong>&nbsp;is a feature-packed task management system for Mac, iPhone and iPad.</p>\n<p>MindYou takes the most useful ideas from top productivity methodologies and&nbsp;combines them together into a single digital platform that can keep up with you wherever you are, with whatever you're doing. You'll get more done in less time than you ever thought possible by keeping your mind on your tasks to keep your tasks off your mind.</p>\n<p>Still under development.</p>\n<p>Based on&nbsp;<a title=\"Getting Things Done\" href=\"http://gettingthingsdone.com/\">Getting Things Done</a>&nbsp;by David Allen,&nbsp;<a title=\"Bullet Journal\" href=\"http://bulletjournal.com/\">Bullet Journal</a>&nbsp;by Ryder Carroll, and Kanban methodologies.</p>",
        'website': "http://mindyou.me/",
        'date_started': "2014-11-18 21:24:18",
        'date_published': "2014-11-18 21:24:20",
    }
)

for project_role in ["Developer", "Designer"]:
    model_factory.add_project_role(
        project = project[0],
        role = roles[project_role][0],
    )

for project_tag in ["iOS", "Mac", "iPad", "Task Management", "Productivity", "GTD", "Bullet Journal"]:
    model_factory.add_project_tag(
        project = project[0],
        tag = tags[project_tag][0],
    )
