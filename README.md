
#Address Management:

This API provides endpoints to manage addresses, including creating, reading, updating, and deleting addresses. It also supports finding nearby addresses within a certain distance of given coordinates.

Features:

  1. Create Address: Add a new address to the database.
  2. Read Address: Get details of a specific address by its ID.
  3. List Addresses: Get a list of addresses with pagination support.
  4. Delete Address: Delete an address by its ID.
  5. Find Nearby Addresses: Find addresses within a certain distance of given coordinates.

  
Technologies Used:

   1. FastAPI: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
   2. SQLAlchemy: SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
   3. Pydantic: Pydantic is a data validation and settings management using Python type hinting.
   4. Geopy: Geopy makes it easy to locate the coordinates of addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources


Installation:
    1. Clone this repository:
            https://github.com/sithihalitha/fastapi_assessment.git
    2. Install dependencies:
            pip install -r requirements.txt

Usage:
    1. Run the FastAPI server:
            uvicorn main:app --reload
      This will start the server at http://localhost:8000.



Contributing
Feel free to contribute to this project. Fork the repository, make your changes, and submit a pull request.
