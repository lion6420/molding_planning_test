from . import app, db
from flask import request
from .models import PlanningResult, Emergency, WeeklyDemand
import json

@app.route('/')
def index():
  return 'Hello World'

@app.route('/planningresult', methods=['GET'])
def get_result():
  data = PlanningResult.query.filter(PlanningResult.start_time.between('2020-01-11', '2020-01-12'))
  result = []
  for d in data:
    d_dic = d.as_dict()
    result.append(d_dic)
  return json.dumps(result, default=str)

@app.route('/weekly', methods=['POST'])
def get_weeklydemand():
  data = request.get_json()
  data_start = (data['page']-1)*data['size']
  data = WeeklyDemand.query.limit(data['size']).offset(data_start).all()
  rows = WeeklyDemand.query.count()
  result = []
  for d in data:
    d_dic = d.as_dict()
    result.append(d_dic)
  result_json = {
    'data': result,
    'rows': rows
  }
  return result_json

@app.route('/weekly', methods=['PUT'])
def update_weeklydemand(id):
  data = WeeklyDemand.query.filter_by(id=id).first()
  if data.priority == 0:
    data.priority = 1
  else:
    data.priority = 0
  db.session.commit()
  return

@app.route('/emergency', methods=['GET'])
def get_emergency():
  data = Emergency.query.all()
  result = []
  for d in data:
    d_dic = d.as_dict()
    result.append(d_dic)
  return json.dumps(result)

@app.route('/emergency')
@app.route('/emergency/adjust', methods=['DELETE', 'POST'])
def adjust_emergency():
  if request.method == 'DELETE':
    result = db.session.query(Emergency).delete()
    db.session.commit()
  elif request.method == 'POST':
    data = json.loads(request.data)
    for dic in data:
      data_tuplelist = tuple(dic.values())
      newEmergency = Emergency(data_tuplelist[1],data_tuplelist[2], data_tuplelist[3], data_tuplelist[4], data_tuplelist[5], \
                               data_tuplelist[6], data_tuplelist[7], data_tuplelist[8], data_tuplelist[9], data_tuplelist[10])
      db.session.add(newEmergency)
    db.session.commit()
  return 'succeeded'

