# coding: utf8
pages = db(db.page.id>0).select()
def view():
	category = db.category[request.args(0)]
	return dict(category=category, pages=pages, selectedpage=0)
