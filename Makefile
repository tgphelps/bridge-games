
check:
	-flake8
	mypy *.py

sql:
	sqlite3 deals.db

create-db:
	-rm deals.db
	sqlite3 deals.db <create-db.sql

db.dump: deals.db
	sqlite3 deals.db .dump >db.dump