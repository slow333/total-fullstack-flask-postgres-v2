from flask import (
  Blueprint, request, redirect, 
  render_template as render, flash, url_for) # type: ignore
from flask_login import login_required, current_user
from app import db
from ...models import Blog
from .utils import pagenation

bp = Blueprint("blog", __name__, url_prefix="/apps/blogs")

@bp.route("/")
def blog_home():
  page, profile_page, total_pages, page_len, start_page, end_page = pagenation(Blog)
  blogs = Blog.query.order_by(Blog.id.desc()).all()

  return render("apps/blog/blog_home.html", 
                blogs=blogs, 
                profiles=profile_page, 
                page=page, 
                total_pages=total_pages, 
                start_page=start_page, 
                end_page=end_page, 
                profile_page_len=page_len)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_blog():
  if request.method == "POST":
    title = request.form["title"]
    content = request.form["content"]
    comment = request.form["comment"]

    if not title or not content:
      flash("타이틀과 컨텐트는 필수입니다.")
      return render("apps/blog/create_blog.html")
    else:
      db.session.add(Blog(title=title, content=content, comment=comment, author_id=current_user.id))
      db.session.commit()
      return redirect(url_for("blog.blog_home"))
  return render("apps/blog/create_blog.html")

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_blog(id):
  if request.method == "POST":
    title = request.form["title"]
    content = request.form["content"]
    comment = request.form["comment"]
    
    if not title or not content:
      flash("타이틀과 컨텐트는 필수입니다.")
      return render("apps/blog/update_blog.html")
    else:
      blog = db.session.query(Blog).filter_by(id=id).first()
      blog.title = title
      blog.content = content
      blog.comment = comment
      db.session.commit()
    return redirect("/apps/blogs/")
  else:
    blog = db.session.query(Blog).filter_by(id=id).first()
    return render("apps/blog/edit_blog.html", blog=blog)

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_blog(id):
  if request.method == "POST":
    blog = db.session.query(Blog).filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()
    return redirect("/apps/blogs/")
  elif request.method == "GET":
    blog = db.session.query(Blog).filter_by(id=id).first()
    return render("apps/blog/delete_blog.html", blog=blog)
  return None

