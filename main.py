from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask('Company Management')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(300), nullable=False)
    work_duration = db.Column(db.Integer) 
    is_current = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'Company {self.id}. {self.company_name} - {self.work_duration} months'

@app.route('/')
def main():
    companies = Company.query.all()
    return render_template('index.html', companies_list=companies)

@app.route('/clear', methods=['DELETE'])
def clear_companies():
    try:
        db.session.query(Company).delete()
        db.session.commit()
        return 'OK', 200
    except Exception as e:
        db.session.rollback()
        return str(e), 500

@app.route('/current/<company_id>', methods=['PATCH'])
def modify_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    company.is_current = request.json['is_current']
    db.session.commit()
    return 'OK', 200

@app.route('/add', methods=['POST'])
def add_company():
    data = request.json
    company = Company(
        company_name=data['company_name'],
        work_duration=data['work_duration'],
        is_current=data.get('is_current', True)
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({'id': company.id}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
