# coding: utf8

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  
pages = db(db.page.id > 0).select()
from gluon.contrib.markdown import WIKI
import math
def index():
	perpage = 3
	totalposts = db(db.post.id > 0).count()
	totalpages = totalposts / perpage
	if totalposts > perpage and totalpages == 1 and totalpages * perpage != totalposts:
		totalpages = 2
	page = int(request.vars.page) if request.vars.page else 1
	limit = int(page - 1) * perpage
	posts = db(db.post.id > 0).select(orderby=~db.post.id, limitby=(limit, perpage))
	for i in range(len(posts)):
		categories = {}
		for relation in posts[i].relations.select():
			categories[relation.category] = relation.category.title
			posts[i].categories = categories
	return dict(posts=posts, pages=pages, selectedpage=1, totalpages=totalpages, postpage=page)


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth(), pages=pages, selectedpage=0)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
