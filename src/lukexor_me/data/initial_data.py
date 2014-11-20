from lib import model_factory

model_factory.create_category(name = "Programming")

for role in ["Developer", "Designer"]:
    model_factory.create_role(name = role)

model_factory.create_article(
    title = "First post",
    permalink_title = "first_post",
    summary = "The site is up and running!",
    body = "<p>It's taken me awhile to get around to it, but the site is up and all pages are in a mostly complete state. There's a lot more functionality I want to add like comments and an RSS feed but this is a good start!</p>\n<p>I'll be posting articles about once a month to start with as I finish out the site, and we'll see where to go from there. Happy coding!</p>",
    category = "Programming",
    minutes_to_read = 1,
    is_published = True,
    date_published = "2014-11-18 21:29:50",
    created = "2014-11-18 21:29:50",
    updated = "2014-11-18 21:59:58",
)

model_factory.create_project(
    title = "MindYou",
    permalink_title = "mindyou",
    description = "<p><strong>MindYou</strong>&nbsp;is a feature-packed task management system for Mac, iPhone and iPad.</p>\n<p>MindYou takes the most useful ideas from top productivity methodologies and&nbsp;combines them together into a single digital platform that can keep up with you wherever you are, with whatever you're doing. You'll get more done in less time than you ever thought possible by keeping your mind on your tasks to keep your tasks off your mind.</p>\n<p>Still under development.</p>\n<p>Based on&nbsp;<a title=\"Getting Things Done\" href=\"http://gettingthingsdone.com/\">Getting Things Done</a>&nbsp;by David Allen,&nbsp;<a title=\"Bullet Journal\" href=\"http://bulletjournal.com/\">Bullet Journal</a>&nbsp;by Ryder Carroll, and Kanban methodologies.</p>",
    date_started = "2014-11-18 21:24:18",
    created = "2014-11-18 21:24:20",
    updated = "2014-11-18 22:03:51",
    website = "http://mindyou.me/",
    summary = "Keep your mind on your tasks to keep your tasks off your mind.",
)
