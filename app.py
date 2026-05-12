from flask import Flask,render_template , request
import pickle
import numpy as np


with open('popular.pkl', 'rb') as f:
    popular_df = pickle.load(f)

with open('pt.pkl', 'rb') as f:
    pt = pickle.load(f)

with open('books.pkl', 'rb') as f:
    books = pickle.load(f)

with open('similarity_score.pkl', 'rb') as f:
    similarity_score = pickle.load(f)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['title'].values),
                           author=list(popular_df['author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           ratings=list(popular_df['avg_ratings'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]

    similar_items = sorted(enumerate(similarity_score[index]), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        item.extend(list(temp_df.drop_duplicates('title')['Image-URL-M'].values))

        data.append(item)

        print(data)


    return render_template('recommend.html',data = data)



if __name__ == '__main__':
    app.run(debug=True)
