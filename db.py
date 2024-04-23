import sqlite3
from typing import Any

#TODO Dokoncit tabulku zoo, pridat dalsie atributy pre zvieratko 
# TODO Moznost vybrat chovatelov, kazdy chovatel ma svoju tabulku o ktore zvieratka sa stará a rozpis kedy robi

class Caregiver:
    def __init__(self, data) -> None:
        if data:
            self.id = data[0]
            self.name = data[1]
            self.shift_days = data[2]
            self.shift_times = data[3]

class Cages:
    def __init__(self, data) -> None:
        if data:
            self.id = data[0]
            self.name = data[1]
            self.cleaning_days = data[2]
            self.cleaning_time = data[3]
        


class AnimalEntity:
    def __init__(self, data=None) -> None:
        if data:
            self.id = data[0]
            self.name = data[1]
            self.specie = data[2]
            self.origin_country = data[3]
            self.birth_date = data[4]
            self.food = data[5]
            self.feeding_time = data[6]
            self.last_cleaning = data[7]
            self.caregiver_key = data[8]
            self.cage_key = data[9]

    def __getattribute__(self, name: str) -> Any:
        return object.__getattribute__(self, name)

    def modify(self, reqForm, animal_id):
        self.name = reqForm["animalName"]
        self.specie = reqForm["species"]
        self.origin_country = reqForm["origin_country"]
        self.birth_date = reqForm["birth_date"]
        self.food = reqForm["food"]
        self.feeding_time = reqForm["feeding_time"]
        self.last_cleaning = reqForm["last_cleaning"]
        self.cage_key = reqForm["cage_key"]
        self.caregiver_key = reqForm["caregiver_key"]
        self.id = animal_id

class DB:
    def __init__(self) -> None:
        self.con = sqlite3.connect("animals.db")
        self.cur = self.con.cursor()
        self.initTable()
        
    def initTable(self):
        self.cur.execute(open("zoo_schema.sql").read())
        self.cur.execute(open("cages_schema.sql").read())
        self.cur.execute(open("caregivers_schema.sql").read())

    # Caregivers
    def get_caregivers(self) -> list[Caregiver]:
        tuples = self.cur.execute("SELECT * FROM caregivers").fetchall()
        res = [Caregiver(caregiver) for caregiver in tuples]
        return res
    
    def add_caregiver(self, data):
        self.cur.execute("INSERT INTO caregivers (name, shift_days, shift_times) VALUES(?, ?, ?)", data)
        self.con.commit()

    # Animals
    def add_animal(self, data):
        self.cur.execute("INSERT INTO zoo (name, spiece, origin_country, birth_date, food, feeding_time, last_cleaning, caregiver_key, cage_key) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        self.con.commit()


    def get_animals(self, searchText=None) -> list[AnimalEntity]:
        query = '''SELECT 
                zoo.key,
                zoo.name, 
                spiece, 
                origin_country, 
                birth_date,
                food,
                feeding_time,
                last_cleaning,
                c.name,
                cages.name 
                FROM zoo, caregivers c, cages
                WHERE zoo.caregiver_key = c.key AND zoo.cage_key = cages.key 
                '''
        if searchText is not None:
            query += "AND (zoo.name = ? OR spiece = ? OR origin_country = ? OR birth_date = ? OR food = ? OR feeding_time = ? OR last_cleaning = ? OR c.name = ? OR cages.name = ?)"
            tuples = self.cur.execute(query, [searchText]*9).fetchall()
        else:
            tuples = self.cur.execute(query).fetchall()
        res = [AnimalEntity(animal) for animal in tuples]
        return res
    
    def pick_animal(self, id) -> AnimalEntity:
        picked = self.cur.execute("SELECT * FROM zoo WHERE zoo.key = ?", [id]).fetchone()
        if picked is None:
            raise Exception(f"Animal with {id} does not exists")
        else:
            return AnimalEntity(picked)
        
    def update_animal(self, animal: AnimalEntity) -> None:
        self.cur.execute(f'''UPDATE zoo 
                         SET name = "{animal.name}", spiece = "{animal.specie}", origin_country = "{animal.origin_country}",
                         birth_date = "{animal.birth_date}", food = "{animal.food}", feeding_time = "{animal.feeding_time}",
                         last_cleaning = "{animal.last_cleaning}", caregiver_key = "{animal.caregiver_key}", cage_key = "{animal.cage_key}" 
                         WHERE key = {animal.id}''')
        self.con.commit()

    def delete_animal(self, animal_id):
        self.cur.execute(f"DELETE FROM zoo WHERE key = {animal_id}")
        self.con.commit()

    # Cages
    def get_cages(self) -> list[Cages]:
        tuples = self.cur.execute("SELECT * FROM cages").fetchall()
        res = [Cages(cage) for cage in tuples]
        return res
    
    def add_cage(self, data):
        self.cur.execute("INSERT INTO cages (name, cleaning_days, cleaning_time) VALUES(?, ?, ?)", data)
        self.con.commit()
    
    def close(self):
        self.con.close()

