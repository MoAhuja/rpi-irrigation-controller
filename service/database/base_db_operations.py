from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from service.database.db_schema import Base
# from service.utilities.logger import Logger

class BaseDBOperations():

    session = None
    def _fk_pragma_on_connect2(self,dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')

    def initialize(self):
        
        if self.session is None:

            engine = create_engine('sqlite:///sqlalchemy_example.db?check_same_thread=False')
            event.listen(engine, 'connect', self._fk_pragma_on_connect2)

            # Bind the engine to the metadata of the Base class so that the
            # declaratives can be accessed through a DBSession instance
            Base.metadata.bind = engine
            
            DBSession = sessionmaker(bind=engine, autoflush=False)
            # A DBSession() instance establishes all conversations with the database
            # and represents a "staging zone" for all the objects loaded into the
            # database session object. Any change made against the objects in the
            # session won't be persisted into the database until you call
            # session.commit(). If you're not happy about the changes, you can
            # revert all of them back to the last commit by calling
            # session.rollback()
            self.session= DBSession()
        
        
    def saveAndClose(self):
        result = False
        try:
            self.session.commit()
            result = True
        except:
            # shared.logger.error(self, "An error occured writing to DB")
            self.session.rollback()
        finally:
            self.session.close()
        
        return result
    
    def undo(self):
        self.session.rollback()
    