# project: p4
# submitter: txiong53@wisc.edu
# partner: none
# hours: 14

import re
import pandas as pd
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, Response
from io import StringIO

matplotlib.use('Agg')

app = Flask(__name__)



num_subscribed = 0
counter = 0
A_val = 0
B_val = 0

@app.route('/')
def home():
    global counter
    with open("index.html") as f:
        html = f.read()
    if counter < 10:
        if counter % 2 == 0:
            html = html.replace('<a href="donate.html">Donate Page!</a>',
                                '<a href="donate.html?from=A" style="color:red;">Donate Page!</a>')
            counter += 1
            return html
        else:
            html = html.replace('<a href="donate.html">Donate Page!</a>',
                                '<a href="donate.html?from=B" style="color:blue;">Donate Page!</a>')
            counter += 1
            return html
    else:   
        if A_val >= B_val:
            with open("index.html") as f:
                html = f.read()
                versionA = html.replace('<a href="donate.html">Donate Page!</a>',
                                        '<a href="donate.html?from=A" style="color:red;">Donate Page!</a>')
                return versionA
        else:
            with open("index.html") as f:
                html = f.read()
                versionB = html.replace('<a href="donate.html">Donate Page!</a>',
                                        '<a href="donate.html?from=B" style="color:blue;">Donate Page!</a>')
                return versionB

    


@app.route("/donate.html")
def donate():
    args = dict(request.args)  
    if args.get("from") == 'A':
        global A_val
        A_val += 1
    if args.get("from") == 'B':
        global B_val
        B_val += 1
    with open("donate.html") as f:
        html = f.read()
    return "<h1>Donate Page</h1>"+html


@app.route('/browse.html')
def show_table():
    df = pd.read_csv ('main.csv')
    return "<h1>Table</h1>"+df.to_html()


# check  {ip1 : time1 , ip2 : time2 , ... }
check = dict()
@app.route('/browse.json')
def goaway():
    global check
    # TODO: limit on a per-person basis
    if request.remote_addr not in check:
        df = pd.read_csv ('main.csv')  
        check[request.remote_addr] = time.time()
        return df.to_dict()
    else:        
        if time.time() - check.get(request.remote_addr) > 60:
            df = pd.read_csv ('main.csv')       
            return df.to_dict()
        else:
            html = "too many requests, come back later"
            return Response(html, status=429,
                                  headers={"Retry-After": 60})



@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"[^@]+@[^@]+\.[^@]+", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
            global num_subscribed
            num_subscribed += 1
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify(f'Wrong email address format, please double check!') # 3



@app.route('/dashboard_1.svg')
def gen_svg1():
    hp = []
    ac = []
    args = dict(request.args)
    fig, ax = plt.subplots(figsize = (8,5))
    data = pd.read_csv ('main.csv')
    cl = data['Cylinders']
    f = StringIO()
    
    if args.get('parm')=='Acceleration':
        hp = data['Horsepower']
        ac = data['Acceleration']
        scat = ax.scatter(cl,hp, c=ac, cmap = 'viridis')
        ax.set_xlabel("Number of Cylinders")
        ax.set_ylabel("Horsepower")        
        fig.colorbar(scat, label="Acceleration(m/s)")
        plt.tight_layout()
        fig.savefig(f, format = "svg")
        plt.close() 
    else:
        hp = data['Horsepower']
        ax.scatter(cl,hp)
        ax.set_xlabel("Number of Cylinders")
        ax.set_ylabel("Horsepower")
        plt.tight_layout()
        fig.savefig(f, format = "svg")
        plt.close()
        
    svg = f.getvalue()
    hdr = {"Content-Type":"image/svg+xml"}
    return Response(svg, headers = hdr)
    

    
@app.route('/dashboard_2.svg')
def gen_svg2():
    fig, ax = plt.subplots(figsize = (8,5))
    data = pd.read_csv ('main.csv')
    dic = dict()
    test = data['Cylinders']

    for i in test:
        if i in dic:
            dic[i] = dic[i] + 1
        else:
            dic[i] = 1

    d1 = []
    d2 = []
    for i in dic:
        d1.append(i)
        d2.append(dic[i])
    
    f = StringIO()
    ax = plt.bar(d1,d2)
    plt.xlabel("Number of Cylinders")
    plt.ylabel("Number of Cars")
    
    plt.tight_layout()
    fig.savefig(f, format = "svg")
    plt.close() 
    
    svg = f.getvalue()
    hdr = {"Content-Type":"image/svg+xml"}
    return Response(svg, headers = hdr)
    
    



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.