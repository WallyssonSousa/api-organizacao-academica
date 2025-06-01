from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import ExamResult, Subject, SubjectResult

results_bp = Blueprint('results', __name__)
@results_bp.route('/results', __name__)
@jwt_required()
def create_exam_result():
    data = request.get_json()
    user_id = get_jwt_identity()

    exam_type = data.get('type')
    total_questions = data.get('total_questions')
    correct = data.get('correct_answers')
    notes = data.get('notes', '')

    if not all([exam_type, total_questions, correct]):
        return jsonify({"msg": "Missing required fields"}), 400
    
    incorrect = total_questions - correct
    exam = ExamResult(
        type = exam_type, 
        total_questions = total_questions,
        correct_answers = correct,
        incorrect_answers = incorrect,
        notes = notes, 
        user_id = user_id
    )

    db.session.add(exam)
    db.session.commit()

    subjects_data = data.get('subjects', [])
    for sub in subjects_data:
        subject = Subject.query.get(sub['subject_id'])
        if subject:
            subject_result = SubjectResult(
                exam_id = exam.id,
                subject_id = subject.id,
                correct = sub['correct'], 
                incorrect = sub['incorrect']
            )
            db.session.add(subject_result)

        db.session.commit()
        return jsonify({"msg": "Exam result created successfully", "exam_id": exam.id}), 201
    

@results_bp.route('/results/<int:exam_id>', methods=['GET'])
@jwt_required()
def get_exam_result(exam_id):
    user_id = get_jwt_identity()
    exam = ExamResult.query.filter_by(id=exam_id, user_id=user_id).first()

    if not exam:
        return jsonify({"msg": "Exam result not found"}), 404

    subject_data = []
    for sr in exam.subject_results:
        subject = Subject.query.get(sr.subject_id)
        if subject:
            subject_data.append({
                "subject_id": subject.id,
                "correct": sr.correct,
                "incorrect": sr.incorrect
            })

    return jsonify({
        'type': exam.type,
        'total_questions': exam.total_questions,
        'correct_answers': exam.correct_answers,
        'incorrect_answers': exam.incorrect_answers,
        'notes': exam.notes,
        'date': exam.date.strftime('%Y-%m-%d %H:%M:%S'),
        'subjects': subject_data
    }), 200


@results_bp.route('/results', methods=['GET'])
def get_timeline():
    user_id = get_jwt_identity()
    exams = ExamResult.query.filter_by(user_id=user_id).order_by(ExamResult.date)

    timeline = []
    for exam in exams:
        timeline.append({
            'date': exam.date.strftime('%Y-%m-%d %H:%M:%S'),
            'type': exam.type,
            'correct_answers': exam.correct_answers,
            'incorrect_answers': exam.incorrect_answers,
        })

        return jsonify(timeline), 200
    
@results_bp.route('/results/subjects', methods=['GET'])
@jwt_required()
def get_subject_results():
    user_id = get_jwt_identity()
    results = SubjectResult.query.join(ExamResult).filter(ExamResult.user_id == user_id).all()

    stats = {}
    for r in results:
        subject_name = r.subject.name
        if subject_name not in stats:
            stats[subject_name] = { 'correct' : 0, 'incorrect' : 0}
        stats[subject_name]['correct'] += r.correct
        stats[subject_name]['incorrect'] += r.incorrect

    return jsonify(stats), 200