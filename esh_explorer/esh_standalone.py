print("ESH Standalone")

import sys
import re
import os
import csv
import json
import time
import requests
from flask import Flask
from flask import request

app = Flask(__name__)

#response = requests.get("https://google.com")
response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_tree_top_descriptions")
TREE_TOP_DESCRIPTIONS = response.json()


response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_esh_fulls")
ESH_FULLS = response.json()



response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_r_section_descriptions")
R_SECTION_DESCRIPTIONS = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_descriptions")
DESCRIPTIONS = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_full_grouper_values")
FULL_GROUPER_VALUES = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_esh_children")
CHILDREN,PARENTS = response.json()


ESH_PRIMARY = "34d96442-3799-4dbc-8551-1d2942c81c08"
SECTION_NAMES = list(R_SECTION_DESCRIPTIONS.keys())
SECTION_NAMES.sort()
    
def bolden(code):
    return "#m" + str(code) + " {\n  font-weight: bold;\n  color: red\n}\n\n" 

def yellowen(code):
    return "#m" + str(code) + " {\n  font-weight: bold;\n  background-color: yellow\n}\n\n" 

def bolden_parents(codes,boldened):
    outstring = ""
    for code in codes:
        if code in boldened:
            continue
        outstring += bolden(code)
        if code in PARENTS:
            outstring += bolden_parents(PARENTS[code],boldened)
        boldened.append(code)
    return outstring

def yellowen_parents(codes,yellowened):
    outstring = ""
    for code in codes:
        if code in yellowened:
            continue
        outstring += yellowen(code)
        if code in PARENTS:
            outstring += yellowen_parents(PARENTS[code],yellowened)
        yellowened.append(code)
    return outstring


    
def li(description,indent=0):
  return " " * indent + "<li>\n" + description + " " * indent + "</li>\n"

def span(code,inbed,indent=0):
    if indent == 0:
        return " " * indent + "<span class=\"box check-box\" id=\"m" + code + "\">" + inbed + "</span>\n"
    return " " * indent + "<span class=\"box\" id=\"m" + code + "\">" + inbed + "</span>\n"

def ul(code,inbed, indent=0):
    return " " * indent + "<ul class=\"nested\" id=\"n" + code + "\">\n" + inbed + " " * indent + "</ul>\n" 

def create_tree(code,indent=0):
  subs = "" 
  description = DESCRIPTIONS[code]
    
  if code in CHILDREN:
     childs = list(CHILDREN[code])
     childs.sort()
     for child in childs:
        subs += create_tree(child,indent + 4)

  if subs:
    subs = ul(code,subs,indent+4)
    return li(span(code,description,indent+4) + subs,indent+2)
  else:
    return " " * (indent + 2) + "<li id=\"m" + code + "\"><button class=\"button\" id=\"m" + code + "\" type=\"submit\" value=\"" + code +"\" name=\"grouper_name\">" + description + "</button></li>\n"

BIG_STRING = create_tree("3995585")

