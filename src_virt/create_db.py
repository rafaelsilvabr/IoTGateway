import peewee

db=peewee.SqliteDatabase('ids.db')

class BaseModel(peewee.Model):
	class Meta:
		database=db

class Sensors(BaseModel):
	localid = peewee.CharField(unique=True)
	uuid = peewee.CharField(unique=True)
	lastdata = peewee.CharField(unique=False)

class VirtualSensor(BaseModel):
	localid = peewee.CharField(unique=True)
	uuid = peewee.CharField(unique=True)
	sensor01 = peewee.CharField(unique=True)
	sensor02 = peewee.CharField(unique=True)

if __name__=='__main__':
	try:
		Sensors.create_table()
		VirtualSensor.create_table()
		print("Tabela 'Sensors' criada!")
	except peewee.OperationError:
		print("Tabela 'Sensors' ja existe!")

