from ast import pattern
from sqlalchemy import null
from database import *
from flask import Flask,render_template,request,session
from algo import perfrom_recommendations
import json

# Start of application....
# Getting database connection
c , conn = create_schema()

application = Flask(__name__)
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
application.config['SECRET_KEY'] = 'THis Very StRong K3Y to Br#@K ! '


df_connector = read_data_from_csv_file()
global_dict = {}

@application.route('/')
def main_page():
    try:
        return render_template("index.html")
    except Exception as e:
        return render_template("error.html")

@application.route('/home')
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return render_template("error.html")

@application.route('/about')
def about():
    try:
        return render_template("about.html")
    except:
        return render_template("error.html")

@application.route('/blog')
def blog():
    try:
        return render_template("blog.html")
    except:
        return render_template("error.html")

@application.route('/blogDetails')
def blogDetails():
    try:
        return render_template("blog-details.html")
    except:
        return render_template("error.html")

@application.route('/contact')
def contact():
    try:
        return render_template("contact.html")
    except:
        return render_template("error.html")

@application.route("/signInScreen")
def signInScreen():
    try:
        if(session.get('email')!=None and session.get('password')!=None):
            return render_template("form.html")

        return render_template("signIn.html")
    except Exception as e:
        print(e)
        return render_template("error.html")

@application.route("/signUpScreen")
def signUpScreen():
    try:
        return render_template("signIn.html")
    except:
        return render_template("error.html")



@application.route("/signedIn",methods=['POST'])
def signedIn():
    try:
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return render_template("form.html")
    except:
        return render_template("error.html")


@application.route("/signedUp",methods=['POST'])
def signedUp():
    try:
        data = json.loads(request.data)
        c.execute("insert into Clients (name,email,password) values (?,?,?)",(data['name'],data['email'],data['password'],))
        conn.commit()
        return("user created")
    except Exception as e:
         print(e)
         return("Error")
         

@application.route('/recommend',methods=['POST'])
def recommend():
    try:
        
        global_dict['counter'] = 0

        solid_check_list = ["check_1","check_2","check_3","check_4","check_5","check_6","check_7","check_8","check_9","check_10","check_11"]
        pattern_check_list = ["check_12","check_13","check_14","check_15","check_16","check_17","check_18","check_19","check_20","check_21","check_22"]
        
        acsent_color = []
        pattern_color = []

        # print(request.form)

        input_dict = {
            "Name": request.form["name"],
            "Age":request.form["age"],
            "Base_color":request.form["base_color"],
            "Description":request.form["description"],
            "Event":request.form["select_event"],
            "Time":request.form["select_time"],
            "Venue":request.form["select_venue"],
            "material":request.form["material_of_saree"],
        }
      
        # solid
        if(request.form["style_flag"]=='0'):
            for x in solid_check_list:
                if(x in request.form):
                    acsent_color.append(request.form[x])
            input_dict['acsent_color'] = acsent_color
        
        # Pattern
        else:
            for x in pattern_check_list:
                if(x in request.form):
                    pattern_color.append(request.form[x])
            input_dict['pattern_color'] = pattern_color
            input_dict['kind_of_pattern'] = request.form["kind_of_pattern"]
        

        global_dict['user_input'] = input_dict


        a,b,c = perfrom_recommendations(df_connector.copy(),input_dict)

        global_dict['recommendations_liked'] = {}
        
        global_dict['recommendations'] = pd.concat([a, b], ignore_index=True)
        global_dict['recommendations'] = pd.concat([global_dict['recommendations'], c], ignore_index=True)
        global_dict['recommendations'] = global_dict['recommendations'].drop_duplicates()
        
        # print(".............................")
        # print(global_dict["recommendations"].head(4))
        if(len(global_dict['recommendations'])==0):
            print("No results .. Sorry")
            return render_template("recommendations.html",img1 = "no-img.png" ,img2 = "no-img.png" , img3 = "no-img.png",id_1=-1,id_2=-1,id_3=-1,color_1='black',color_2='black',color_3='black')
            
        else:
            filter_recommendations = global_dict['recommendations'].iloc[global_dict['counter']:global_dict['counter']+3]
            global_dict['counter'] = global_dict['counter'] + 3
            img1 = "no-img.png"
            img2 = "no-img.png"
            img3 = "no-img.png"
            id_1 = -1
            id_2 = -1
            id_3 = -1
            for x in range(0,len(filter_recommendations)):
                if(x==0):
                    img1 = filter_recommendations.iloc[x,4]
                    id_1 = filter_recommendations.iloc[x,0]
                    img1 = img1.replace("./images/","")
                elif(x==1):
                    img2 = filter_recommendations.iloc[x,4]
                    id_2 = filter_recommendations.iloc[x,0]
                    img2 = img2.replace("./images/","")
                else:
                    img3 = filter_recommendations.iloc[x,4]
                    id_3 = filter_recommendations.iloc[x,0]
                    img3 = img3.replace("./images/","")
            return render_template("recommendations.html",img1 = img1 , img2 = img2 , img3 = img3,id_1=id_1,id_2=id_2,id_3=id_3,color_1='black',color_2='black',color_3='black')
              
    except Exception as e:
        print(e)
        return render_template("error.html")
    