ESH_TEMPLATE = ''' 

<!DOCTYPE html>
<html>
<head>
		<title>ESH Explorer</title>
		<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1, maximum-scale=1">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<style>
ul, #myUL {
  list-style-type: none;
}

#myUL {
  margin: 0;
  padding: 0;
}

input[type=submit] {
  border: none;
  text-decoration: none;
  cursor: pointer;
}

BBBBOOOOLLLLDDDD

.button {
  border: none;
  outline: none; 
  cursor: pointer;
}

td, th {
  white-space: nowrap;
}

.box {
  cursor: pointer;
  -webkit-user-select: none; /* Safari 3.1+ */
  -moz-user-select: none; /* Firefox 2+ */
  -ms-user-select: none; /* IE 10+ */
  user-select: none;
}

.box::before {
  content: "\\25B6 ";
  color: black;
  display: inline-block;
  margin-right: 6px;
}

.check-box::before {
  content: "\\25BC "; 
  color: black;
}

.nested {
  display: none;
}

.active {
  display: block;
}

div.mycontainer {
  width:100%;
  overflow:auto;
}

div.search_panel {
  width:450px;
  overflow:auto;
}
div.bottom_panel {
	display:flex;
}

div.tree_panel {
	width: 350px;
}

div.grouper_name
{
  color: red;
  font-size: x-large;
}

div.grouper
{
	display: block;
}
div.groupers
{
	height: 100%;
	border-style: solid;
}
div.event_sets
{
	border-style: solid;
	display: block;
}
div.event_set
{
	border-style: solid;
	display: flex;
}
div.event_set_snomeds
{
	border-style: solid;
	display:flex;
}
div.event_set_powerforms
{
	border-style: solid;
	display:flex;
}
div.event_set_details
{
	border-style: solid;
	display: block;
}
div.event_set_snomed
{
	width: 300px;
	border-style: solid;
	display: flex;
}
div.event_set_powerform
{
	width: 300px;
	border-style: solid;
	display: flex;
}
div.event_set_name
{
	width: 300px;
	background-color: MintCream;
}

div.buttons
{
	display: block;
}

body, html {
				font-family: helvetica;
				font-size: 14px;
				height: 100%;
				position: absolute;
}

			

</style>
</head>
<header>
	<h1>ESH Explorer</h1>
</header>
<body>
The ESH Explorer is a tool for finding the proper location for a newly proposed Event Set within the
Event Set Hierarchy and to discover if there is already an existing Event Set that covers the same
basic concept.</br></br>
            

  <form action="/" method="post">
    _HIDDEN_DETAILS_
    <div style="background-color: Gainsboro;" class="search_panel">
        <label for="text">Possible New ESH:</label>
        <input type="text" name="text" style="width: 300px;" id="text" name="description" value="TEST"><br><br>
	        <div style="display: flex;">
 		        <label for="subtree" style="display: inline-block; width: 50%;">ESH Subpart:
  		            <select name="subtree" id="subtree">
		                _SUBTREES_
  		            </select>
		        </label>
	        </div>
        <div style="display: flex;">
            <div id="powerforms_to_select" style="display: flex; gap: 10px;">
                <div style="display: block;">
                    <select id="rightValues" style="display: block; width: 200px" size="10" multiple>
                        _UNSELECTED_POWERFORM_SECTIONS_
                    </select>
                    <input type="button" style="display: block; width: 200px; white-space: normal;" id="btnLeft" value="Select Associated Powerform Sections" />
                </div>
                <div style="display: block;">
                    <select id="leftValues" style="display: block; width: 200px" size="10" name="leftValues" multiple>_SELECTED_POWERFORM_SECTIONS_</select>
                    <button type="submit" style="display: block; width: 200px" name="clear" value="clear">Clear Selected Powerforms</button>
                </div>
            </div>
        </div>
		<div style="display: block;">
           	<button style="display: block;" type="submit">Find Suggested Groupers and Possible Event Set Duplicates</button>
		</div>
      </div>
    </div">
  </form>
    <br>
    <div>
	 <input type="button" class="mybutton" onclick="toggle_esh()" value=">>">
	 <input type="button" class="mybutton" style="display: none;" onclick="toggle_esh()" value="<<">
    </div>	
    <div>
    <h2>Identified Possible Groupers</h2>
        To use links to web protege please go <a target=\"blank\" href=\"https://osler.compbio.buffalo.edu/webprotege/#projects/34d96442-3799-4dbc-8551-1d2942c81c08/perspectives/69df8fa8-4f84-499e-9341-28eb5085c40b\">here</a> to log in. 
    <br/>
    <table><tr><th>webprotege link</th><th>confidence</th><th>hierarchy</th></tr>
esh_details
</table>
    (Possible groupers appear in red text below.)
    </div>
    <div>
        <h2>Identified Possible Duplicates</h2>
        <table>
        <tr><th>display button</th><th>webprotege link</th><th>hierarchy</th></tr>
_DUPES_
        </table>
    </div>
    <br>
    <button onclick="toggle_bottom()" style="display:flex" class="bottom_panel" >Hide Analysis</button>
    <button onclick="toggle_bottom()" style="display:none" class="bottom_panel" >Show Analysis</button>
    <div class="bottom_panel">
        <div class="display_panel">
            _ESH_
        </div class="display_panel">
    </div class="bottom_panel">
    <div>

  <script>

    _ADDITIONAL_SCRIPT_
var toggler = document.getElementsByClassName("box");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("check-box");
  });
}
$("#btnLeft").click(function () {
    var selectedItem = $("#rightValues option:selected");
    $("#leftValues").append(selectedItem);
});

$("#btnRight").click(function () {
    var selectedItem = $("#leftValues option:selected");
    $("#rightValues").append(selectedItem);
});

$("#rightValues").change(function () {
    var selectedItem = $("#rightValues option:selected");
    $("#txtRight").val(selectedItem.text());
});

$("#leftValues").change(function () {
    var selectedItem = $("#leftValues option:selected");
    $("#txtLeft").val(selectedItem.text());
});

function toggle_esh(){
	document.querySelectorAll('.mybutton').forEach(function(el) {
		if (el.style.display == 'none') {
   			el.style.display = 'flex';
		}
		else{
   			el.style.display = 'none';
		}
	});
}

function toggle_bottom(){
    const elements = document.getElementsByClassName('bottom_panel');
    for (let el of elements) {
        if (el.style.display == 'none') {
            el.style.display = 'flex';
        } 
        else{
          el.style.display = 'none';
        }
    }
}

function show_grouper(elementId){
    const elements = document.getElementsByClassName('grouper');
    for (let el of elements) {
        el.style.display = 'none';
    }
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'block';
    }

}


  </script>
</body>
</html>
'''

