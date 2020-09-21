from flask import Flask,render_template,request,url_for,flash,redirect
import numpy as np
import pandas as pd
import pickle
app=Flask(__name__)


model = pickle.load(open('model_housePricePrediction_xgboost.pkl', 'rb'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/housePricePrediction", methods=['GET','POST'])
def housePricePrediction():
        if request.method=='POST':
            OverallQual=(request.form['OverallQual'])
            GrLivArea=float(request.form['GrLivArea'])
            stFlrSF=float(request.form['1stFlrSF'])
            GarageCars=float(request.form['GarageCars'])
            LotArea=float(request.form['LotArea'])  
            MasVnrArea=float(request.form['MasVnrArea'])
            YearBuilt=int(request.form['YearBuilt'])
            YearRemodAdd=int(request.form['YearRemodAdd'])
            LotFrontage=int((request.form['LotFrontage'] ).replace('.',''))
            BsmtUnfSF=float(request.form['BsmtUnfSF'])
            TotRmsAbvGrd=int(request.form['TotRmsAbvGrd'])
            MoSold=float(request.form['MoSold']) 
            Fireplaces=int(request.form['Fireplaces'] )
            WoodDeckSF=int(request.form['WoodDeckSF'] )
            OpenPorchSF=int(request.form['OpenPorchSF'] )
            OverallCond= int(request.form['OverallCond'] )
            CentralAir= str((request.form['CentralAir']).upper() )
          
            
            data=[OverallQual, GrLivArea, stFlrSF, GarageCars, LotArea,
                      MasVnrArea, YearBuilt, YearRemodAdd, LotFrontage, BsmtUnfSF,
                          TotRmsAbvGrd, MoSold, Fireplaces, WoodDeckSF, OpenPorchSF,OverallCond,CentralAir]
            data=np.array(data)
            data=data.reshape(1, -1)
            df=pd.DataFrame(data)
            df.columns=['OverallQual', 'GrLivArea', '1stFlrSF', 'GarageCars', 'LotArea',
                            'MasVnrArea', 'YearBuilt', 'YearRemodAdd', 'LotFrontage', 'BsmtUnfSF',
                                'TotRmsAbvGrd', 'MoSold', 'Fireplaces', 'WoodDeckSF', 'OpenPorchSF','OverallCond','CentralAir']
            
            prediction=model.predict(df)
            output=round(prediction[0],2)
            result=output
            lower=round((output-(0.20*output)),2)
            upper=round((output+(0.20*output)),2)
            
            if output<=0:
                return render_template('housePricePrediction.html',output="Sorry you cannot sell this House. value is Nill")
            else:
                return render_template('housePricePrediction.html',output=(result))
            
        else:
            return render_template('housePricePrediction.html')


@app.route("/blightTicketPaymentPrediction", methods=['GET','POST'])
def blightTicketPayment():
    return render_template('blightTicketPaymentPrediction')

@app.route("/vehiclePricePreiction", methods=['GET','POST'])
def vehiclePricePrediction():
    return render_template('vehiclePricePreiction')



if __name__=='__main__':
    app.run(debug=True)
    
    