@application.route('/TryAgain',methods=['POST'])
def recommend_again():
    try:
        #------------------------------------------------#
        img_id_1 = int(request.form['image_1_id'])
        img_id_2 = int(request.form['image_2_id'])
        img_id_3 = int(request.form['image_3_id'])

        like_flag_1 = request.form['image_1_like']
        like_flag_2 = request.form['image_2_like']
        like_flag_3 = request.form['image_3_like']

        if(like_flag_1=='True' and img_id_1!=-1):
            global_dict["recommendations_liked"][img_id_1] = 'True'
        else:
            try:
                del global_dict["recommendations_liked"][img_id_1]
            except:
                pass

        if(like_flag_2=='True' and img_id_2!=-1):
            global_dict["recommendations_liked"][img_id_2] = 'True'
        else:
            try:
                del global_dict["recommendations_liked"][img_id_2]
            except:
                pass

        if(like_flag_3=='True' and img_id_3!=-1):
            global_dict["recommendations_liked"][img_id_3] = 'True'
        else:
            try:
                del global_dict["recommendations_liked"][img_id_3]
            except:
                pass
        #------------------------------------------------#
        
        if(global_dict['counter']>=len(global_dict['recommendations'])):
            global_dict['counter'] = 0
        
        filter_recommendations = global_dict['recommendations'].iloc[global_dict['counter']:global_dict['counter']+3]
        global_dict['counter'] = global_dict['counter'] + 3

        img1 = "no-img.png"
        img2 = "no-img.png"
        img3 = "no-img.png"

        id_1 = -1
        id_2 = -1
        id_3 = -1

        color_1 = "black"
        color_2 = "black"
        color_3 = "black"


        for x in range(0,len(filter_recommendations)):
                if(x==0):
                    img1 = filter_recommendations.iloc[x,4]
                    img1 = img1.replace("./images/","")
                    id_1 = filter_recommendations.iloc[x,0]
                    if(id_1 in global_dict['recommendations_liked']):
                        color_1 = "blue"

                elif(x==1):
                    img2 = filter_recommendations.iloc[x,4]
                    img2 = img2.replace("./images/","")
                    id_2 = filter_recommendations.iloc[x,0]
                    if(id_2 in global_dict['recommendations_liked']):
                        color_2 = "blue"
                else:
                    img3 = filter_recommendations.iloc[x,4]
                    img3 = img3.replace("./images/","")
                    id_3 = filter_recommendations.iloc[x,0]
                    if(id_3 in global_dict['recommendations_liked']):
                        color_3 = "blue"

        return render_template("recommendations.html",img1 = img1 , img2 = img2 , img3 = img3, id_1=id_1, id_2=id_2, id_3=id_3,color_1=color_1,color_2=color_2,color_3=color_3)


    except Exception as e:
        print(e)
        return render_template("error.html")


@application.route('/save',methods=['POST'])
def save_response():
    print(global_dict['user_input'])
    print("\n\n")
    
    name = global_dict['user_input']['Name']
    age = global_dict['user_input']['Age']
    base_color = None
    pattern_color = None

    if("acsent_color" in global_dict['user_input']):
        pass

    if("pattern_color" in global_dict['user_input']):
        pass

    base_color = global_dict['user_input']['Age']

    c.execute("insert into Users (Name,Age,event,TIME,VENUE,description,base_color,acsent_color,material,pattern_color,kind_of_pattern,recommendation_type) values (?,?,?,?,?,?,?,?,?,?,?,?)",(data['name'],data['email'],data['password'],))
    conn.commit()
    print(global_dict['recommendations_liked'])
    return global_dict

if __name__ == '__main__':
    application.run(debug=True)