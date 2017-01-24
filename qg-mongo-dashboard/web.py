from flask import Flask, request, render_template, send_from_directory
from bson import json_util
import constants
import json

print 'web started'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def test():
    return render_template('index.html', node_names=constants.LIST_OF_NODES)

@app.route('/get_mongo_current_op/<node_name>', methods=['GET', 'POST'])
def get_mongo_current_op(node_name):
    print node_name
    uri = constants.ALL_NODES[node_name]
    conn = constants.MONGO_CONN.get_connection(node_name, uri)
    db = conn['admin']
    current_ops = db.current_op()
    inprog_ops = current_ops['inprog']
    _dict = {}
    filtered_ops = []
    for op in inprog_ops:
        desc = op['desc'].lower()
        ns = op.get('ns', '').lower()
        desc_bool = 'repl' not in desc and 'sync' not in desc and 'oplog' not in desc and 'applybatch' not in desc
        ns_bool = 'local.oplog.rs' not in ns and 'admin.$cmd' not in ns
        if desc_bool and ns_bool:
            filtered_ops.append(op)
    _dict['total'] = len(inprog_ops)
    _dict['filtered'] = len(filtered_ops)
    _dict['data'] = filtered_ops
    json_str = json_util.dumps(_dict)
    _dict = json.loads(json_str)
    return render_template('index.html', node_names=constants.LIST_OF_NODES)

@app.route('/kill_mongo_op/<node_name>/<int:opid>', methods=['GET', 'POST'])
def test(node_name, opid):
    conn = constants.MONGO_CONN.get_connection(node_name)
    db = conn['admin']
    try:
        result = db.command('killOp', op=opid)
        return ('<p>Result: ' + str(result)) + '</p>')
    except Exception as e:
        return ('<p>Unable to kill mongo op. Error: ' + str(e)) + '</p>')
