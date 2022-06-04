from flask import Flask, render_template, request, make_response
import re
import postgre


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/select")
def select():
    condition = request.query_string.decode().replace("&", " AND ")
    condition = re.sub(r"((?<==)\S*)", r"'\1'", condition)
    print("[CONDOTION]", condition, sep="\n")
    fields = "f_val, n_val, p_val, s_val, building, korpus, apartments, phone"
    if(condition):
        res = postgre.select("main", fields, True, condition)
    else:
        res = postgre.select("main", fields, False)
    print("[RES]", res, sep="\n")
    return make_response(res, 200)


@app.route("/add")
def add():
    values = request.query_string.decode().replace("&", ", ")  # & -> ,
    # kostily
    street = re.findall(r"(?<=s_val=)\w*", values)[0]  # save street value
    values = values.replace(", s_val=" + street, "")  # delete strett
    values = re.sub(r"((?<==)[a-zA-z]+)", r"'\1'", values)  # take name in ""
    values = re.sub(r"[a-z_]*=(?=['0-9])", "", values)  # delete all before =<value>
    values += ", '" + street + "'"
    values = re.sub(r"'NULL'", r"NULL", values)  # dele " around NULL
    print(values)
    postgre.insert("main", values)
    return values


@app.route("/delete")
def delete():
    condition = request.query_string.decode().replace("&", " AND ")
    condition = re.sub(r"((?<==)\S*)", r"'\1'", condition)
    res = postgre.delete("main", condition)
    return res


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(debug=True)
