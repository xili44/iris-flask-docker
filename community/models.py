from dataclasses import dataclass
from typing import List
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
db = SQLAlchemy()

@dataclass
class Comment(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    content:str = db.Column(db.Text)
    post_id:int = db.Column(db.Integer, db.ForeignKey('post.id'))

@dataclass
class Post(db.Model):
    __allow_unmapped__ = True
    id:int = db.Column(db.Integer, primary_key=True)
    title:str = db.Column(db.String(100))
    content:str = db.Column(db.Text)
    comments:List[Comment] = db.relationship('Comment', backref='post')

@dataclass
class Patient(db.Model):
    PatientId:int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name:str = db.Column(db.String(100))
    Title:str = db.Column(db.String(20))
    Gender:str = db.Column(db.String(10))
    DOB:str = db.Column(db.Date)
    Ethnicity:str = db.Column(db.String(100))
    HN:str = db.Column(db.String(10))
    
def load_csv(file_path):
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                dob = datetime.strptime(row['DOB'], '%d/%m/%Y').date()
                new_patient = Patient(
                    Name=row['Name'],
                    Title=row['Title'],
                    Gender=row['Gender'],
                    DOB=dob,
                    Ethnicity=row['Ethnicity'],
                    HN=row['HN']
                )
                db.session.add(new_patient)
            db.session.commit()
    except Exception as e:
        return f"Error: {str(e)}"

def init_db(app):
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create fake data
        path = '/irisdev/app/community/static/PatientData.csv'
        load_csv(path)
        
        post1 = Post(title='Post The First', content='Content for the first post')
        post2 = Post(title='Post The Second', content='Content for the Second post')
        post3 = Post(title='Post The Third', content='Content for the third post')

        comment1 = Comment(content='Comment for the first post', post=post1)
        comment2 = Comment(content='Comment for the second post', post=post2)
        comment3 = Comment(content='Another comment for the second post', post=post2)
        comment4 = Comment(content='Another comment for the first post', post=post1)

        db.session.add_all([post1, post2, post3])
        db.session.add_all([comment1, comment2, comment3, comment4])
        db.session.commit()

    return db    