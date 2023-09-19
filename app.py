from flask import Flask,redirect,session,render_template,request,url_for
from car_class import Car, RepairSchema, CarSchema
from crud import save,load
from marshmallow import Schema, fields,ValidationError

repair_schema = RepairSchema()
car_schema = CarSchema()


try:
    data=load()
except:
    save(data=[])


app=Flask(__name__)
app.secret_key="123456"

@app.route('/')
def home():
    try:
        del session["chosen_car"]
    except KeyError:
        pass
    return render_template('home.html')

@app.route("/create", methods=["GET","POST"])
def create():
    if request.method=="GET":
        return render_template("create_car.html",status=request.args.get("status",""))
    if request.method == "POST":
        car_input= {"numberplate" : request.form["numberplate"],"holdername":request.form["holdername"],"manufacture":request.form["manufacture"],"model":request.form["model"],"year":request.form["year"],"color":request.form["color"],"tire_size":request.form["tire_size"]}
        try:
            car_schema.load(car_input)
            database = load()
            database.append(Car(numberplate=request.form["numberplate"],holdername=request.form["holdername"],manufacture=request.form["manufacture"],model=request.form["model"],year=request.form["year"],color=request.form["color"],tire_size=request.form["tire_size"]))
            save(data=database)
            return redirect(url_for("create",status=1))
        except ValidationError as err:
            return redirect(url_for("create",status=2))
            
        
        
    
@app.route("/database")
def database():
    database = load()
    try:
        del session["chosen_car"]
    except KeyError:
        pass
    return render_template("database.html",database=database)

@app.route("/car_delete")
def car_delete():
    if len(request.args) == 1 and request.args["chosen_car"].isdigit() == True:
        choice=int(request.args["chosen_car"])
        database = load()
        if 0<=choice<=len(database):
            database.remove(database[choice])
            save(data=database)
            try:
                del session["chosen_car"]
            except KeyError:
                pass
            return redirect("/database")
        else:
            return redirect("/database")
    else:
        return redirect("/database")
    


@app.route("/car_info")
def car_info():
    if len(request.args) == 1 and request.args["chosen_car"].isdigit() == True or session["chosen_car"] == True:
        choice=int(request.args["chosen_car"])
        session["chosen_car"]=request.args["chosen_car"]
        database = load()
        if 0<=choice<=len(database):
            return render_template('car_info.html', carinfo=database[int(session["chosen_car"])])
        else:
            return redirect("/database")
    else:
        return redirect("/database")
    
@app.route("/car_history")
def car_history():
    if session.get("chosen_car",False) != False:
        database = load()
        if 0<=int(session["chosen_car"])<=len(database):
            return render_template('history.html', car_history=database[int(session["chosen_car"])].repair_history)
        else:
            return redirect("/")
    else:
            return redirect("/")


@app.route("/car_repair",methods=["GET","POST"])
def repair():
    if request.method=="GET":
        if session.get("chosen_car",False) != False:
            database = load()
            if 0<=int(session["chosen_car"])<=len(database):
                return render_template('create_repair.html',status=request.args.get("status",""))
            else:
                return redirect("/")
        else:
            return redirect("/")
    if request.method=="POST":
        repair_input = {"mechanic_name":request.form["mechanic_name"],"date":request.form["date"],"start_time":request.form["start_time"],"end_time":request.form["end_time"],"number_of_tires":request.form["number_of_tires"],"price":request.form["price"],"notes":request.form["notes"]}
        try:
            repair_schema.load(repair_input)
            database = load()
            database[int(session["chosen_car"])].new_repair(mechanic_name=request.form["mechanic_name"],date=request.form["date"],start_time=request.form["start_time"],end_time=request.form["end_time"],number_of_tires=request.form["number_of_tires"],price=request.form["price"],notes=request.form["notes"])
            database[int(session["chosen_car"])].new_entrance()
            save(data=database)
            return redirect(url_for("repair",chosen_car=int(session["chosen_car"]),status=1))
        except ValidationError as err:
            return redirect(url_for("repair",chosen_car=int(session["chosen_car"]),status=2))
        
        
    
@app.route("/search")
def search():
    if request.args["q"].isdigit() == True:
        database = load()
        return render_template("database.html", database=[car for car in database if request.args["q"]==car.numberplate])


@app.route("/car_update", methods=["GET","POST"])
def car_update():
    if request.method=="GET":
        if session.get("chosen_car",False) != False:
            database = load()
            if 0<=int(session["chosen_car"])<=len(database):
                return render_template('car_update.html',car=database[int(session["chosen_car"])],status=request.args.get("status",""))
            else:
                return redirect("/")
        else:
                return redirect("/")
    if request.method=="POST":
        car_input= {"numberplate" : request.form["numberplate"],"holdername":request.form["holdername"],"manufacture":request.form["manufacture"],"model":request.form["model"],"year":request.form["year"],"color":request.form["color"],"tire_size":request.form["tire_size"]}
        try:
            car_schema.load(car_input)
            database = load()
            database[int(session["chosen_car"])].update_car(numberplate=request.form["numberplate"],holdername=request.form["holdername"],manufacture=request.form["manufacture"],model=request.form["model"],year=request.form["year"],color=request.form["color"],tire_size=request.form["tire_size"])
            save(data=database)
            return redirect(url_for("car_update",chosen_car=session["chosen_car"],status=1))
        except ValidationError as err:
            return redirect(url_for("car_update",chosen_car=session["chosen_car"],status=2))

    