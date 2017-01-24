from flask import Flask, request, render_template, send_from_directory
from bson import json_util
import constants
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return render_template('index.html', node_names=constants.LIST_OF_NODES)

@app.route('/get_mongo_current_op/<node_name>/', methods=['GET'])
def get_mongo_current_op(node_name):
    uri = constants.ALL_NODES[node_name].get_connection_string_uri()
    print 'uri', uri
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
    return json_str

@app.route('/kill_mongo_op/<node_name>/<int:opid>/', methods=['POST'])
def kill_mongo_op(node_name, opid):
    uri = constants.ALL_NODES[node_name]
    conn = constants.MONGO_CONN.get_connection(node_name, uri)
    db = conn['admin']
    try:
        result = db.command('killOp', op=opid)
        return 'Result: ' + str(result)
    except Exception as e:
        return 'Unable to kill mongo op. Error: ' + str(e)
