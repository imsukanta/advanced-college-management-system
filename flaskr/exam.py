from flask import Blueprint,render_template,request,g,flash,redirect,url_for
from flaskr.models import Dept,Semester,Exam,Question,Answer
from datetime import datetime
from flaskr import db
bp=Blueprint('exam',__name__,url_prefix='/admin-exam')

@bp.route('/')
def exam_dashboard():
    page=request.args.get('page',1,type=int)
    per_page=10
    exam=Exam.query.paginate(page=page,per_page=per_page)
    return render_template('exam.html',exam=exam)
@bp.route('/question')
def question_dashboard():
    page=request.args.get('page',1,type=int)
    per_page=10
    question=Question.query.paginate(page=page,per_page=per_page)
    return render_template('question.html',question=question)

@bp.route('/add-exam',methods=['POST','GET'])
def add_exam():
    dept=Dept.query.all()
    sem=Semester.query.filter_by(is_active=True).all()
    if request.method=="POST":
        exam_name=request.form['exam_name']
        exam_desc=request.form['exam_desc']
        dept_id=request.form['dept']
        sem_id=request.form['sem']
        total_marks=request.form['total_marks']
        duration=request.form['duration']
        is_active=request.form.get('status')=='true'
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        exam=Exam(exam_name=exam_name,description=exam_desc,dept_id=int(dept_id),sem_id=int(sem_id),created_by=int(g.user.user_id),total_marks=total_marks,duration=duration,start_date=start_date,end_date=end_date,is_active=is_active)
        db.session.add(exam)
        db.session.commit()
        flash("Exam Added")
        return redirect(url_for('exam.add_exam'))
    return render_template('addfile/addExam.html',dept=dept,sem=sem)

@bp.route('/show-exam/<int:id>',methods=['POST','GET'])
def show_exam(id):
    exam=Exam.query.get(id)
    if request.method=='POST':
        total_marks=request.form['total_marks']
        duration=request.form['duration']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        is_active=request.form.get('confirmation')=='true'
        exam.total_marks=total_marks
        exam.duration=duration
        exam.start_date=start_date
        exam.end_date=end_date
        exam.is_active=is_active
        db.session.commit()
        return redirect(url_for('exam.exam_dashboard'))    
    return render_template('profile/exam_profile.html',exam=exam)

@bp.route('/add-question',methods=['POST','GET'])
def add_question():
    exam=Exam.query.all()
    if request.method=="POST":
        exam_id=request.form['exam_id']
        question_text=request.form['question_name']
        options=request.form['options']
        marks=request.form['marks']
        correct_answer=request.form['correct_answer']
        if int(marks) <0:
            flash('Marks should not negative')
            return redirect(url_for('exam.add_question'))
        if int(correct_answer) <0:
            flash('Options should not negative')
            return redirect(url_for('exam.add_question'))
        question=Question(exam_id=int(exam_id),question_text=question_text,options=options,marks=marks,correct_answer=correct_answer)
        db.session.add(question)
        db.session.commit()
        flash("Question Added")
        return redirect(url_for('exam.add_question'))
    return render_template('addfile/addQuestion.html',exam=exam)

@bp.route('/show-question/<int:id>',methods=['POST','GET'])
def show_question(id):
    question=Question.query.get(id)
    exam=Exam.query.all()
    if request.method=='POST':
        exam_id=request.form['exam_id']
        question_text=request.form['question_name']
        options=request.form['options']
        marks=request.form['marks']
        correct_answer=request.form['correct_answer']
        if int(marks) <0:
            flash('Marks should not negative')
            return redirect(url_for('exam.add_question'))
        if int(correct_answer) <0:
            flash('Options should not negative')
            return redirect(url_for('exam.add_question'))
        question.exam_id=int(exam_id)
        question.question_text=question_text
        question.options=options
        question.marks=marks
        question.correct_answer=correct_answer
        db.session.commit()
        return redirect(url_for('exam.question_dashboard'))    
    return render_template('profile/show_question.html',question=question,exam=exam)

import json

@bp.route('/exam/<int:exam_id>', methods=['GET'])
def take_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.filter_by(exam_id=exam_id).all()

    # Parse options from JSON string to list
    for q in questions:
        q.options = q.options.split('|')

    return render_template('exam_panel.html', exam=exam, questions=questions)
@bp.route('/submit-exam', methods=['POST'])
def submit_exam():
    student_id = 1  # You should fetch this from session or login
    exam_id = request.args.get('exam_id')
    questions = Question.query.filter_by(exam_id=exam_id).all()

    for question in questions:
        selected = request.form.get(f'q{question.question_id}')
        if selected is not None:
            answer = Answer(
                exam_id=exam_id,
                question_id=question.question_id,
                student_id=student_id,
                selected_answer=json.dumps(int(selected)),
                submission_time=datetime.now()
            )
            db.session.add(answer)

    db.session.commit()
    flash("Exam submitted successfully!")
    return redirect(url_for('index.home'))