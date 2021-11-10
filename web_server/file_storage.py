import os
import uuid

from flask import session, g, render_template, Blueprint, url_for, request, flash, current_app, send_from_directory
from flask import redirect

from web_server.aut import login_required
from web_server.models import Users, File, db

bp = Blueprint("file_storage", __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ico'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == "POST":
        accessibility = request.form['accessibility']
        if accessibility is None:
            return flash("Choose degree of file accessibility")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No selected files")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_extension = file.filename.split('.')[1]
            unique_filename = f"{str(uuid.uuid4())}.{file_extension}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            file_for_save = File(g.user.id, unique_filename, file.filename, accessibility)
            db.session.add(file_for_save)
            db.session.commit()
            if file_for_save.accessibility == "link":
                return redirect(url_for('file_storage.uploaded_file', filename=unique_filename))
            return redirect(url_for('file_storage.upload_file'))
        else:
            error = "Wrong file extension"
            return render_template('file_upload/file_upload.html', error=error)
    else:
        return render_template('file_upload/file_upload.html')


@bp.route('/upload/<filename>')
def uploaded_file(filename):
    base_url = os.getenv('BASE_URL')
    file_link = f"{base_url}/files/{filename}"
    return render_template('file_upload/file_link.html',
                           file_link=file_link)


@bp.route('/')
def public_files():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()
    files = File.query.filter((File.accessibility == "open"))
    return render_template('file_upload/all_files.html', files=files)


@bp.route('/files/<filename>')
def file_from_link(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/my-files')
@login_required
def privat_files():
    files = File.query.filter((File.user_id == g.user.user_id))
    return render_template('file_upload/all_files.html', files=files)
