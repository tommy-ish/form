from flask import *
import pandas as pd
import datetime
import random

app = Flask(__name__)
app.secret_key = '10928482048'

@app.route('/', methods=['GET'])
def start():
    return render_template("start.html")

@app.route('/', methods=['POST'])
def post_id():
    lancers_id = request.form.get("value1")
    session.permanent = False
    session["id"] = lancers_id
    if not session["id"]:
        return redirect(url_for('start'))
    else:
        return redirect(url_for('form'))

@app.route('/form', methods=['GET'])
def form():
    review_data = []
    sample_review_index = []
    df = pd.read_csv("./static/data/review_form.csv", header=None, names=["review"])
    sample_review = df["review"].sample(40)
    for i in range(0, 40):
        sample_review_index.append(sample_review.index[i])
    for i in range(len(df["review"])):
        review_data.append(df["review"][i])
    return render_template("index.html", sample_review=sample_review, review_data=review_data, sample_review_index=sample_review_index)

@app.route('/show', methods=['POST'])
def show():
    df = pd.read_csv("./static/data/review_form.csv", header=None, names=["review"])
    review_id = []
    part1 = []
    purpose1 = []
    part2 = []
    purpose2 = []
    part3 = []
    purpose3 = []
    exist = []
    for i in range(0,40):
        review_id.append(request.form.get(f"review_index-{i}"))
        exist_value = request.form.get(f"is_exist-{i}")
        part1_value = request.form.get(f"part1-{i}")
        purpose1_value = request.form.get(f"purpose1-{i}")
        part2_value = request.form.get(f"part2-{i}")
        purpose2_value = request.form.get(f"purpose2-{i}")
        part3_value = request.form.get(f"part3-{i}")
        purpose3_value = request.form.get(f"purpose3-{i}")

        part1.append(part1_value)
        purpose1.append(purpose1_value)
        part2.append(part2_value)
        purpose2.append(purpose2_value)
        part3.append(part3_value)
        purpose3.append(purpose3_value)
        exist.append(exist_value)

    reviews = []
    print(exist[0])
    try:
        for id in review_id:
            reviews.append(df["review"][int(id)])
    except:
        return redirect(url_for("form"))
    now = datetime.datetime.now()
    rand_num = random.randrange(999)
    f_name = f"{session['id']}_{now.strftime('%H%M')}_{rand_num:03}"
    with open(f"static/data/answer_data/{f_name}.txt", "w") as f:
        for i in range(0, 40):
            f.write(f'{review_id[i]},{reviews[i]}')
            if exist[i]:
                f.write(",なし")
            else:
                if not part1[i] and not part2[i] and not part3[i]:
                    f.write(",なし")
                else:
                    if part1[i]:
                        f.write(f',{part1[i]}')
                        f.write(f',{purpose1[i]}')
                    if part2[i]:
                        f.write(f',{part2[i]}')
                        f.write(f',{purpose2[i]}')
                    if part3[i]:
                        f.write(f',{part3[i]}')
                        f.write(f',{purpose3[i]}')
            f.write("\n")
    return render_template("show.html", token=f_name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')