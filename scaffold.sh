export $(cat .env | xargs)
sqlacodegen $DATABASE_URL > orm/entities/entities.py