GROUPER_TEMPLATE = '''
    <div id="__ID__" style="display: _STYLE_" class="grouper">
        <div class="grouper_name">GROUPER_NAME</div>
        <div class="event_sets">
            EVENT_SETS
        </div>
    </div>
'''

EVENT_SET_TEMPLATE =''' 
    			<div class="event_set">
        			<div class="event_set_name" id="EVENT_SET_CODE">EVENT_SET_NAME</div>
				    <div class="event_set_details">
					    <div class="event_set_snomeds">
                            EVENT_SET_SNOMEDS
                        </div>
					    <div class="event_set_powerforms">
                            EVENT_SET_POWERFORMS
					    </div>
                    </div>
                </div>
'''

EVENT_SET_SNOMED_TEMPLATE = '''<div class="event_set_snomed">EVENT_SET_SNOMED</div>'''
EVENT_SET_SNOMED_TEMPLATE_GREEN = '''<div class="event_set_snomed" style="background-color: lightgreen">EVENT_SET_SNOMED</div>'''
EVENT_SET_POWERFORM_TEMPLATE = '''<div class="event_set_powerform">EVENT_SET_POWERFORM</div>'''
EVENT_SET_POWERFORM_TEMPLATE_BLUE = '''<div class="event_set_powerform" style="background-color: lightblue">EVENT_SET_POWERFORM</div>'''

def convert_grouper_certainties(groupers_list):
    output = []
    total_certainty = 0
    for grouper_entry in groupers_list:
        total_certainty += grouper_entry[1]

    
    for grouper_entry in groupers_list:
        i = round(100 * grouper_entry[1]/total_certainty)
        output.append([grouper_entry[0],i])
    return output


def get_groupers_list(groupers_list,sub_tree):
    output = ""
    corrected_groupers_list = convert_grouper_certainties(groupers_list)
    for grouper_entry in corrected_groupers_list:
        grouper = grouper_entry[0]
        grouper_value = str(grouper_entry[-1])
        print(grouper_value)
        subtree_and_results = None
        subtree_match = None
        for grouper_spec in FULL_GROUPER_VALUES[grouper]:
            if sub_tree in grouper_spec:
                subtree_match = grouper_spec
                if "ALL RESULT SECTIONS" in grouper_spec:
                    subtree_and_results = grouper_spec
        p = None
        if subtree_and_results:
            p = subtree_and_results
        else:
            o = subtree_match
        o = p[1:][::2]
        o[0] = o[0] + " [" +  p[0] + "]"
        l = " < ".join(o)
        o.reverse()
        m = " > ".join(o)
        link = "<a onclick=\"show_grouper('" + p[0] + "')\" target=\"blank\" href=\"https://osler.compbio.buffalo.edu/webprotege//#projects/" + ESH_PRIMARY + "/perspectives/69df8fa8-4f84-499e-9341-28eb5085c40b?selection=Class(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/01/P0630%23EC" + p[0] + "%3E)\">" + p[0] + "</a>"
        output += "<tr>"
        output += "<th>" + link + "</th><th>" + grouper_value + "</th><th style=\"text-align: left;\"><div style=\"margin: 4px 2px; border:none; background-color:AliceBlue; cursor:pointer\" class=\"mybutton\" >" + l + "</div>"
        output += "<div style=\"display: none; margin: 4px 2px; border:none; background-color:AliceBlue; cursor:pointer\" class=\"mybutton\" type=\"submit\">" + m + "</div></th>\n"
        output += "</tr>"
        
    return output


