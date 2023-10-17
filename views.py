import math
from flask import render_template, request, url_for, redirect,session
from app import app, db
from models import User
from utils import validate_reg, validate_login
import pandas as pd




productReview = pd.read_excel('./data/Lifelong LLPCM05 Beard Trimmer for Men, with One Year Warranty (Black)_Lifelong_2019-11-09_reviews.xlsx')
  
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        response = request.form.to_dict()
        # validate the form response
        if validate_reg(response):
            user = User.query.filter_by(email=response.get('email')).first()
            # user with same email should not be already registered.
            if not user:
                user = User(first_name=response.get('first_name'), last_name=response.get('last_name'),
                            email=response.get('email'))
                user.set_password(response.get('password'))
                db.session.add(user)
                db.session.commit()

                # registration successful
                return redirect(url_for('login'))

    # for GET request and invalid form data , return register page
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = request.form.to_dict()
        # validate login form data
        if validate_login(response):
            user = User.query.filter_by(email=response.get('email')).first()
            #  check if user is registered
            if user:
                check = user.check_password(response.get('password'))
                # if password is correct
                if check:
                    # can flash login-success message
                    # We can also generate and return jwt token here
                    session["email"] =response.get('email')
                    return redirect(url_for('index'))

    # for GET request and invalid form data , return login page
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return  redirect( url_for("login"))


@app.route('/map')
def map1():
    return render_template('map1.html')

@app.route('/worldcloud')
def wordcloud():
    return render_template('wordcloud.html')


@app.route('/sentiment_analysis')
def sentiments_analysis():
#   product  in templates are watches but excel data were of trimmer
    data = productReview[['Review_Stars','Review_Title','Review_Text','Reviewer_Name']].sort_values(by='Review_Stars', ascending=False).values
    Arr=[]
    posRev,negRev=0,0
    for key in data:
        
        try:
            Arr.append( {
                "Review_Stars":int(key[0]),
                "Review_Title":key[1],
                "Review_Text":key[2],
                "Reviewer_Name":key[3]
                })
            if int(key[0])<2.5:  # considering  Review_Stars > 2.5 as positive review and all else as negative review.
                negRev+=1
            else:
                posRev+=1         
        except ValueError:
            pass
    diff_rev = {'posRev': posRev, 'negRev': negRev} # to be used by Pie chart
  
    return render_template('detailed_sentiment.html',data=Arr,diff_rev=diff_rev)


@app.route('/feature_breakdown')
def feature_breakdown():
    #   product  in templates are watches but excel data were of trimmer
    data = productReview[['Review_Stars','Review_Title','Review_Text','Reviewer_Name']].sort_values(by='Review_Stars', ascending=False).values
    Arr = {
            "Quality": {"positive": "", "negative": "","count":0}, #count to be used by horizontal bars chart
            "Battery": {"positive": "", "negative": "","count":0},
            "Product": {"positive": "", "negative": "","count":0},
            "Price": {"positive": "", "negative": "","count":0},
            "Water_Resistance": {"positive": "", "negative": "","count":0}
        }
    countArr=[]
    for key in data:
      
        for k, v in Arr.items():
            if str(k).lower() in str(key[2]).lower():
                try:
                    if int(key[0]) < 2.5:   # considering  Review_Stars > 2.5 as positive review and all else as negative review.
                        v["negative"] = key[2]
                        v["count"]+=1
                    else:
                        v["positive"] = key[2]
                        v["count"]+=1
                        break
                    
                except ValueError:
                    pass
    total=sum([v["count"] for k,v in  Arr.items()]) #total count of features
    
    return render_template('feature_breakdown.html',data=Arr,count=countArr,total=total)


@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html')

@app.route('/competitor_analysis')
def comp_analysis():
    return render_template('All_textual.html')


@app.route('/product_list')
def prod_list():
    return render_template('tables.html')
