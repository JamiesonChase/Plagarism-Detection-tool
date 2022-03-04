import datetime 
from flask import Flask, render_template_string, jsonify
import threading
import time
app = Flask(__name__)

global dataTime 

#
@app.route("/")
def index():
    return render_template_string("""<!DOC html>
    <html>
    <head>
     <meta http-equiv="refresh" content="0.5">
    
    <meta charset="utf-8" />
    <title>Test</title>
    </head>
    <body>
    <table class="center">
      <tr>
        <th>doc Pairs</th>
        <th>Pair Similarity</th>
      </tr>
      {% for i in newEntry %}
        <tr><th><A HREF="HTMLFiles/baseFiles/{{i[0]}}-1.html?file1={{i[3]}}&file2={{i[4]}}&rowNumber={{i[0]}}">{{i[1]}}</A></th><th>{{i[2]}}</th></tr>
    {% endfor %}
    </table>
    </body>
    </html>""", newEntry=dataTime)

@app.route('/data', methods=['POST'])
def data():
    return jsonify({'map':dataTime})

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        global dataTime
        dataTime = [[0,"c", "k", "l"]]
        i = 1
        while(1):
            dataTime.append( [i,"c", "k", "l"])
            i = i + 1
            time.sleep(1)
            


if __name__ == "__main__":
    app.run(debug=True)