def get_dupes_list(dups,subtree):
    output = ""
    groupers = []
    for dup in dups:
        if not dup in ESH_FULLS:
            continue
        esh_full = ESH_FULLS[dup]
        subtree_match = None
        subtree_and_results = None
        for esh_spec in esh_full:
            if subtree in esh_spec:
                subtree_match = esh_spec
                if "ALL RESULT SECTIONS" in esh_spec:
                    subtree_and_results = esh_spec
        p = None
        if subtree_and_results:
            p = subtree_and_results
        else:
            p = subtree_match
        grouper = p[4]
        o = p[1:][::2]
        o[0] = o[0] + " [" +  p[0] + "]"
        l = " < ".join(o)
        o.reverse()
        m = " > ".join(o)
        link = "<a onclick=\"show_grouper('" + p[4]  + "')\" target=\"blank\" href=\"https://osler.compbio.buffalo.edu/webprotege//#projects/" + ESH_PRIMARY + "/perspectives/69df8fa8-4f84-499e-9341-28eb5085c40b?selection=Class(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/01/P0630%23EC" + p[0] + "%3E)\">" + p[0] + "</a>"
        output += "<tr>"
        output += "<th>" + link + "</th><th style=\"text-align: left;\"><div style=\"margin: 4px 2px; border:none; background-color:HoneyDew; cursor:pointer\" class=\"mybutton\" >" + l + "</div>\n"
        output += "<div style=\"display: none; margin: 4px 2px; border:none; background-color:HoneyDew; cursor:pointer\" class=\"mybutton\" >" + m + "</div></th>"
        output += "</tr>"
    
    return [output,groupers]

HIDDEN_SUBTREE = '''<input type="hidden" name="hidden_subtree" value="VALUE">'''

def get_subtree_options(selected_tree):
    output = ""
    tree_top_descriptions = TREE_TOP_DESCRIPTIONS 
    if selected_tree:
        output += "<option id=\"" + tree_top_descriptions[selected_tree] + "\">" + selected_tree + "</option>"
    if selected_tree != "CLINICAL INFO":
        output += "<option id=\"" + tree_top_descriptions["CLINICAL INFO"] + "\">CLINICAL INFO</option>"
    if selected_tree != "ALL RESULT SECTIONS":
        output += "<option id=\"" + tree_top_descriptions["ALL RESULT SECTIONS"] + "\">ALL RESULT SECTIONS</option>"
    if selected_tree != "ALL OCF EVENT SETS":
        output += "<option id=\"" + tree_top_descriptions["ALL OCF EVENT SETS"] + "\">ALL OCF EVENT SETS</option>"
    if selected_tree != "ALL DOCUMENT SECTIONS":
        output += "<option id=\"" + tree_top_descriptions["ALL DOCUMENT SECTIONS"] + "\">ALL DOCUMENT SECTIONS</option>"

    tdescriptions = list(tree_top_descriptions.keys())
    tdescriptions.sort()
        
    for description in tdescriptions:
        if not description in ["CLINICAL INFO","ALL RESULT SECTIONS","ALL OCF EVENT SETS","ALL DOCUMENT SECTIONS",selected_tree]:
            output += ("<option id=\"" + tree_top_descriptions[description] + "\">" + description + "</option>")

    h = HIDDEN_SUBTREE.replace("VALUE","CLINICAL_INFO")
    if selected_tree:
        h = HIDDEN_SUBTREE.replace("VALUE",selected_tree)
    return output, h

def get_selected_and_unselected_options(pfs_names):
    selected_options = ""
    hidden_selected = ""
    for name in pfs_names:
        selected_options += "<option id=\"" + R_SECTION_DESCRIPTIONS[name] + "\">" + name + "</option>"   
        hidden_selected += "<input type=\"hidden\" name=\"hidden_selected\" value=\"" + name + "\">"
    unselected_options = ""
    for name in SECTION_NAMES:
        if not name in pfs_names:
            unselected_options += "<option id=\"" + R_SECTION_DESCRIPTIONS[name] + "\">" + name + "</option>"   
    return selected_options, unselected_options,hidden_selected

def get_pfs_codes(pfs_names):
    output = []
    for name in pfs_names:
        output.append(R_SECTION_DESCRIPTIONS[name])
    return output
        

