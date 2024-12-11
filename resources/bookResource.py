from flask_restful import Resource
from flask import request
import json
import pymysql

# Establish a connection to the MySQL server
conn = pymysql.connect(
    host='localhost',  # Hostname where the MySQL server is running (usually localhost)
    user='root',  # Your MySQL username
    password='pass@word1',  # Your MySQL password
    database='housing',  # The database you want to connect to
    port=3306  # Port number (default MySQL port is 3306)
)
cursor = conn.cursor()


# GET all houses (Fetch data from MySQL)
class HousesGETResource(Resource):
    def get(self):
        # SQL query to select all houses
        query = "SELECT * FROM house1"
        cursor.execute(query)
        rows = cursor.fetchall()
        houses = []

        for row in rows:
            # Assuming columns: id, SalePrice, OverAllQual, TotalBsmtSF, GrLivArea, BsmtFullBath, GarageCars, YearBuilt, MasVnrArea
            house = {
                "id": row[0],
                "SalePrice": row[1],
                "OverAllQual": row[2],
                "TotalBsmtSF": row[3],
                "GrLivArea": row[4],
                "BsmtFullBath": row[5],
                "GarageCars": row[6],
                "YearBuilt": row[7],
                "MasVnrArea": row[8]
            }
            houses.append(house)
        return houses


# GET a single house by ID (Fetch data from MySQL)
class HouseGETResource(Resource):
    def get(self, id):
        # SQL query to select a house by id
        query = "SELECT * FROM house1 WHERE id = %s"
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if row:
            house = {
                "id": row[0],
                "SalePrice": row[1],
                "OverAllQual": row[2],
                "TotalBsmtSF": row[3],
                "GrLivArea": row[4],
                "BsmtFullBath": row[5],
                "GarageCars": row[6],
                "YearBuilt": row[7],
                "MasVnrArea": row[8]
            }
            return house
        return {"message": "House not found"}, 404


# POST a new house (Insert into MySQL)
class HousePOSTResource(Resource):
    def post(self):
        house = json.loads(request.data)
        try:
            # SQL query to insert a new house
            insert_query = """
            INSERT INTO house1 (SalePrice, OverAllQual, TotalBsmtSF, GrLivArea, BsmtFullBath, GarageCars, YearBuilt, MasVnrArea)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                house["SalePrice"], house["OverAllQual"], house["TotalBsmtSF"], house["GrLivArea"],
                house["BsmtFullBath"], house["GarageCars"], house["YearBuilt"], house["MasVnrArea"]
            ))

            # Commit the transaction (important to save the data in MySQL)
            conn.commit()
            print("Data inserted successfully!")

            # Get the inserted ID
            house["id"] = cursor.lastrowid  # Get the auto-generated ID
            return house, 201
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return {"error": str(e)}, 500


# PUT (update) a house by ID (Update in MySQL)
class HousePUTResource(Resource):
    def put(self, id):
        house = json.loads(request.data)
        try:
            # SQL query to update house details by ID
            update_query = """
            UPDATE house1
            SET SalePrice = %s, OverAllQual = %s, TotalBsmtSF = %s, GrLivArea = %s, BsmtFullBath = %s,
                GarageCars = %s, YearBuilt = %s, MasVnrArea = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (
                house["SalePrice"], house["OverAllQual"], house["TotalBsmtSF"], house["GrLivArea"],
                house["BsmtFullBath"], house["GarageCars"], house["YearBuilt"], house["MasVnrArea"], id
            ))

            # Commit the transaction (important to save the data in MySQL)
            conn.commit()
            if cursor.rowcount > 0:
                return house
            return {"message": "House not found to update"}, 404
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return {"error": str(e)}, 500


# DELETE a house by ID (Delete from MySQL)
class HouseDELETEResource(Resource):
    def delete(self, id):
        try:
            # SQL query to delete a house by ID
            delete_query = "DELETE FROM house1 WHERE id = %s"
            cursor.execute(delete_query, (id,))
            conn.commit()
            if cursor.rowcount > 0:
                return {"message": "House deleted successfully"}, 200
            return {"message": "House not found"}, 404
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            return {"error": str(e)}, 500
