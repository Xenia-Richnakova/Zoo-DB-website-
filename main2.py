from db import DB, AnimalEntity, Caregiver, Cages
from flask import Flask, request, g, make_response, redirect, url_for
from design import Design


class App:
    
    def __init__(self) -> None:
        self.app = Flask(__name__)

        def get_db():
            db = getattr(g, '_database', None)
            if db is None:
                db = g._database = DB()
            return db
        
        @self.app.route("/")
        def hello_world():
            caregiversTable = get_db().get_caregivers()
            cagesTable = get_db().get_cages()
            htmlComboBoxes = Design()
            caregivers, cages = htmlComboBoxes.cages_and_caregivers(cagesTable, caregiversTable)
            with open("html/index.html", "r") as index:
                html = index.read()
            html = html.replace('<!--$caregiver_key-->', caregivers)
            html = html.replace('<!--$cages Options-->', cages)
            return html

        @self.app.route("/add_animal", methods = ['POST'])
        def add_animal():
            f = request.form
            get_db().add_animal((f["animalName"], f["species"], f["origin_country"], f["birth_date"], f["food"], f["feeding_time"], f["last_cleaning"], f["caregiver_key"], f["cage_key"]))
            response = make_response("")
            response.headers["HX-Trigger"] = "add_animal"
            response.headers["HX-Redirect"] = "/"
            return response

        @self.app.route("/get_animals", methods = ['GET'])
        def get_animals():
            req = request.args.getlist("searchInput")
            if req != [] and req != [""]:
                data = get_db().get_animals(req[0])
            else:
                data = get_db().get_animals()
            html = Design()
            return html.animals_tr(data)
            

        @self.app.route('/edit/<animal_id>', methods=["GET"])
        def edit_get_animal(animal_id):
            animal = get_db().pick_animal(animal_id)
            caregiversTable = get_db().get_caregivers()
            cagesTable = get_db().get_cages()
            htmlComboBoxes = Design()
            with open("html/edit.html", "r") as file:
                site = file.read()
            site = site.replace("$animal_id", str(animal.id))
            site = site.replace("$animalName", animal.name)
            site = site.replace("$species", animal.specie)
            site = site.replace("$origin_country", str(animal.origin_country))
            site = site.replace("$birth_date", str(animal.birth_date))
            site = site.replace("$food", str(animal.food))
            site = site.replace("$feeding_time", str(animal.feeding_time))
            site = site.replace("$last_cleaning", str(animal.last_cleaning))
            caregivers, cages = htmlComboBoxes.cages_and_caregivers(cagesTable, caregiversTable, animal)
            site = site.replace('<!--$caregiver_key-->', caregivers)
            site = site.replace('<!--$cages Options-->', cages)
            return site

        @self.app.route('/edit/<animal_id>', methods=["POST"])
        def edit_post_animal(animal_id):
            animal = AnimalEntity()

            animal.modify(request.form, animal_id)

            get_db().update_animal(animal)
            response = make_response()
            response.headers["HX-Redirect"] = "/"
            return response

        @self.app.route('/delete/<animal_id>', methods=["POST"])
        def delete_animal(animal_id):
            get_db().delete_entity(animal_id, 'zoo')
            response = make_response()
            response.headers["HX-Redirect"] = "/"
            return response
        
        # CAREGIVERS
        @self.app.route('/caregivers', methods=["GET"])
        def caregivers():
            with open('html/caregivers.html', "r") as file:
                return file.read()


        @self.app.route("/add_caregiver", methods = ['POST'])
        def add_caregiver():
            f = request.form
            get_db().add_caregiver((f["caregiverName"], f["shift_days"], f["shift_time"]))
            response = make_response("")
            response.headers["HX-Trigger"] = "add_caregiver"
            response.headers["HX-Redirect"] = "/caregivers"
            return response
        
        @self.app.route('/get_caregivers', methods=["GET"])
        def get_caregivers():
            data = get_db().get_caregivers()
            html = Design()
            return html.caregivers_tr(data)
        
        @self.app.route('/edit_caregiver/<caregiver_id>', methods=["GET"])
        def edit_get_caregiver(caregiver_id):
            caregiver = get_db().pick_caregiver(caregiver_id)
            
            with open("html/caregiver_edit.html", "r") as file:
                site = file.read()
            site = site.replace("$caregiver_id", str(caregiver.id))
            site = site.replace("$caregiverName", str(caregiver.name))
            site = site.replace("$shift_days", str(caregiver.shift_days))
            site = site.replace("$shift_time", str(caregiver.shift_times))
            
            return site

        @self.app.route('/edit_caregiver/<caregiver_id>', methods=["POST"])
        def edit_post_caregiver(caregiver_id):
            caregiver = Caregiver()
            caregiver.modify(request.form, caregiver_id)
            get_db().update_caregiver(caregiver)
            response = make_response()
            response.headers["HX-Redirect"] = "/caregivers"
            return response
        
        @self.app.route('/delete_caregiver/<caregiver_id>', methods=["POST"])
        def delete_caregiver(caregiver_id):
            get_db().delete_entity(caregiver_id, 'caregivers')
            response = make_response()
            response.headers["HX-Redirect"] = "/caregivers"
            return response
        
        # CAGES
        @self.app.route('/cages', methods=["GET"])
        def cages():
            with open('html/cages.html', "r") as file:
                return file.read()


        @self.app.route("/add_cage", methods = ['POST'])
        def add_cage():
            f = request.form
            get_db().add_cage((f["cageName"], f["cleaning_days"], f["cleaning_time"]))
            response = make_response("")
            response.headers["HX-Trigger"] = "add_cage"
            response.headers["HX-Redirect"] = "/cages"
            return response
        
        @self.app.route('/get_cages', methods=["GET"])
        def get_cages():
            data = get_db().get_cages()
            html = Design()
            return html.cages_tr(data)
        
        @self.app.route('/edit_cage/<cage_id>', methods=["GET"])
        def edit_get_cage(cage_id):
            cage = get_db().pick_cage(cage_id)
            
            with open("html/cages_edit.html", "r") as file:
                site = file.read()
            site = site.replace("$cage_id", str(cage.id))
            site = site.replace("$cageName", str(cage.name))
            site = site.replace("$cleaning_days", str(cage.cleaning_days))
            site = site.replace("$cleaning_time", str(cage.cleaning_time))
            
            return site

        @self.app.route('/edit_cage/<cage_id>', methods=["POST"])
        def edit_post_cage(cage_id):
            cage = Cages()
            cage.modify(request.form, cage_id)
            get_db().update_cage(cage)
            response = make_response()
            response.headers["HX-Redirect"] = "/cages"
            return response
        
        @self.app.route('/delete_cage/<cage_id>', methods=["POST"])
        def delete_cage(cage_id):
            get_db().delete_entity(cage_id, 'cages')
            response = make_response()
            response.headers["HX-Redirect"] = "/cages"
            return response
        
        # Main

        @self.app.teardown_appcontext
        def close_connection(exception):
            db = getattr(g, '_database', None)
            if db is not None:
                db.close()

        @self.app.route('/static/<path:path>')
        def static_file(path):
            return self.app.send_static_file(f"static/{path}")


if __name__ == '__main__':
    theApp = App()
    theApp.app.run(debug=True)