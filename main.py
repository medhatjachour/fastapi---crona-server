# change the limit to get manual pagination
# skip and obviously to skip the uer at the beginning 
# http://127.0.0.1:8000/staff/?skip=0&limit=100 
from sqlalchemy import inspect
import jwt
import datetime 
import shutil
from typing import List
import fastapi as _fastapi

from fastapi_server import schemas as _schemas
from fastapi_server import services as _services
import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()
_services.create_database()
JWT_SECRET = 'youWillNeverKnowTheSecret01|*8'
# oauth2_scheme = _fastapi.security.OAuth2PasswordBearer(tokenUrl='token')
# AUTHENTICATION ########################################
# @app.post('/token/' , response_model = _schemas.Staff )

# turn declarative_base to dict
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
# turn datetime to str --
def defaults(obj):
    keys = obj.keys()
    for i in keys:
        if type(obj[i]) == datetime.datetime:
            w = obj[i].strftime('%m/%d/%Y')
            d = {i:w}
            obj.update(d)
    return obj

# generate token by login
# @app.post('/token/', response_model = _schemas.Staff)
@app.post('/login/')
def generate_token(form_data: _fastapi.security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = _services.authenticate_user(form_data.username, form_data.password,db = db)
    # user:_schemas.Staff = _services.authenticate_user(form_data.username, form_data.password,db = db)
    # user: _schemas.Staff
    if not user:
        raise _fastapi.HTTPException(status_code = 400, detail="Invalid username or password")
    user = object_as_dict(user)
    user = defaults(user)
    token =  jwt.encode(user, JWT_SECRET)
    
    # token =  jwt.encode({'data': user.dict()}, JWT_SECRET , algorithm='HS256')
    return {'access_token' : token, 'token_type' : 'bearer'}

@app.post('/user/authenticated', response_model = _schemas.Staff)
def get_user(token: str = _fastapi.Depends(_fastapi.security.OAuth2PasswordBearer(tokenUrl = 'token')), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    try:
        print("We going to get the user")
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        print("We going to get the user")
        user: _schemas.Staff =  _services.get_staff(db = db , staff_id = payload.get('id')) 
    except:
        raise _fastapi.HTTPException( status_code= _fastapi.status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return user



#  STAFF ################################################
# response_model -- the data format for the response of the api not the request itself
@app.post('/staff/', response_model = _schemas.Staff)
def create_user(staff: _schemas.StaffCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_staff = _services.get_user_by_user_name(db = db , user_name = staff.user_name)
    if db_staff:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the username is already in use")
    return _services.create_staff(db = db , staff = staff)

@app.get("/staff/", response_model = List[_schemas.Staff])
def read_staffs( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    staffs = _services.get_staffs(db = db , skip = skip, limit = limit)
    return staffs

@app.get("/staff/{staff_id}", response_model = _schemas.Staff)
def read_staff(staff_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_staff = _services.get_staff(db = db , staff_id=staff_id)
    if db_staff is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the staff doesn't exist")  
    return db_staff

@app.delete("/staff/{staff_id}")
def delete_staff(staff_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_staff(db = db , staff_id = staff_id)
    return {"message" : f"successfully deleted staff with id {staff_id}"}
    # delete all records for the same staff

@app.put("/staff/{staff_id}", response_model = _schemas.Staff)
def read_staff(staff_id: int , staff:_schemas.StaffCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_staff = _services.update_staff(db = db , staff = staff , staff_id = staff_id)
    if db_staff is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the staff doesn't exist")  
    return db_staff


#  PATIENT ################################################


@app.post("/group/{group_id}/patients/", response_model=_schemas.PatientInGroup)
def create_patient_in_group(
    group_id:int , patient:_schemas.PatientCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    # db_patient = _services.get_staff(db = db , patient_id = group_id )
    db_patient_in_group = _services.get_group(db = db , group_id = group_id )
    db_patient_phone = _services.get_patient_by_phone(db = db , phone = patient.phone)    
    db_patient_email = _services.get_patient_by_email(db = db , email = patient.email)
    if db_patient_phone:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the phone is already in use")
    if db_patient_email:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the email is already in use")
    if db_patient_in_group is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the staff group exist")  
    return _services.create_patient_in_group(db = db, patient = patient, group_id = group_id)     

# @app.post('/patient/', response_model = _schemas.Patient)
# def create_patient(patient: _schemas.PatientCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
#     db_patient = _services.get_patient_by_email(db = db , email = patient.email)
#     if db_patient:
#         raise _fastapi.HTTPException(status_code = 400, detail="woops the email is already in use")
#     return _services.create_patient(db = db , patient = patient)

@app.get("/patient/", response_model = List[_schemas.Patient])
def read_patients( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    patients = _services.get_patients(db = db , skip = skip, limit = limit)
    return patients

@app.get("/patient/{patient_id}", response_model = _schemas.Patient)
def read_patient(patient_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_patient = _services.get_patient(db = db , patient_id=patient_id)
    if db_patient is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the patient doesn't exist")  
    return db_patient

@app.delete("/patient/{patient_id}")
def delete_patient(patient_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_patient(db = db , patient_id = patient_id)
    return {"message" : f"successfully deleted patient with id {patient_id}"}
    # delete all records for the same patient

@app.put("/patient/{patient_id}", response_model = _schemas.Patient)
def read_patient(patient_id: int , patient:_schemas.PatientCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_patient = _services.update_patient(db = db , patient = patient , patient_id = patient_id)
    if db_patient is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the patient doesn't exist")  
    return db_patient


#  DEVICE ################################################
@app.post('/device/', response_model = _schemas.DeviceFitch)
def create_device(device: _schemas.deviceCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_device = _services.get_device_by_name(db = db , name = device.name)
    if db_device:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the device is already exist with the name {name}")
    return _services.create_device(db = db , device = device)

@app.get("/device/", response_model = List[_schemas.DeviceFitch])
def read_devices( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    devices = _services.get_devices(db = db , skip = skip, limit = limit)
    return devices

@app.get("/device/{device_id}", response_model = _schemas.DeviceFitch)
def read_device(device_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_device = _services.get_device(db = db , device_id = device_id)
    if db_device is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the device doesn't exist")  
    return db_device

@app.delete("/device/{device_id}")
def delete_device(device_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_device(db = db , device_id = device_id)
    return {"message" : f"successfully deleted device with id {device_id}"}

@app.put("/device/{device_id}", response_model = _schemas.DeviceFitch)
def read_device(device_id: int , device:_schemas.deviceCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_device = _services.update_device(db = db , device = device , device_id = device_id)
    if db_device is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the device doesn't exist")  
    return db_device

#  RECORD ################################################


# @app.post("/staff/{staff_id}/records/", response_model=_schemas.RecordFitch)
# to Post A record i had 422 error so i divided it 2 endPoints one to create the record raw in db 
# and the the other point is to Put and upload the file to Venv and Put the file_name
@app.post("/staff/{staff_id}/records/")
def create_record(
    record:_schemas.RecordCreate,staff_id:int , patient_id:int , device_id:int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_staff = _services.get_staff(db = db , staff_id = staff_id)
    # # db_device = _services.get_staff(db = db , device_id = device_id )
    if db_staff is None:  
        raise _fastapi.HTTPException(status_code = 400, detail="woops the staff doesn't exist")  
    return _services.create_record(db = db, record = record, patient_id = patient_id, staff_id = staff_id , device_id = device_id)     
@app.put("/records/{record_id}/")
def upload_record(
     record_id:int,filee:_fastapi.UploadFile = _fastapi.File(...), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    # record:_schemas.RecordCreate,staff_id:int , patient_id:int , device_id:int, filee:_fastapi.UploadFile = _fastapi.File(...), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    # record:_schemas.RecordCreate,staff_id:int , patient_id:int , device_id:int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    with open(f'fastapi_server/records/{filee.filename}', 'wb') as buffer:
        # with open(f'src/main/python/wave/db/records/{filee.filename}', 'wb') as buffer:
        shutil.copyfileobj(filee.file, buffer)
    # db_record = _services.get_record(db = db , device_id = record_id )
    # if db_record is None:  
    #     raise _fastapi.HTTPException(status_code = 400, detail="woops the record")  
    # # we need to check if the record is deleted
    # return _services.create_record(db = db, record = record, patient_id = patient_id, staff_id = staff_id , device_id = device_id,file_name = str(file.filename))     
    return _services.upload_record(db = db, record_id = record_id, file_name = filee.filename)     
#  delete a record 
@app.put("/records/{record_id}", response_model = _schemas.RecordDeletedFitch)
def delete_record(record_id: int , user_deleted: int , record:_schemas.RecordDeletedCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_record = _services.update_record(db = db , record = record , record_id = record_id, user_deleted = user_deleted)
    db_staff = _services.get_staff(db = db , staff_id = user_deleted)
    if db_staff is None:  
        raise _fastapi.HTTPException(status_code = 400, detail="woops the staff doesn't exist")  
    if db_record is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the record doesn't exist")  
    return db_record
       
@app.get("/records/", response_model = List[_schemas.RecordFitch])
def read_records( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    records = _services.get_records(db = db , skip = skip, limit = limit)
    return records

@app.get("/records_active/", response_model = List[_schemas.RecordFitch])
def read_active_records( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    records = _services.get_records_active(db = db , skip = skip, limit = limit)
    return records

@app.get("/records_uploaded/", response_model = List[_schemas.RecordFitch])
def read_uploaded_records( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    records = _services.get_records_uploaded(db = db , skip = skip, limit = limit)
    return records

@app.get("/records_deleted/", response_model = List[_schemas.RecordFitch])
def read_deleted_records( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    records = _services.get_records_deleted(db = db , skip = skip, limit = limit)
    return records

@app.get("/record/{record_id}", response_model = _schemas.OneRecordFitch)
def read_one_record(record_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_record = _services.get_record(db = db , record_id = record_id)
    if db_record is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the record doesn't exist")  
    return db_record

# @app.delete("/records/{record_id}")
# def delete_record(record_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
#     _services.delete_record(db = db , record_id = record_id)
#     return {"message" : f"successfully deleted record with id {record_id}"}

     
# # upload file 
# @app.put("/records/{record_id}", response_model = _schemas.RecordDeletedFitch)
# def read_record(record_id: int , user_deleted: int , record:_schemas.RecordDeletedCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
#     db_record = _services.update_record(db = db , record = record , record_id = record_id, user_deleted = user_deleted)
#     if db_record is None:
#         raise _fastapi.HTTPException(status_code = 400, detail="woops the record doesn't exist")  
#     return db_record


#  GROUP ################################################

@app.post('/group/', response_model = _schemas.GroupFitch)
def create_group(group: _schemas.GroupCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_group = _services.get_group_by_name(db = db , name = group.name)
    if db_group:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the group is already exist with the name {name}")
    return _services.create_group(db = db , group = group)

@app.get("/group/", response_model = List[_schemas.GroupFitch])
def read_group( skip: int = 0, limit: int = 10,  db: _orm.Session = _fastapi.Depends(_services.get_db)): 
    groups = _services.get_groups(db = db , skip = skip, limit = limit)
    return groups

@app.get("/group/{group_id}", response_model = _schemas.GroupFitch)
def read_group(group_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_group = _services.get_group(db = db , group_id = group_id)
    if db_group is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the group doesn't exist")  
    return db_group

#  wait if i'm gonna delete all the patients in this group
# @app.delete("/group/{group_id}")
# def delete_group(group_id: int ,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
#     _services.delete_group(db = db , group_id = group_id)
#     return {"message" : f"successfully deleted device with id {group_id}"}

@app.put("/group/{group_id}", response_model = _schemas.GroupFitch)
def read_group(group_id: int , group:_schemas.GroupCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_group = _services.update_group(db = db , group = group , group_id = group_id)
    if db_group is None:
        raise _fastapi.HTTPException(status_code = 400, detail="woops the group doesn't exist")  
    return db_group
