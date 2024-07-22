# Medical Device Backend
This repository contains the backend for handling patient records on a medical device. It is built using FastAPI, SQLAlchemy, and SQLite.

## Features
- CRUD operations (Create, Read, Update, Delete) for patient records
- Authentication using JWT
- Relational database schema

![alt text](https://github.com/medhatjachour/fastapi---crona-server/blob/main/digrams/d1.png?raw=true)
![alt text](https://github.com/medhatjachour/fastapi---crona-server/blob/main/digrams/d2.png?raw=true)
![alt text](https://github.com/medhatjachour/fastapi---crona-server/blob/main/digrams/d3.png?raw=true)
![alt text](https://github.com/medhatjachour/fastapi---crona-server/blob/main/digrams/dd.png?raw=true)
## Installation
1. Clone the repository:
```bash
    git clone https://github.com/medhatjachour/fastapi---crona-server.git
    cd fastapi---crona-server
```

2. Create a virtual environment and activate it:
```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
```

3. Install the dependencies:
```bash
    pip install -r requirements.txt
```

## Usage

1. Start the FastAPI server:
```bash
    uvicorn main:app --reload
```

2. Access the API documentation at `http://127.0.0.1:8000/docs`.
if the socket 8000 is unavailable  use 
```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
```
2. Access the API documentation at `http://127.0.0.1:8080/docs`.
## Contributing

Contributions are welcome! If you’d like to contribute to this project, just contact me

## License
This project is licensed under the MIT License. See the LICENSE file for details.
[MIT](https://choosealicense.com/licenses/mit/)