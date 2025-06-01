from app import create_app, db 
from app.models import Subject 

app = create_app()

with app.app_context():
    subjects = ['Português', 'Matemática', 'História', 'Geografia', 'Fisica', 'Quimica'
                , 'Biologia', 'Lingua Estrangeira', 'Sociologia', 'Filosofia', 'Redação']
    for name in subjects: 
        if not Subject.query.filter_by(name=name).first():
            db.session.add(Subject(name-name))
        db.session.commit()
    print("Matéria(s) adicionadas com sucesso!")
