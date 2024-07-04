
from flask import Flask, jsonify, request, Response
from models import Comment, Post, Patient, init_db
from grongier.pex import Director

import iris
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'iris+emb://IRISAPP'

db = init_db(app)

######################
# IRIS Query example #
######################

@app.route('/iris', methods=['GET'])
def iris_query():
    query = "SELECT top 10 * FROM %Dictionary.ClassDefinition"
    rs = iris.sql.exec(query)
    # Convert the result to a list of dictionaries
    result = []
    for row in rs:
        result.append(row)
    return jsonify(result)

########################
# IRIS interop example #
########################
bs = Director.create_python_business_service('BS')

@app.route('/interop', methods=['GET', 'POST', 'PUT', 'DELETE'])
def interop():
    
    rsp = bs.on_process_input(request)

    return jsonify(rsp)


############################
# CRUD operations comments #
############################

@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify(comments)

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    comment = Comment(content=data['content'], post_id=data['post_id'])
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment)

@app.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get(id)
    return jsonify(comment)

@app.route('/comments/<int:id>', methods=['PUT'])
def update_comment(id):
    comment = Comment.query.get(id)
    data = request.get_json()
    comment.content = data['content']
    db.session.commit()
    return jsonify(comment)

@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify(comment)

############################
# CRUD operations posts    #
############################

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify(posts)

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = Post(title=data['title'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify(post)

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get(id)
    return jsonify(post)

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify(post)

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify(post)

############################
# CRUD operations patients    #
############################

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify(patients), 200

@app.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify(patient), 200
  
@app.route('/patients/<int:id>', methods=['PUT'])  
def update_patient(id):
    try:
        patient:Patient = Patient.query.get_or_404(id)
        data = request.get_json()
        patient.Name = data['Name']
        db.session.commit()
        return jsonify(patient),200
    except Exception as e:
        return Response(e, status=400)

@app.route('/patients', methods=['POST'])
def create_patient():
    try:
        data = request.get_json()
        dob = datetime.strptime(data['DOB'], '%Y-%m-%d').date()
        patient = Patient(Name=data['Name'], Title=data['Title'], Gender=data['Gender'], DOB=dob ,Ethnicity=data['Ethnicity'], HN=data['HN'])
        db.session.add(patient)
        db.session.commit()
        return jsonify(patient),201
    except Exception as e:
        return Response(e, status=400)
@app.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return Response(status=200)

if __name__ == "__main__":
    app.run(debug=True)