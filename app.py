from flask import Flask, render_template,request
import pandas as pd
import pickle
import difflib
import numpy as np


popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
similarity_score = pd.read_pickle('similarity_score.pkl')
books = pd.read_pickle('books.pkl')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Num_Ratings'].values),
                           rating=list(popular_df['AVG_Ratings'].values))


@app.route('/search')
def recommendation_ui():
    return render_template('recommendation.html')

@app.route('/recommendation',methods=['POST'])
def recommendation():
    user_input = request.form.get('user_input')
    close_matches = difflib.get_close_matches(user_input, pt.index, n=1, cutoff=0.1)

    if not close_matches:
        print("No book found with a name similar to:", user_input)
        return
    matched_book = close_matches[0]

    index = np.where(pt.index == matched_book)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[0:9]

    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return render_template('recommendation.html',data=data)

@app.route('/about')
def about():
    return  render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
