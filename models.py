import datetime as _dt

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship

from database import Base


class Patient(Base):
    __tablename__ = "patients"
    
    # min att
    id = Column(Integer, primary_key=True, index=True)
    
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    
    birth_date = Column(Date)

    # additional 
    sex = Column(String, default="Man")
    phone = Column(String, unique=True,)
    email = Column(String, unique=True, index=True)

    group_id = Column(Integer, ForeignKey("groups.id"))
    patient_group = relationship("Group", back_populates="patients")
    records = relationship("Record", back_populates="patient_record") 

class Staff(Base):
    __tablename__ = "staffs"

    id = Column(Integer, primary_key=True, index=True)
    
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    sex = Column(String, default="Man")
    birth_date = Column(DateTime)
    martial_status = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    
    user_name = Column(String, unique=True)
    hash_password = Column(String)

    records = relationship("Record", back_populates="staff_record") 
    # recordsDeleted = relationship("Record", back_populates="staff_record_deleted") 

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    device_manufacture = Column(String)
    manufacture_date = Column(DateTime)
    first_use = Column(DateTime)
    records = relationship("Record", back_populates="device_record") 

class Record(Base):
    __tablename__ = "records"
    # we gonna need to modify that to match the schema
    id = Column(Integer, primary_key=True, index=True)
    date_recorded = Column(DateTime, default=_dt.datetime.utcnow)
    date_uploaded = Column(DateTime, default=_dt.datetime.utcnow)
    # file_name = Column(String, index=True)
    file_name = Column(String, nullable = True)

    uploaded = Column(Boolean, default = False)
    
    deleted = Column(Boolean, default = False)
    date_deleted = Column(DateTime, default=_dt.datetime.utcnow)
    notes = Column(String)

    user_deleted = Column(Integer,nullable = True)
    # user_deleted = Column(Integer, ForeignKey("staffs.id"),nullable = True)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    device = Column(Integer, ForeignKey("devices.id"))

    # staff_record_deleted = relationship("Staff",back_populates="recordsDeleted")
    
    patient_record = relationship("Patient",back_populates="records")
    staff_record = relationship("Staff",back_populates="records")
    device_record = relationship("Device",back_populates="records")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    location = Column(String)

    patients = relationship("Patient", backref="groups" ) 
    # patients = relationship("Patient", backref="groups" ,overlaps="patient_group") 