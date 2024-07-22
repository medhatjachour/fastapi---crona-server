from passlib.hash import bcrypt
import datetime as _dt

import database as _database 
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
# authentication
# https://www.youtube.com/watch?v=6hTRw_HK3Ts
def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
#  add  more functions for every  one
# def verify_user(db:_orm.Session, password:str):
#     return bcrypt.verify(password, db.query)

# def verify_password(db: _orm.Session , password:str):
#     return bcrypt.verify(password ,_models.Staff.hash_password)
def authenticate_user(user_name: str, password: str, db: _orm.Session):
    user = db.query(_models.Staff).filter(_models.Staff.user_name == user_name).first()
    if not user :
        return False
    if not bcrypt.verify(password ,user.hash_password):
        return False
    return user 
    
#PATIENT
def get_patient_by_email(db: _orm.Session , email:str):
    return db.query(_models.Patient).filter(_models.Patient.email == email).first()
def get_patient_by_phone(db: _orm.Session , phone:str):
    return db.query(_models.Patient).filter(_models.Patient.phone == phone).first()

#STAFF
def get_user_by_user_name(db: _orm.Session , user_name:str):
    return db.query(_models.Staff).filter(_models.Staff.user_name == user_name).first()

#DEVICE
def get_device_by_name(db: _orm.Session , name:str):
    return db.query(_models.Device).filter(_models.Device.name == name).first()

#GROUP
def get_group_by_name(db: _orm.Session , name:str):
    return db.query(_models.Group).filter(_models.Group.name == name).first()


#  STAFF ################################################

def create_staff(db: _orm.Session , staff:_schemas.StaffCreate ):
    first_name = staff.first_name
    middle_name = staff.middle_name
    last_name = staff.last_name
    sex = staff.sex
    birth_date = staff.birth_date
    martial_status = staff.martial_status
    phone = staff.phone
    email = staff.email
    user_name = staff.user_name
    fake_hashed_pass =bcrypt.hash(staff.hash_password) 
    db_staff = _models.Staff(
        first_name = first_name,
        middle_name = middle_name,
        last_name = last_name,
        sex = sex,
        birth_date = birth_date,
        martial_status = martial_status,
        phone = phone,
        email = email,
        user_name = user_name,
        hash_password = fake_hashed_pass)
    
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def get_staffs(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.Staff).offset(skip).limit(limit).all()

def get_staff(db: _orm.Session, staff_id: int):
    return db.query(_models.Staff).filter(_models.Staff.id == staff_id).first()

def delete_staff(db: _orm.Session, staff_id:int):
    db.query(_models.Staff).filter(_models.Staff.id  == staff_id).delete()
    db.commit()

def update_staff(db: _orm.Session, staff : _schemas.StaffCreate , staff_id:int):
    db_staff = get_staff(db = db , staff_id = staff_id)

    db_staff.first_name = staff.first_name
    db_staff.middle_name = staff.middle_name
    db_staff.last_name = staff.last_name
    db_staff.sex = staff.sex
    db_staff.birth_date = staff.birth_date
    db_staff.martial_status = staff.martial_status
    db_staff.phone = staff.phone
    db_staff.email = staff.email
    # db_staff.address = staff.address
    # db_staff.date_created = staff.date_created
    # db_staff.is_user = staff.is_user
    # db_staff.role = staff.role
    db_staff.user_name = staff.user_name
    # db_staff.date_last_updated = staff.date_last_updated
    db_staff.date_last_updated = _dt.datetime.now()

    db.commit()
    db.refresh(db_staff)
    return db_staff

#  PATIENT ################################################

def create_patient_in_group(db: _orm.Session, patient: _schemas.PatientInGroup, group_id: int ):
    patient = _models.Patient(**patient.dict(),group_id = group_id,)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patients(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Patient).offset(skip).limit(limit).all()

def get_patient(db: _orm.Session, patient_id: int):
    return db.query(_models.Patient).filter(_models.Patient.id == patient_id).first()

def delete_patient(db: _orm.Session, patient_id:int):
    db.query(_models.Patient).filter(_models.Patient.id  == patient_id).delete()
    db.commit()

def update_patient(db: _orm.Session, patient : _schemas.PatientCreate , patient_id:int):
    db_patient = get_patient(db = db , patient_id = patient_id)

    db_patient.first_name = patient.first_name
    db_patient.middle_name = patient.middle_name
    db_patient.last_name = patient.last_name
    db_patient.sex = patient.sex
    db_patient.birth_date = patient.birth_date
    # db_patient.martial_status = patient.martial_status
    db_patient.phone = patient.phone
    db_patient.email = patient.email
    # db_patient.address = patient.address
    # db_patient.date_created = patient.date_created
    # db_patient.Complains = patient.Complains
    # db_patient.Diagnosis = patient.Diagnosis
    # db_patient.Treatment = patient.Treatment
    # db_patient.date_last_updated = patient.date_last_updated
    # db_patient.date_last_updated = _dt.datetime.now()

    db.commit()
    db.refresh(db_patient)
    return db_patient


