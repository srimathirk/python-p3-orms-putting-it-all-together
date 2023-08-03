import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self,name,breed,id = None):
        self.id = id
        self.name = name
        self.breed = breed
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        dog = CURSOR.execute(sql)
        return dog

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
    
    def save(self):
        sql = """
            INSERT INTO dogs (name,breed)
            VALUES (?,?)
        """
        CURSOR.execute (sql,(self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        
    @classmethod
    def create(cls,name,breed):
        dog = cls(name,breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls,row):
        dog = cls(
            name= row[1],
            breed = row[2],
            id= row[0]
        )
        
        return dog
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        dogs = CURSOR.execute(sql).fetchall()
        cls.dogs = [cls.new_from_db(row)for row in dogs]
        return cls.dogs
    @classmethod
    def find_by_name(cls,name):
        sql = """
            SELECT * FROM dogs WHERE name = ?
        """
        dog = CURSOR.execute(sql,(name,)).fetchone()
        if not dog:
            return None
        print(dog)
        return cls(
            name = dog[1],
            breed = dog[2],
            id = dog[0] 
        )
    @classmethod
    def find_by_id(cls,id):
        sql = """
            SELECT * FROM dogs WHERE id = ?
        """
        dog = CURSOR.execute(sql,(id,)).fetchone()
        if not dog:
            return None
        print(dog)
        return cls(
            name = dog[1],
            breed = dog[2],
            id = dog[0] 
        )
    @classmethod
    def find_or_create_by(cls,name,breed):
        sql = """
            SELECT * FROM dogs WHERE name = ? and breed = ?
        """
        dog = CURSOR.execute(sql,(name,breed,)).fetchone()
        if not dog:
            new_dog = cls.create(name,breed)
            print(new_dog)
            return new_dog
        print(dog)
        return cls(
            name = dog[1],
            breed = dog[2],
            id = dog[0] 
        )
    def update(self):
        sql = """
            UPDATE dogs SET name = ? WHERE id = ?
        """
        CURSOR.execute(sql,(self.name,self.id))
        CONN.commit()

#Dog.drop_table()
#Dog.create_table()
#puppy = Dog("Pup","mixd")
#puppy.save()
puppy = Dog.create("Hello","gg")
#print(puppy)
#puppy = Dog.get_all()
#print(puppy)
# puppy = Dog.find_by_name("Hello")
# print(puppy)
puppy = Dog.find_by_id(2)
puppy.update()
print(puppy)



