from flask import Blueprint,render_template,g,request,redirect,url_for,flash
from flaskr.models import User,Staff,Student
from flaskr import db
from flaskr.login import permission_required
from flaskr.models import Enquiry
from flask_mail import Message
from flaskr import mail

bp=Blueprint("index",__name__)

@bp.route("/admin-dashboard")
@permission_required('dashboard')
def dashboard():
    user=db.session.query(User).count()  
    staff=db.session.query(Staff).count()
    student=db.session.query(Student).count()
    return render_template("index.html",user=user,staff=staff,student=student)
@bp.route("/")
def home():
    return render_template("mainpage.html")

@bp.route("/enquiry-page", methods=["GET", "POST"])
def enquiry_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Optional: Add basic validation
        if not name or not email:
            flash("Name and Email are required!", "danger")
            return redirect(url_for("main.enquiry_page"))

        # Create enquiry object
        new_enquiry = Enquiry(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        # Save to DB
        db.session.add(new_enquiry)
        db.session.commit()
        subject="Successfully Received Enquiry"
        msg = Message(subject, recipients=[request.form['email']])
        msg.body= f"""
            Hello {name},

            Please wait for sometime. We're shortly reach out to you.

            Thank you for contact us!

            - Your Team Name
            """

        mail.send(msg)
        flash("Your enquiry has been submitted successfully!", "success")
        return redirect(url_for("index.enquiry_page"))

    return render_template("enq.html")

@bp.route('/update-enquiry/<int:id>', methods=['GET', 'POST'])
def update_enquiry(id):
    enquiry = db.get_or_404(Enquiry, id)
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if name and email:
            enquiry.name = name
            enquiry.email = email
            enquiry.phone = phone
            enquiry.subject = subject
            enquiry.message = message

            db.session.commit()
            flash("Enquiry updated successfully", "success")
            return redirect(url_for('enquiry.dashboard_enquiry'))  # replace with your actual dashboard route
        else:
            flash("Name and Email are required", "danger")
            return redirect(url_for('index.dashboard_enquiry'))

    return render_template("updatefile/updateEnquiry.html", enquiry=enquiry)
@bp.route('/delete-enquiry/<int:id>')
def delete_enquiry(id):
    enquiry = Enquiry.query.get_or_404(id)
    db.session.delete(enquiry)
    db.session.commit()
    flash("Enquiry deleted successfully", "success")
    return redirect(url_for("index.dashboard_enquiry"))  # replace with your actual dashboard route
@bp.route("/dashboard-enquiry")
def dashboard_enquiry():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    enquiry = Enquiry.query.paginate(page=page, per_page=per_page)
    return render_template('admin_enq.html', enquiry=enquiry)
