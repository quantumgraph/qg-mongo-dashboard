// Global variables
var PASSWORD = "qg123";
var MONGO_DATA;

$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function mongoCurrentOp(name) {
    var url = "/get_mongo_current_op/" + name + "/";
    var headerTxt = name + " CurrentOp";
    $.get(url, function(data, status) {
        injectHTMLForMongoOps(name, data, headerTxt);
    });
}

function injectHTMLForMongoOps(name, data, headerTxt) {
    var json = JSON.parse(data);
    var total_count = json['total'];
    var filtered_count = json['filtered'];
    var json_data = json['data'];

    $("#mongo_table")[0].innerHTML = '<div id="header"></div><div id="table"></div><div id="kill_status"></div><div id="header_2"></div><div id="json"></div>';
    var utc_timestamp = new Date().getTime();
    utc_timestamp = Math.ceil(utc_timestamp / 1000);
    var header_text = '<p>Timestamp: ' + utc_timestamp + '</p><h3>' + headerTxt + ':</h3>';
    header_text = header_text + '<p>Total ops found: ' + total_count + '<br>Showing filtered ops: ' + filtered_count + '</p>';
    $("#header")[0].innerHTML = header_text;
    $("#header_2")[0].innerHTML = '<h3>Detailed Stats:</h3>';

    var table_html = '\
      <div>\
        <table class="table table-bordered" id="mongo_ops_table">\
          <thead>\
            <tr>\
              <th>opid</th>\
              <th>client</th>\
              <th>appName</th>\
              <th>ns</th>\
              <th>query</th>\
              <th>op</th>\
              <th>secs running</th>\
            </tr>\
          </thead>\
          <tbody id="table_body"></tbody>\
        </table>\
      </div>';
    $("#table")[0].innerHTML = table_html;
    var tbody_html = "";
    json_data.forEach(function(each_data) {
        var opid = each_data.opid || "undefined";
        var kill_op_btn = '<button onclick="killMongoOp(\'' + name + "', " + opid + ')" type="button" class="btn btn-default btn-sm">kill Op</button>';
        var client = each_data.client || "undefined";
        var appName = each_data.appName || "undefined";
        client = client.split(":")[0];
        var ns = each_data.ns || "undefined";
        var query = JSON.stringify(each_data.query) || "undefined";
        var op = each_data.op || "undefined";
        var secs_running = JSON.stringify(each_data.secs_running) || "undefined";
        var tr_html = '<tr><td>' + opid + '<br>' + kill_op_btn + '</td><td>' + client + '</td><td>' + appName + '</td><td>' + ns + '</td>';
        tr_html = tr_html + '<td>' + query + '</td><td>' + op + '</td><td>' + secs_running + '</td></tr>';
        tbody_html = tbody_html + tr_html;
    });
    $("#table_body")[0].innerHTML = tbody_html;

    var div_json = $("#json")[0];
    var b = new PrettyJSON.view.Node({ el: div_json, data: json_data });
    b.expandAll();
}

function killMongoOp(name, opid) {
    var disp_txt = "You are about to kill the query with opid: " + opid;

    var pass = prompt(disp_txt);
    if (pass === PASSWORD) {
        var url = "/kill_mongo_op/" + name + "/" + opid + "/";
        $.ajax({
            type: "POST",
            url: url,
            contentType: 'application/json; charset=utf-8',
            dataType: 'text',
            data: JSON.stringify({ "opid": +opid }),
            processData: false,
            success: function(data) {
                mongoCurrentOp(name);
                setTimeout(function() {
                    $("#kill_status")[0].innerHTML = '<p>' + data + '</p>';
                }, 1500);
            },
            error: function(data) {
                console.log("error:", data);
                $("#kill_status")[0].innerHTML = '<p>' + 'Error occured, check console for the details' + '</p>';
            }
        });
    } else {
        alert("You have entered wrong password");
    }
}
