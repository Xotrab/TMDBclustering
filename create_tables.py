from database_facade import DatabaseFacade

database_facade = DatabaseFacade()

print('CREATING TABLES >>>>')
database_facade.create_tables()

print('FINISHED >>>>')