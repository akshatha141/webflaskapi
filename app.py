
from flask_marshmallow import Marshmallow
from flask import Flask, render_template,redirect,request,url_for,jsonify,Request

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import query


app = Flask(__name__)  # creating the Flask class object
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test6.db'
db=SQLAlchemy(app)
ma=Marshmallow(app)

class TodoSchema(ma.Schema):
    class Meta:
        fields=('id','content','date_created')
        
todo_schema=TodoSchema()
todos_schema=TodoSchema(many='True')  
    
class Todo(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
def __repr__(self):
    return f'<Task  {self.content} >'    
      
@app.route('/' , methods=['POST','GET'])  
def index():
    if request.method == 'POST':
        task_content = request.json['content']
        new_task =Todo(content=task_content)
              
        try:
            db.session.add(new_task)
            db.session.commit()
            return todo_schema.jsonify(new_task)
        except:
            return jsonify({'content':'Data not inserted into database'})
    else:
        tasks =Todo.query.all()        
        return todos_schema.jsonify(tasks)
            
@app.route('/<int:id>',methods=['GET'])
def get_task(id):
    task=Todo.query.get_or_404(id)
    return todo_schema.jsonify(task)

@app.route('/<int:id>',methods=['DELETE'])
def delete_task(id):
    delete_msg={"message":"The task is deleted Successfully"}
    task=Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(delete_msg)
                                                                
if __name__ == '__main__':
    app.run(debug=True)






