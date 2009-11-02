from gluon.contrib.markdown import WIKI
def getCategories():
	categories = db(db.category.id>0).select(orderby=db.category.title)
	categoryList = ""
	for category in categories:
		categoryList += str(DIV(XML('<a href="'+URL(r=request, c="category", f="view", args=category.id)+'">'+category.title+'</a> ('+str(category.relations.count())+')')))
	return categoryList

def getRecentPosts(limit):
	posts = db(db.post.id>0).select(orderby=~db.post.dateline, limitby=(0,limit))
	recentPosts = ""
	for post in posts:
		recentPosts += str(DIV(XML('<a href="'+URL(r=request, c="post", f="view", args=post.id)+'">'+post.title+'</a>')))
	return recentPosts
	
def getRecentComments(limit):
	comments = db(db.comment.id>0).select(orderby=~db.comment.dateline, limitby=(0, limit))
	recentComments = ""
	for comment in comments:
		recentComments += str(DIV(XML('By '+comment.name+' on <a href="'+URL(r=request, c="post", f="view", args=comment.post_id)+'">'+comment.post_id.title+'</a>')))
	return recentComments

def getArchives():
	from datetime import datetime
	archives = db(db.post.id>0).select(db.post.dateline, distinct=True)
	archiveList = ""
	addedToList = []
	for archive in archives:
		if archive.dateline.strftime("%B %Y") not in addedToList:
			addedToList.append(archive.dateline.strftime("%B %Y"))
			archiveList += str(DIV(XML('<a href="'+URL(r=request, c="archive", f="view", args=archive.dateline.strftime("%Y/%m"))+'">'+archive.dateline.strftime("%B %Y")+'</a>')))
	return archiveList

import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def fetch_codes(body):
	for match in re.finditer(r'\[code(?:=([^]]*))?](.*?)\[/code]', body, re.DOTALL):
		language = match.group(1)
		code = match.group(2)
		lexer = get_lexer_by_name(language, stripall=True)
		formatter = HtmlFormatter(linenos=False, cssclass="source")
		result = highlight(code, lexer, formatter)
		body = body.replace(match.group(0), result)
	return body

def is_admin():
	if auth.user:
		memberships = db(db.auth_membership.user_id==auth.user.id).select()
		for membership in memberships:
			if membership.group_id == 1:
				return True
	else:
		return False

	
