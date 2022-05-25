from database import *
from flask import Flask,render_template,request,session
from algo import perfrom_recommendations


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
        pass
    except:
         return render_template("error.html")

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
        

        a,b,c = perfrom_recommendations(df_connector.copy(),input_dict)

        
        global_dict['recommendations'] = pd.concat([a, b], ignore_index=True)
        global_dict['recommendations'] = pd.concat([global_dict['recommendations'], c], ignore_index=True)
        global_dict['recommendations'] = global_dict['recommendations'].drop_duplicates()
        
        if(len(global_dict['recommendations'])==0):
            print("No results .. Sorry")
            return render_template("recommendations.html",img1 = "no-img.png" ,img2 = "no-img.png" , img3 = "no-img.png")
            
        else:
            filter_recommendations = global_dict['recommendations'].iloc[global_dict['counter']:global_dict['counter']+3]
            global_dict['counter'] = global_dict['counter'] + 3
            img1 = "no-img.png"
            img2 = "no-img.png"
            img3 = "no-img.png"
            for x in range(0,len(filter_recommendations)):
                if(x==0):
                    img1 = filter_recommendations.iloc[x,4]
                    img1 = img1.replace("./images/","")
                elif(x==1):
                    img2 = filter_recommendations.iloc[x,4]
                    img2 = img2.replace("./images/","")
                else:
                    img3 = filter_recommendations.iloc[x,4]
                    img3 = img3.replace("./images/","")
            return render_template("recommendations.html",img1 = img1 , img2 = img2 , img3 = img3)
              
    except Exception as e:
        print(e)
        return render_template("error.html")
    
@application.route('/TryAgain',methods=['POST'])
def recommend_again():
    try:
        
        if(global_dict['counter']>=len(global_dict['recommendations'])):
            global_dict['counter'] = 0
        
        filter_recommendations = global_dict['recommendations'].iloc[global_dict['counter']:global_dict['counter']+3]
        global_dict['counter'] = global_dict['counter'] + 3

        img1 = "no-img.png"
        img2 = "no-img.png"
        img3 = "no-img.png"

        for x in range(0,len(filter_recommendations)):
                if(x==0):
                    img1 = filter_recommendations.iloc[x,4]
                    img1 = img1.replace("./images/","")
                elif(x==1):
                    img2 = filter_recommendations.iloc[x,4]
                    img2 = img2.replace("./images/","")
                else:
                    img3 = filter_recommendations.iloc[x,4]
                    img3 = img3.replace("./images/","")

        return render_template("recommendations.html",img1 = img1 , img2 = img2 , img3 = img3)


    except Exception as e:
        print(e)
        return render_template("error.html")

if __name__ == '__main__':
    application.run(debug=True)