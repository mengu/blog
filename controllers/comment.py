# coding: utf8
# try something like
def create():
    postid = request.vars.postid
    name = auth.user.first_name+" "+auth.user.last_name if auth.user else request.vars.name
    email = auth.user.email if auth.user else request.vars.email
    comment = request.vars.comment
    db.comment.insert(post_id=postid, name=name, email=email, comment=comment)
    redirect(URL(r=request, c="post", f="view", args=postid))

@auth.requires_membership('Admin')
def delete():
		db(db.comment.id == request.args(0)).delete()
		redirect("/blog/post/view/"+request.vars.postid)
