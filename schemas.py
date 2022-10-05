from tokenize import group
from typing import List, Union
from datetime import datetime ,date
import pydantic as _pydantic


class _Record(_pydantic.BaseModel):
    date_recorded: datetime
    date_uploaded: Union[datetime, None] = None
    # date_deleted: Union[datetime, None] = None
    # file_name: str
class RecordCreate(_Record):
    pass
    file_name:Union[str , None] = None
    # file_name: str

class RecordFitch(_Record):
    id:int
    
    patient_id:int
    staff_id:int
    device:int
    uploaded:bool
    deleted:bool


    class Config:
        orm_mode = True
class OneRecordFitch(_Record):
    id:int
    
    patient_id:int
    staff_id:int
    device:int
    file_name: str

    class Config:
        orm_mode = True       

class RecordDeletedCreate(_pydantic.BaseModel):
    # user_deleted:int
    # deleted:bool
    date_deleted:datetime
    notes:str
    class Config:
        orm_mode = True
class RecordDeletedFitch(_Record):
    user_deleted:int
    deleted:bool
    date_deleted:datetime
    notes:str
    class Config:
        orm_mode = True

class _User(_pydantic.BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    sex: str
    # birth_date: datetime
    phone: str
    email: str

# print(datetime.now().date())
class PatientCreate(_User):
    birth_date: date
class Patient(_User):
    id: int
    birth_date: date
    records: List [RecordFitch] = [] # the class i'm gonna build
    group_id: int
    # group_id: Union[int, None] = None
    class Config:
        orm_mode = True

class PatientInGroup(_User):
    id: int
    birth_date: date
    group_id: Union[int , None] = None
    records: List [RecordFitch] = [] # the class i'm gonna build
    class Config:
        orm_mode = True

class StaffCreate(_User):
    birth_date: datetime
    martial_status: str
    user_name: str
    hash_password: str
    
    class Config:
        orm_mode = True
class Staff(_User):
    id: int
    user_name: str
    records: List [RecordFitch] = [] #  List [RecordFitch] = []   Union[List [RecordFitch] , None] = None  # the class i'm gonna build
    class Config:
        orm_mode = True

class _Device(_pydantic.BaseModel):
    name: str
    description: Union[str, None] = None
class deviceCreate(_Device):
    device_manufacture : Union[str , None] = None
    manufacture_date: datetime
    first_use: datetime
    # sensors:List[str] = []
class DeviceFitch(_Device):
    id:int
    manufacture_date: datetime
    first_use: Union[datetime, None] = None
    # sensors:List[str] = []
    records: List [RecordFitch] = [] # the class i'm gonna build
    class Config:
        orm_mode = True


class _Group(_pydantic.BaseModel):
    name: str
    location: Union[str, None] = None
class GroupCreate(_Group):
    pass
class GroupFitch(_Group):
    id:int
    name: str
    location: Union[str, None] = None
    patients: List [Patient] = [] # the class i'm gonna build
    class Config:
        orm_mode = True

