# coding=utf-8
class dbrouter(object):
    """A router to control all database operations on models in
    the case application"""

    def db_for_read(self, model, **hints):
        "Point all operations on case models to 'case'"
        if model._meta.app_label == 'case':
            return 'case'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on case models to 'case'"
        if model._meta.app_label == 'case':
            return 'case'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in case is involved"
        if obj1._meta.app_label == 'project' or obj2._meta.app_label == 'case':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the case app only appears on the 'case' db"
        if db == 'csystem':
            return model._meta.app_label == 'case'
        elif model._meta.app_label == 'case':
            return False
        return None

class MasterSlaveRouter(object):
    """A router that sets up a simple master/slave configuration"""

    def db_for_read(self, model, **hints):
        "Point all read operations to a random slave"
        return random.choice(['slave1','slave2'])

    def db_for_write(self, model, **hints):
        "Point all write operations to the master"
        return 'master'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation between two objects in the db pool"
        db_list = ('master','slave1','slave2')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_syncdb(self, db, model):
        "Explicitly put all models on all databases."
        return True