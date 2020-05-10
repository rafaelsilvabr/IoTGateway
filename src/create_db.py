import peewee

db=peewee.SqliteDatabase('ids.db')

class BaseModel(peewee.Model):
	class Meta:
		database=db

class Sensors(BaseModel):
	localid=peewee.CharField(unique=True)
	uuid=peewee.CharField(unique=True)
	capabilities=peewee.TextField(unique=True)

if __name__=='__main__':
	try:
		Sensors.create_table()
		print("Tabela 'Sensors' criada!")
	except peewee.OperationError:
		print("Tabela 'Sensors' ja existe!")

