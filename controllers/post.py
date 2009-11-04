# coding: utf8
# try something like
pages = db(db.page.id > 0).select()
categories = db(db.category.id > 0).select(orderby=db.category.title)
def index():
    posts = db(db.post.id > 0).select()
    for i in range(len(posts)):
    	for relation in posts[i].relations.select():
    		posts[i].categories = relation.category.title.join(",")
    return dict(posts=posts, pages=pages)
    
def view():
		post = db.post[request.args(0)]
		categories = {}
		for relation in post.relations.select():
			categories[relation.category] = relation.category.title
			post.categories = categories
		return dict(post=post, pages=pages, selectedpage=0)

@auth.requires_membership('Admin')
def new():
	categorylist = str()
	j = 1
	for i in range(len(categories)):
		categorylist += str(INPUT(_type="checkbox", _name="categories", _value=categories[i].id))+categories[i].title+" "
		if j % 4 == 0: categorylist += "<br />"
		j = j + 1
	return dict(categories=categorylist, pages=pages, selectedpage=0)

@auth.requires_membership('Admin')
def edit():
	post = db.post[request.args(0)]
	postcategories = [relation.category for relation in post.relations.select()]
	categorylist = str()
	j = 1
	for i in range(len(categories)):
		if categories[i].id in postcategories:
			categorylist += str(INPUT(_type="checkbox", _name="categories", _value=categories[i].id, value="on"))+categories[i].title+" "
		else:
			categorylist += str(INPUT(_type="checkbox", _name="categories", _value=categories[i].id))+categories[i].title+" "
		if j % 4 == 0: categorylist += "<br />"
		j = j + 1
	return dict(post=post, categories=categorylist, pages=pages, selectedpage=0)

@auth.requires_membership('Admin')
def create():
	title = request.vars.title
	body = request.vars.body
	post = db.post.insert(title=title, body=body)
	if post.id:
		for category in request.vars.categories:
			db.relations.insert(post=post.id, category=category)
	redirect(URL(r=request, f="view", args=post.id))	

@auth.requires_membership('Admin')
def update():
	title = request.vars.title
	body = request.vars.body
	post = db.post[request.vars.postid]
	postcategories = [relation.category for relation in post.relations.select()]
	db(db.post.id == post.id).update(title=title, body=body)
	# update categories.
	request.vars.categories = [request.vars.categories] if type(request.vars.categories).__name__ == 'int' else request.vars.categories
	i = 0
	for pcategory in request.vars.categories:
		request.vars.categories[i] = int(request.vars.categories[i])
		if int(pcategory) not in postcategories:
			db.relations.insert(post=post.id, category=pcategory)
		i = i + 1
	for ecategory in postcategories:
		if ecategory not in request.vars.categories:
			db((db.relations.category==ecategory)&(db.relations.post==request.vars.postid)).delete()
	redirect(URL(r=request, f="view", args=post.id))

@auth.requires_membership('Admin')
def delete():
	db(db.post.id == request.args(0)).delete()
	redirect("/blog/")


