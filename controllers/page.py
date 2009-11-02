# coding: utf8
# try something like
pages = db(db.page.id > 0).select()
    
def view():
    page = db.page[request.args(0)]
    return dict(page=page, pages=pages, selectedpage=page.id)
