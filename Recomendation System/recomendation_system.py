import pyodbc 
from flask import *
import json
import pandas as pd 
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.linear_model import Ridge
from sklearn import linear_model
import datetime as dt
from flask_cors import CORS
import pandas as pd

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-JT5VP5I;'
                      'Database=BookStoreAPI;'
                      'Trusted_Connection=yes;')

def GetBooks():
    cursor = conn.cursor()
    books = cursor.execute('SELECT Id,Title,Price, Image FROM Books').fetchall()
    books = pd.DataFrame([[x[0], x[1], x[2], x[3]] for x in books], columns=['BookId', 'Title', 'Price', 'Image'])
    return books

def GetRatings():
    cursor = conn.cursor()
    ratings = cursor.execute('SELECT UserId,BookId,Rate FROM Ratings').fetchall()
    ratings = pd.DataFrame([[x[0], x[1], x[2]] for x in ratings], columns=['UserId', 'BookId', 'Rate'])
    return ratings

def GetVectorFeature(data):
    return 0

def item_based_recommender(bookId,user_book_df):
    book_name_df = user_book_df[bookId]
    recommend = user_book_df.corrwith(book_name_df).sort_values(ascending=False)
    return recommend

def GetBookById(id, data):
    return data.loc[data['BookId'] == id, ]

app = Flask(__name__)
CORS(app)

@app.route('/recommend/<int:book_id>', methods=['GET'])
def recommend_page(book_id):
    #Get id recoment
    id = book_id

    #Get books data
    book_df = GetBooks()

    #Get ratings data
    rating_df = GetRatings()

    #Tiền xử lý dữ liệu
    
    book_rating_df = rating_df.merge(book_df, left_on = 'BookId', right_on = 'BookId')
    user_book_df = book_rating_df.pivot_table(index=["UserId"],columns=["BookId"],values=["Rate"])
    user_book_df = pd.DataFrame(user_book_df)
    user_book_df = user_book_df["Rate"]

    book_recomend = (item_based_recommender(id,user_book_df))

    books = []
    for id in book_recomend.index.to_numpy():
        # books.append(GetBookById(id,book_df))
        books.append(id)

    print(books)

    response = {
            'code': 200,
            'message': 'success',
            'data': [arr.tolist() for arr in books]
        }
    json_data = json.dumps(response, ensure_ascii=False)
    return json_data

if __name__ == '__main__':
    app.run(port=5000)