@app.route("/",methods=["GET","POST"])
def esh_search():
    text = "Blood Pressure"
    post_obj = {}
    post_obj["text"] = text
    pf_names = []
    hidden_names = []
    hidden_subtree = ""
    clear = False
    subtree = "CLINICAL INFO"
    maxn = 10 
    
    if "text" in request.form:
        text = request.form["text"]
        post_obj["text"] = text
    if "leftValues" in request.form:
        print(request)
        pf_names = request.form.getlist("leftValues")
        print(pf_names)
        post_obj["powerforms"] = pf_names
    if "hidden_selected" in request.form:
        hidden_names = request.form.getlist("hidden_selected")
    if "hidden_subtree" in request.form:
        hidden_subtree = request.form["hidden_subtree"]
    if "clear" in request.form:
        clear = request.form["clear"]
    if "subtree" in request.form:
        subtree = request.form["subtree"]
        post_obj["subtree"] = subtree 
    post_obj["max_response"] = maxn
    print(post_obj)
    
    print(text)
    if text == None:
        text = "Blood Pressure"
    pf_codes = []
    if clear:
        pf_names = []
    if pf_names:
        print("asdfasdfasdf")
        print(pf_names)
        pf_codes = get_pfs_codes(pf_names)
    elif hidden_names and not clear:
        pf_names = hidden_names 
        print(pf_names)
        pf_codes = get_pfs_codes(pf_names)
        
    print(subtree)
    if not subtree:
        subtree = "CLINICAL INFO"
    
    headers = {'Content-Type': 'application/json'}
    
    url = "https://halsted.compbio.buffalo.edu/anf_viewer/esh_service"
    response = requests.post(url,data=json.dumps(post_obj),headers=headers)
    j = response.json()
    groupers = j["groupers"]
    event_sets = j["event_sets"]
    dup_string, dup_groupers = get_dupes_list(event_sets,subtree)
    selected_options, unselected_options,hidden_options = get_selected_and_unselected_options(pf_names)
    subtree_options, subtree_hidden = get_subtree_options(subtree)
    hidden_options += subtree_hidden

    output_groupers = groupers[:maxn]
    esh_details = get_groupers_list(output_groupers+dup_groupers,subtree)
    bstring = BIG_STRING
    if subtree and subtree != "CLINICAL INFO":
        bstring = create_tree(tree_top_descriptions[subtree])
    
    grouper_full = None
    search_codes = []
    for result in output_groupers:
        search_codes.append(result[0])

    grouper_outputs = ""
    first = True
    for grouper in groupers:
        event_sets_out = ""
        style = ""
        if first:
            first = False
            style = "block"
        else:
            style = "none"
        grouper_code = grouper[0]
        grouper_name = DESCRIPTIONS[grouper_code] + " [" + grouper_code + "]"
        for esh_with_codes in grouper[2]:
            esh = esh_with_codes[0]
            esh_name = DESCRIPTIONS[esh]
            child_snomeds = ""
            for snomed in esh_with_codes[1][0]:
                child_snomeds += EVENT_SET_SNOMED_TEMPLATE_GREEN.replace("EVENT_SET_SNOMED",snomed)
            child_pfs = ""
            for powerform in esh_with_codes[1][2]:
                child_pfs += EVENT_SET_POWERFORM_TEMPLATE_BLUE.replace("EVENT_SET_POWERFORM",powerform)
            for powerform in esh_with_codes[1][3]:
                child_pfs += EVENT_SET_POWERFORM_TEMPLATE.replace("EVENT_SET_POWERFORM",powerform)
            event_sets_out += EVENT_SET_TEMPLATE.replace("EVENT_SET_SNOMEDS",child_snomeds).replace("EVENT_SET_POWERFORMS",child_pfs).replace("EVENT_SET_NAME",esh_name).replace("EVENT_SET_CODE","m"+esh)
        
        grouper_outputs += GROUPER_TEMPLATE.replace("EVENT_SETS",event_sets_out).replace("GROUPER_NAME",grouper_name).replace("_STYLE_",style).replace("__ID__",grouper_code)

   
    return ESH_TEMPLATE.replace("_SUBTREES_",subtree_options).replace("esh_details",esh_details).replace("TTTTRRRREEEE",bstring).replace("_DUPES_",dup_string).replace("_ADDITIONAL_SCRIPT_","").replace("_HIDDEN_DETAILS_",hidden_options).replace("TEST",text).replace("_SELECTED_POWERFORM_SECTIONS_",selected_options).replace("_UNSELECTED_POWERFORM_SECTIONS_",unselected_options).replace("BBBBOOOOLLLLDDD",yellowen_parents(event_sets,[]) + bolden_parents(search_codes,[])).replace("_ESH_",grouper_outputs)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)
