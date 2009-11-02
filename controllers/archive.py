# coding: utf8
pages = db(db.page.id > 0).select()
def view():
	year = request.args(0)
	month = request.args(1)
	query = (db.post.dateline.year()==year)
	if month:
		query = (db.post.dateline.year()==year)&(db.post.dateline.month()==month)
	posts = db(query).select(db.post.id, db.post.title)
	return dict(posts=posts, pages=pages, selectedpage=0)
