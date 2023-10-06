from flask import Flask
from app.actionParser.actionParser import Nfa
from app.actionParser.actionParser import ActionParser

app = Flask(__name__)
nfa = Nfa()

@app.route('/getActionByString', methods=['GET'])
def get_action_by_string(action_string):
    print(action_string)
    string = nfa.parseActionDescription(action_string)
    return app.jsonify(string)

@app.route('/api/greet/<name>', methods=['GET'])
def greet(name):
    return f'Hallo, {name}! Wie geht es dir?'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

get_action_by_string('afkjs(shdj:\'sdf\')')