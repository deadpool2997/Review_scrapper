import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)  # returns HTTPS response object
            flipkartPage = uClient.read()  # reads teh above url
            uClient.close()  # close the read request
            flipkart_html = bs(flipkartPage, "html.parser")
            link = []
            for lk in flipkart_html.findAll('a', {'href': re.compile('&srno=s_1_1')}):
                link.append(lk.get('href'))
            # print(link)
            f_link = 'https://www.flipkart.com' + link[0]
            # print(f_link)
            uClient1 = uReq(f_link)  # returns HTTPS response object
            flipkartPage1 = uClient1.read()  # reads teh above url
            uClient1.close()  # close the read request
            flipkart_html1 = bs(flipkartPage1, "html.parser")
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment, Certified \n"
            fw.write(headers)
            reviews = []
            i=0
            for rr in flipkart_html1.findAll('div', {'class': 'col _390CkK'}):
                rating = flipkart_html.find_all('div', {'class': 'hGSR34 E_uFuv'})[i].text
                cust_name = flipkart_html1.find_all('p', {'class': '_3LYOAd _3sxSiS'})[i].text
                heading = flipkart_html1.find_all('p', {'class': '_2xg6Ul'})[i].text
                comment = flipkart_html1.find_all('div', {'class': 'qwjRop'})[i].text
                certified = flipkart_html1.find_all('p', {'class': '_19inI8'})[i].text
                mydict = {"Product": 'tv', "Name": cust_name, "Rating": rating, "CommentHead": heading,
                          "Comment": comment, "certified": certified}
                reviews.append(mydict)
                i+=1
            return render_template('result.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=8001, debug=True)
