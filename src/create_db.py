import peewee

db=peewee.SqliteDatabase('ids.db')

class BaseModel(peewee.Model):
	class Meta:
		database=db

class Sensors(BaseModel):
	localid=peewee.CharField(unique=True)
	uuid=peewee.CharField(unique=True)

class Virtualizers(BaseModel):
	uuid=peewee.CharField(default=None)
	addr=peewee.CharField(default=None)

if __name__=='__main__':
	try:
		db.create_tables([
			Sensors,
			Virtualizers
		])
		print("Tabela 'Sensors' criada!")
	except:
		print("Tabela 'Sensors' ja existe!")

