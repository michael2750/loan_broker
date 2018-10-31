from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import text
from sqlalchemy.pool import Pool, NullPool
import json

DATABASE_CONNECTION = {
    'drivername': 'postgres',
    'port': '5432',
    'username': 'prod',
    'database': 'prod',
}

"""
Makes an engine to the database
"""
def make_engine():
    engine = create_engine(URL(**DATABASE_CONNECTION), poolclass=NullPool)
    return engine.connect()

def sqlalchemy_json(dictionary):
    return json.dumps([dict(r) for r in dictionary],default=str)

def insert_request(request_ssn, request_loan_amount, request_loan_duration):
	sql_statement = """
		INSERT INTO
			requests(
				ssn,
				loanAmount,
				loanDuration
				)
			VALUES(
				:request_ssn,
				:request_loan_amount,
				:request_loan_duration
			)
			RETURNING id
	"""
	con = make_engine()
	request_id = con.execute(text(sql_statement), request_ssn=request_ssn, request_loan_amount=request_loan_amount, request_loan_duration=request_loan_duration)
	con.close()
	value = None
	for row in request_id:
		value = row[0]
	return value

def select_result(request_id):
	sql_statement = """
		SELECT
			interest,
			ssn
		FROM
			requests
		WHERE
			id = :request_id
	"""
	con = make_engine()
	result = con.execute(text(sql_statement), request_id=request_id)
	con.close()
	sql_dict = None
	for row in result:
		sql_dict = dict(row)
	return sql_dict