#  DEVICE ################################################

def create_device(db: _orm.Session , device:_schemas.deviceCreate ):
    name = device.name
    description = device.description
    device_manufacture = device.device_manufacture
    manufacture_date = device.manufacture_date
    first_use = device.first_use
    # sensors = device.sensors
    db_device = _models.Device(
        name = name,
        description = description,
        device_manufacture = device_manufacture,
        manufacture_date = manufacture_date,
        first_use = first_use,
        # sensors = sensors
        )
    
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Device).offset(skip).limit(limit).all()

def get_device(db: _orm.Session, device_id: int):
    return db.query(_models.Device).filter(_models.Device.id == device_id).first()

def delete_device(db: _orm.Session, device_id:int):
    db.query(_models.Device).filter(_models.Device.id  == device_id).delete()
    db.commit()

def update_device(db: _orm.Session, device : _schemas.deviceCreate , device_id:int):
    db_device = get_device(db = db , device_id = device_id)
    # db_device.date_uploaded = device.date_uploaded
    db_device.name = device.name
    db_device.description = device.description
    db_device.device_manufacture = device.device_manufacture
    db_device.manufacture_date = device.manufacture_date
    db_device.first_use = device.first_use
    # db_device.sensors = device.sensors
    # db_device.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_device)
    return db_device

#  RECORD ################################################

# def create_record(db: _orm.Session, record: _schemas.RecordCreate, patient_id: int ,staff_id: int ,device_id:int, file_name:str):
    # not a valid dict start from here     
    # record = _models.Record(**record.dict(),patient_id = patient_id, staff_id = staff_id, device = device_id, file_name = file_name)
def create_record(db: _orm.Session, record: _schemas.RecordCreate, patient_id: int ,staff_id: int ,device_id:int):
    record = _models.Record(**record.dict(),patient_id = patient_id, staff_id = staff_id, device = device_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def upload_record(db: _orm.Session, record_id:int, file_name:str):
    db_record = get_record(db = db , record_id = record_id )
    db_record.file_name = file_name
    db_record.uploaded = True
    # db_record.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_record)
    return db_record

def get_records(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Record).offset(skip).limit(limit).all()

def get_records_active(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Record).filter(_models.Record.uploaded  == False and _models.Record.deleted  == False).all()

def get_records_uploaded(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Record).filter(_models.Record.uploaded  == True).all()

def get_records_deleted(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Record).filter(_models.Record.deleted  == True).all()

def get_record(db: _orm.Session, record_id:int):
    return db.query(_models.Record).filter(_models.Record.id  == record_id).first()

def delete_record(db: _orm.Session, record_id:int):
    db.query(_models.Record).filter(_models.Record.id  == record_id).delete()
    db.commit()

def update_record(db: _orm.Session, record : _schemas.RecordDeletedCreate , record_id:int,user_deleted:int):
    db_record = get_record(db = db , record_id = record_id )
    # db_record.date_uploaded = record.date_uploaded
    db_record.file_name = ""
    db_record.deleted = True
    db_record.date_deleted = record.date_deleted
    db_record.notes = record.notes
    db_record.user_deleted = user_deleted

    # db_record.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_record)
    return db_record


#  DEVICE ################################################

def create_group(db: _orm.Session , group:_schemas.GroupCreate ):
    name = group.name
    location = group.location
    db_group = _models.Group(
        name = name,    
        location = location,
        )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_groups(db: _orm.Session, skip:int, limit:int):
    return db.query(_models.Group).offset(skip).limit(limit).all()

def get_group(db: _orm.Session, group_id: int):
    return db.query(_models.Group).filter(_models.Group.id == group_id).first()

def delete_group(db: _orm.Session, group_id:int):
    db.query(_models.Group).filter(_models.Group.id  == group_id).delete()
    db.commit()

def update_group(db: _orm.Session, group : _schemas.GroupCreate , group_id:int):
    db_group = get_group(db = db , group_id = group_id)
    # db_group.date_uploaded = group.date_uploaded
    db_group.name = group.name
    db_group.location = group.location
    # db_group.date_last_updated = _dt.datetime.now()
    db.commit()
    db.refresh(db_group)
    return db_group
