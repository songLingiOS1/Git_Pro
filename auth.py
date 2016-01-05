uthor__ = 'MoMoWang'

#from flask import Flask, url_for, render_template, request, session, redirect, escape,jsonify,json

from flask import Flask,request,jsonify,json
from flask.ext.httpauth import HTTPBasicAuth
from pymongo import MongoClient
from cStringIO import StringIO
import time

auth = HTTPBasicAuth()




app = Flask(__name__)

link = MongoClient('localhost',27017)
db = link.shop


@auth.verify_password
def verify_password(username, password):
    if username != "momowang" or password != "123":
        return False
    return True

@app.route('/', methods=['POST','GET'])
@auth.login_required
def testServer():
    return jsonify({"result":"ok"})

@app.route('/helloworld', methods=['POST','GET'])
def hello_world():
    resultData = []
    result = db.user.find({"name":"wang"},{"_id":0}).sort("name")
    for item in result:
        resultData.append(item)
    #print(resultData)
    if resultData:
        return jsonify({"result":"successful","data":resultData})
    else:
        return jsonify({"result":"noData"})



#01添加商品图片
@app.route('/uploadImage', methods=['POST','GET'])
def uploadImage():
    if request.method == 'POST':
        file = request.files['pic']
        if file:
                print('有收到文件')
                content = StringIO(file.read())
                currentTime = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime())
                ip = request.remote_addr
                filename = '/data/images/'+currentTime+'_'+ip+'.jpeg'
                print (filename)
                f = open(filename,'w')
                f.write(content.getvalue())
                f.close()
                imageURL = currentTime + '_' + ip + '.jpeg'
                return jsonify({"result":"successful","imageURL":imageURL})
        else:
            return jsonify({"result":"notReceivePic"})
    else:
        return jsonify({"result":"PostMethodsError"})

#02添加商品
@app.route('/addProduct',methods=['POST','GET'])
def addProduct():
    print "request is coming"
    if request.method == 'POST':
#	print("data is coming")
        if request:
            print(request.json)
            productInfo = {
                'codeNum'       :request.json['codeNum'],

                'name'          :request.json['name'],

                'oldPrice'      :request.json['oldPrice'],

                'promotionPrice':request.json['promotionPrice'],

                'productIntroduce':request.json['productIntroduce'],

                'isPromotionProduct':request.json['isPromotionProduct'],

                'unit'          :request.json['unit'],

                'cataGory'      :request.json['cataGory'],

                'isRecommendProduct':request.json['isRecommendProduct'],

                'imagesURL'     :request.json['imagesURL'],

                'beloneToShop'  :request.json['beloneToShop'],

                'inventoryLevel':request.json['inventoryLevel'],

                'productionDate':request.json['productionDate'],

                'expiration'    :request.json['expiration'],

                'shelfLife'     :request.json['shelfLife'],

                "saleState"     : request.json["saleState"]
            }

            print(productInfo)

            for (key,value) in productInfo.items():
                if key == None:
                    return jsonify({"result":"paraError"})

            #insert db
            #检测该商品的条形码是否已经存在
            findResultdata = db.products.find_one({"codeNum":productInfo["codeNum"]})
            print(findResultdata)

            if findResultdata:
                if "codeNum" in findResultdata:
                    if findResultdata["codeNum"] == productInfo["codeNum"]:
                        return jsonify({"result":"thisProductIsPresent"})

            db.products.insert(productInfo)

            #检测是否插入数据库
            findCodeNum = db.products.find_one({"codeNum":productInfo["codeNum"]})

            if "codeNum" in findCodeNum:
                if findCodeNum["codeNum"] == productInfo["codeNum"]:
                    return jsonify({"result":"insertProductSuccessfull"})
            else:
                return jsonify({"result":"insertProductError"})

        else:
            return jsonify({"result":"addProductError"})

    else:
        return jsonify({"result":"PostMethodsError"})


if __name__ == '__main__':
    app.run(debug=True)
