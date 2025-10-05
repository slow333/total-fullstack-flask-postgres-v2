import os
from flask import (
  Blueprint, request, redirect, url_for,
  render_template as render, flash, current_app) # type: ignore
from ...models import UserProfile as Profile, User
from app import db
from .utils import pagenation
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'static/uploads/profiles'

bp = Blueprint("user_profile", __name__, url_prefix="/apps/profiles")

@bp.route("/")
@login_required
def profile_list():
  page, profile_page, total_pages, page_len, start_page, end_page = pagenation(Profile)

  return render("apps/user_profile/profile_home.html", 
                profiles=profile_page, 
                page=page, 
                total_pages=total_pages, 
                start_page=start_page, 
                end_page=end_page, 
                profile_page_len=page_len)

def save_resized_picture(form_picture):
    """Resizes and saves an uploaded picture."""
    filename = secure_filename(form_picture.filename)
    upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    os.makedirs(upload_path, exist_ok=True)
    
    # Resize image
    output_size = (128, 128)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    
    picture_path = os.path.join(upload_path, filename)
    img.save(picture_path)
    
    return f'/{UPLOAD_FOLDER}/{filename}'
@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_user():
  if request.method == "POST":
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    address = request.form.get("address")
    
    profile_image_uri = '/static/image/icon/heart.png' # Default image
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename != '':
            profile_image_uri = save_resized_picture(file)

    user = db.session.query(Profile).filter_by(user_id=current_user.id).first()
    if user is not None:
      flash("이미 프로필이 생성되어 있습니다.")
      return redirect(url_for("user_profile.profile_list"))
    if not firstname or not lastname:
      flash("이름은 필수입니다.")
      return render("apps/user_profile/create_profile.html")
    else:
      db.session.add(Profile(firstname=firstname, lastname=lastname, address=address, profile_image=profile_image_uri, user_id = current_user.id))
      db.session.commit()
      flash("프로필이 생성되었습니다.")
      return redirect(url_for("user_profile.profile_list"))
  return render("apps/user_profile/create_profile.html")

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(id):
  profile = db.session.get(Profile, id)
  user = db.session.get(User, current_user.id)
  if not profile:
      flash("Profile not found.")
      return redirect(url_for("user_profile.profile_list")), 404
  
  if profile.user_id != current_user.id:
      flash("You are not authorized to edit this profile.")
      return redirect(url_for("user_profile.profile_list"))

  if request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    address = request.form.get("address")

    user.username = username
    user.email = email
    db.session.commit()

    profile.firstname = firstname
    profile.lastname = lastname
    profile.address = address

    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename != '':
            profile.profile_image = save_resized_picture(file)

    db.session.commit()
    flash("Profile updated successfully.")
    return redirect(url_for("user_profile.profile_list"))
  else:
    return render("apps/user_profile/edit_profile.html", profile=profile)

@bp.route("/<int:id>/delete", methods=["GET","POST"])
@login_required
def delete_user(id):
  profile = db.session.get(Profile, id)
  if request.method == "POST":
    if profile and profile.user_id == current_user.id:
      db.session.delete(profile)
      db.session.commit()
      flash("Profile deleted successfully.")
    else:
      flash("Profile not found or you are not authorized to delete it.")
    return redirect(url_for("user_profile.profile_list"))
  else:
    return render("apps/user_profile/delete_profile.html", profile=profile)
  
