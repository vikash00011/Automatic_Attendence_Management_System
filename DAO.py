from pymongo import MongoClient

class DAO:

    def __init__(self,present):
        self.present=present
        self.students={3:"Vikash",5:"Aviral",6:"Sachin",7:"Abhishek",8:"Divyansh",0:"Arvind",2:"Snehal",4:"Suvidha"}

    def dbOperations(self):
        
        self.client=MongoClient(port=27017)
        db=self.client.attendence_db
        #insert=attendence_db.students.insert_one({'Name':'Vikash','Age':27,'School':'IACSD'})
        #result=db.students.find()

        
        present=list(self.present)
        present.sort();
        print(type(present))
        for rollno in present:
            if rollno in self.students:
                try:
                    db.students.insert_one({"_id":rollno,"Name":self.students[rollno],"Attendence":[]})
                    db.students.update_one({"_id":rollno},{'$push': {"Attendence":'P'}})
                except:
                    db.students.update_one({"_id":rollno},{'$push': {"Attendence":'P'}})

        set_present=set(present)
        total_student=set(self.students.keys())
        print(total_student)
        print(type(total_student))
        print(type(set_present))
        absent=total_student - set_present
        print(absent)
        for rollno in absent:
            if rollno==1:
                continue
                try:
                    print("up try")
                    db.students.insert_one({"_id":rollno,"Name":self.students[rollno],"Attendence":[]})
                    print("middle try")
                    db.student.update_one({"_id":rollno},{'$push' : {"Attendence":'A'}})
                    print("down try")
                except:
                    print("up except")
                    db.students.update_one({"_id":rollno},{'$push' : {"Attendence":'A'}})
                    print("down except")

    def __del__(self):
        self.client.close()
    
            

