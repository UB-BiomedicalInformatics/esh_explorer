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

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
app = Flask(__name__)


response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_tree_top_descriptions")
TREE_TOP_DESCRIPTIONS = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_placeholders")
PLACEHOLDERS = response.json()


response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_esh_fulls")
ESH_FULLS = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_esh_to_powerforms_map")
esh_to_powerforms_map = response.json()
esh_names = {} 


response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_powerform_to_eshs_map")
powerform_to_eshs_map = response.json()

if "2654125371" in powerform_to_eshs_map:
    print(powerform_to_eshs_map["2654125371"] )
    print("asdfasdfasd")

if "2654125371" in esh_to_powerforms_map:
    print(esh_to_powerforms_map["2654125371"] )
    print("asdfasdfadfasdfasdfasdfd")

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_r_section_descriptions")
R_SECTION_DESCRIPTIONS = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_section_descriptions")
SECTION_DESCRIPTIONS = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_descriptions")
DESCRIPTIONS = response.json()

for code in esh_to_powerforms_map.keys():
    if code in DESCRIPTIONS:
        esh_names[DESCRIPTIONS[code]] = code

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_full_grouper_values")
FULL_GROUPER_VALUES = response.json()

response = requests.get("https://halsted.compbio.buffalo.edu/anf_viewer/get_esh_children")
CHILDREN,PARENTS = response.json()

#https://osler.compbio.buffalo.edu/webprotege//?fragment=projects%2F23c0f833-978e-414e-ac25-42f570f4b090%2Fperspectives%2F69df8fa8-4f84-499e-9341-28eb5085c40b%3Fselection%3DClass(%253Chttp%3A%2F%2Fwww.semanticweb.org%2ForacleRDFBot%2Fontologies%2F2026%2F06%2FP0630%2523EC3995585%253E)
ESH_PRIMARY = "23c0f833-978e-414e-ac25-42f570f4b090"
SECTION_NAMES = list(R_SECTION_DESCRIPTIONS.keys())
SECTION_NAMES.sort()

LINK_TARGET_TEMPLATE = "https://osler.compbio.buffalo.edu/webprotege//?fragment=projects%2F" + ESH_PRIMARY + "%2Fperspectives%2F69df8fa8-4f84-499e-9341-28eb5085c40b%3Fselection%3DClass(%253Chttp%3A%2F%2Fwww.semanticweb.org%2ForacleRDFBot%2Fontologies%2F2026%2F06%2FP0630%2523EC" + "_CODE_" + "%253E)"
    

ESH_TEMPLATE = ''' 

<!DOCTYPE html>
<html>
<head>
		<title>ESH Explorer</title>
		<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1, maximum-scale=1">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0/dist/css/select2.min.css" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0/dist/js/select2.min.js">
</script>
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
</header>
<body>
    <button onclick="toggle_whole()" style="display:block" class="whole_panel" >Hide Search</button>
    <button onclick="toggle_whole()" style="display:none" class="whole_panel" >Show Search</button>
    <div class="whole_panel" style="display:block">
	<h1>ESH Explorer</h1>
    <div style="width:450px;overflow:auto;">
The ESH Explorer is a tool for finding the proper location for a newly proposed Event Set within the
Event Set Hierarchy and to discover if there is already an existing Event Set that covers the same
basic concept.</br>
<a target="blank" href="https://osler.compbio.buffalo.edu/webprotege//?fragment=projects%2F23c0f833-978e-414e-ac25-42f570f4b090%2Fperspectives%2F69df8fa8-4f84-499e-9341-28eb5085c40b%3Fselection%3DClass(%253Chttp%3A%2F%2Fwww.semanticweb.org%2ForacleRDFBot%2Fontologies%2F2026%2F06%2FP0630%2523EC3995585%253E)">Link To WebProtege</a>
    </div>
</br>
</br>
  <form id="search_form" action="javascript:void(0)" onsubmit="populate_search_results();">
    <div style="background-color: Gainsboro;" class="search_panel">
        <label for="text">Possible New ESH:</label>
        <input type="text" name="text" style="width: 300px;" id="text" name="description" value="TEST"><br><br>
	        <div style="display: flex;">
 		        <label for="subtree" style="display: inline-block; width: 50%;">ESH Subpart:
  		            <select class="js-example-basic-single" name="subtree" id="subtree">
		                _SUBTREES_
  		            </select>
		        </label>
	        </div>
        <div style="display: flex;">
 		    <label for="powerforms" style="display: inline-block; width: 50%;">Powerform Sections:
            <select id="powerforms" class="js-example-basic-multiple" multiple="multiple" name="powerforms">
                _UNSELECTED_POWERFORM_SECTIONS_
            </select>
        </div>
		<div style="display: block;">
           	<input onclick="populate_search_results();" style="display: block;" type="button" value="Find Suggested Groupers and Possible Event Set Duplicates">
		</div>
      </div>
    </div">
  </form>
    <br>
    <div>
	 <input type="button" class="mybutton" onclick="toggle_esh()" value=">>">
	 <input type="button" class="mybutton" style="display: none;" onclick="toggle_esh()" value="<<">
    </div>	
    <h3 style="display:flex; column-gap:20px;"><div>Search Term:  </div> <div id="search_term"></div></h3>
    <div>
    <h2>Identified Possible Groupers</h2>
    <br/>
    <div id="groupers_panel">
    </div>
</table>
    (Possible groupers appear in red text below.)
    </div>
    <div>
        <h2>Identified Possible Duplicates</h2>
        <div id="dups_panel">
        </div>
    </div>
    <br>
    <button onclick="toggle_bottom()" style="display:none" class="bottom_panel" >Hide Analysis</button>
    <button onclick="toggle_bottom()" style="display:flex" class="bottom_panel" >Show Analysis</button>
    <div class="bottom_panel" style="display:none;">
        <div id="display_panel" class="display_panel">
        </div class="display_panel">
    </div>
  </div>
  <button onclick="toggle_powerform()" style="display:none" class="powerform_panel" >Hide Powerform View</button>
  <button onclick="toggle_powerform()" style="display:flex" class="powerform_panel" >Show Powerform View</button>
  <div class="powerform_panel" style="display:none;">
    <div style="display: flex;" >
        _SECTIONS_DATALIST_
        _ESHS_DATALIST_
        <div>
            <table>
                <tr>
                    <th>KEY:</th>
                    <th style="background-color:lightgreen">EVENT SETS</th>
                    <th style="background-color:lightblue">POWERFORMS</th>
                </tr>
            </table>
        </div>
    </div>
    <table> 
        <tbody id="powerform_eshs">
        </tbody>
    </table>
  </div>

  <script>

$(document).ready(function() {
    $('.js-example-basic-multiple').select2();
});
$(document).ready(function() {
    $('.js-example-basic-single').select2();
});


var toggler = document.getElementsByClassName("box");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("check-box");
  });
}

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

function toggle_whole(){
    const elements = document.getElementsByClassName('whole_panel');
    for (let el of elements) {
        if (el.style.display == 'none') {
            el.style.display = 'block';
        } 
        else{
          el.style.display = 'none';
        }
    }
}

function toggle_powerform(){
    const elements = document.getElementsByClassName('powerform_panel');
    for (let el of elements) {
        if (el.style.display == 'none') {
            el.style.display = 'block';
        } 
        else{
          el.style.display = 'none';
        }
    }
}

function show_grouper(elementId){
   
    const e = String(elementId)
    const elements = document.getElementsByClassName('grouper');
    for (let el of elements) {
        el.style.display = 'none';
    }
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = 'block';
    }

}

async function show_selected_powerform(){
    const form = document.getElementById('powerformform');
    const data = new FormData(form);
    const selectedValue = data.get('sections');
    const url = '/eshexplorer/get_powerform_info';
    const req = { method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({powerform: selectedValue,row_number:0})
                }
                    
    try{
        const response = await fetch(url,req);
        const restext = await response.text();
        var mydiv = document.getElementById('powerform_eshs');
        mydiv.innerHTML = restext
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function populate_search_results(){
    const form = document.getElementById('search_form');
    const data = new FormData(form);
    const text = data.get('text');
    const powerforms = data.getAll('powerforms');
    const subtree = data.get('subtree');
    const the_body = JSON.stringify({'powerforms': powerforms,'text':text,'subtree':subtree});
    const url = '/eshexplorer/display_duplicates';
    const req = { method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: the_body
                }
    try{
        const response = await fetch(url,req);
        const restext = await response.text();
        var mydiv = document.getElementById('dups_panel');
        mydiv.innerHTML = restext;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
   
   const display_grouper_url= '/eshexplorer/display_groupers';
    try{
        const response = await fetch(display_grouper_url,req);
        const restext2 = await response.text();
        var groupers_panel = document.getElementById('groupers_panel');
        groupers_panel.innerHTML = restext2;
    } catch (error) {
        console.error('Error fetching data:', error);
    }

    const grouper_analysis_url = '/eshexplorer/display_grouper_analysis';
    try{
        const response = await fetch(grouper_analysis_url,req);
        const restext3 = await response.text();
        var display_panel = document.getElementById('display_panel');
        display_panel.innerHTML = restext3;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
    var search_term_place = document.getElementById('search_term');
    search_term_place.innerHTML = text;


    
}

async function show_selected_esh(){
    const form = document.getElementById('eshsform');
    const data = new FormData(form);
    const selectedValue = data.get('teshs');
    const url = '/eshexplorer/get_esh_info';
    const req = { method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({esh_name: selectedValue,row_number:0})
                }
                    
    try{
        const response = await fetch(url,req);
        const restext = await response.text();
        var mydiv = document.getElementById('powerform_eshs');
        mydiv.innerHTML = restext
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function show_selected_powerform_by_name(powerform_id,thelink){
    j = {};
    if (thelink != null) {
        
    const thencell = thelink.parentElement;
    const therow = thencell.parentElement;
    const thecells = Array.from(therow.cells);
    for (const thecell of thecells){
       thecell.style.removeProperty('border-style'); 
       thecell.style.removeProperty('border-radius'); 
       thecell.style.removeProperty('border-width'); 
    }
    thencell.style.borderStyle = 'solid';
    thencell.style.borderRadius = '15px';
    thencell.style.borderWidth = '3px';
    while (therow.nextElementSibling) {
        therow.nextElementSibling.remove();
    }
        j = {powerform:powerform_id};;
    } else {
        j = {powerform:powerform_id,row_number:0};
    }

    
    const url = '/eshexplorer/get_powerform_info';
    const req = { method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(j)
                }
                    
    try{
        const response = await fetch(url,req);
        const restext = await response.text();
        var mydiv = document.getElementById('powerform_eshs');
        if (thelink == null) {
            mydiv.innerHTML = restext
        } else {
            mydiv.innerHTML += restext
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function show_selected_esh_by_id(esh_id,thelink){
    j = {};
    if (thelink != null) {
        
        const thencell = thelink.parentElement;
        const therow = thencell.parentElement;
        const thecells = Array.from(therow.cells);
        for (const thecell of thecells){
            thecell.style.removeProperty('border-style'); 
            thecell.style.removeProperty('border-radius'); 
            thecell.style.removeProperty('border-width'); 
        }
        thencell.style.borderStyle = 'solid';
        thencell.style.borderRadius = '15px';
        thencell.style.borderWidth = '3px';
        while (therow.nextElementSibling) {
            therow.nextElementSibling.remove();
        }
        j = {esh:esh_id};
    } else {
        j = {esh:esh_id,row_number:0};
    }
    
    

    const url = '/eshexplorer/get_esh_info';
    const req = { method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(j)
                }
                    
    try{
        const response = await fetch(url,req);
        const restext = await response.text();
        var mydiv = document.getElementById('powerform_eshs');
        if (thelink == null) {
            mydiv.innerHTML = restext
        } else {
            mydiv.innerHTML += restext
        }
    } catch (error) {
        console.error('Error fetching data:', error);
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
DUPES_TABLE_TEMPLATE = '''
        <table>
            <tr><th>link</th><th>hierarchy</th></tr>
            _DUPES_
        </table>
'''

GROUPERS_TABLE_TEMPLATE = '''
    <table><tr><th>link</th><th>confidence</th><th>hierarchy</th></tr>
        _GROUPERS_
    </table>
    '''

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
        link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",p[0])
        link = "<a onclick=\"show_grouper(" + p[0] + ")\" target=\"blank\" href=\"" + link_target + "\">" + p[0] + "</a>"
        output += "<tr>"
        output += "<th>" + link + "</th><th>" + grouper_value + "</th><th style=\"text-align: left;\"><div style=\"margin: 4px 2px; border:none; background-color:AliceBlue; cursor:pointer\" class=\"mybutton\" >" + l + "</div>"
        output += "<div style=\"display: none; margin: 4px 2px; border:none; background-color:AliceBlue; cursor:pointer\" class=\"mybutton\" type=\"submit\">" + m + "</div></th>\n"
        output += "</tr>"
        
    return output

#/(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/01/P0630%23EC" + p[0] + "%3E)\">" + p[0] + "</a>"
#/(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/01/P0630%23EC3995585%3E)">Link To WebProtege</a>i
#/(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/06/P0630%23EC472145007%3E)
#https://osler.compbio.buffalo.edu/webprotege//#projects/23c0f833-978e-414e-ac25-42f570f4b090/perspectives/69df8fa8-4f84-499e-9341-28eb5085c40b?selection=Class(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/06/P0630%23EC366660175%3E)
#https://osler.compbio.buffalo.edu/webprotege//#projects/23c0f833-978e-414e-ac25-42f570f4b090/perspectives/69df8fa8-4f84-499e-9341-28eb5085c40b?selection=Class(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/01/P0630%23EC366660175%3E)
#https://osler.compbio.buffalo.edu/webprotege//#projects/23c0f833-978e-414e-ac25-42f570f4b090/perspectives/69df8fa8-4f84-499e-9341-28eb5085c40b?selection=Class(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/06/P0630%23EC366660175%3E)




def get_dupes_list(dups,subtree):
    output = ""
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
        link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",p[4])
        link = "<a target=\"blank\" href=\"" + link_target + "\">" + p[0] + "</a>"
        output += "<tr>"
        output += "<th>" + link + "</th><th style=\"text-align: left;\"><div style=\"margin: 4px 2px; border:none; background-color:HoneyDew; cursor:pointer\" class=\"mybutton\" >" + l + "</div>\n"
        output += "<div style=\"display: none; margin: 4px 2px; border:none; background-color:HoneyDew; cursor:pointer\" class=\"mybutton\" >" + m + "</div></th>"
        output += "</tr>"
    
    return output


def get_subtree_options():
    output = ""
    tree_top_descriptions = TREE_TOP_DESCRIPTIONS 
    output += "<option id=\"" + tree_top_descriptions["CLINICAL INFO"] + "\">CLINICAL INFO</option>"
    output += "<option id=\"" + tree_top_descriptions["ALL RESULT SECTIONS"] + "\">ALL RESULT SECTIONS</option>"
    output += "<option id=\"" + tree_top_descriptions["ALL OCF EVENT SETS"] + "\">ALL OCF EVENT SETS</option>"
    output += "<option id=\"" + tree_top_descriptions["ALL DOCUMENT SECTIONS"] + "\">ALL DOCUMENT SECTIONS</option>"

    tdescriptions = list(tree_top_descriptions.keys())
    tdescriptions.sort()
        
    for description in tdescriptions:
        if not description in ["CLINICAL INFO","ALL RESULT SECTIONS","ALL OCF EVENT SETS","ALL DOCUMENT SECTIONS"]:
            output += ("<option id=\"" + tree_top_descriptions[description] + "\">" + description + "</option>")

    return output

def get_options():
    output = ""
    for name in SECTION_NAMES:
        output += "<option id=\"" + R_SECTION_DESCRIPTIONS[name] + "\">" + name + "</option>"   
    return output 

def get_sections_datalist():
    output = "<form id=\"powerformform\" action=\"javascript:void(0)\" onsubmit=\"show_selected_powerform();\"><input name=\"sections\" list=\"sections\"><datalist id=\"sections\">"
    for name in SECTION_NAMES:
        output += "<option value=\"" + name + "\">"
    output += "</datalist><input onclick=\"show_selected_powerform();\" type=\"button\" value=\"Powerform\"></form>"
    return output

def get_eshs_datalist():
    output = "<form id=\"eshsform\" action=\"javascript:void(0)\" onsubmit=\"show_selected_esh();\"><input name=\"teshs\" list=\"teshs\"><datalist id=\"teshs\">"
    names = list(esh_names.keys())
    names.sort()
    for name in names:
        output += "<option value=\"" + name + "\">"
    output += "</datalist><input onclick=\"show_selected_esh();\" type=\"button\" value=\"Event Set\"></form>"
    return output


def get_pfs_codes(pfs_names):
    output = []
    for name in pfs_names:
        output.append(R_SECTION_DESCRIPTIONS[name])
    return output
        
'''
[   [], 
    ['Mid parental height (observable entity)', 'Result (navigational concept)', 'Followed by (qualifier value)', 'Result (administrative concept)', 'Following (qualifier value)', 'Resulting in (attribute)', 'Male (finding)', 'Male structure (body structure)', 'Man (person)'], 
    [], 
    ['Mid Parental Height', 'Mid Parental Height']
]

'''

@app.route("/eshexplorer",methods=["GET","POST"])
def esh_search_one():
    
    subtree_options = get_subtree_options()
    sections_datalist = get_sections_datalist() 
    esh_datalist = get_eshs_datalist()
    options = get_options()
    return ESH_TEMPLATE.replace("_UNSELECTED_POWERFORM_SECTIONS_",options).replace("_SUBTREES_",subtree_options).replace("_SECTIONS_DATALIST_",sections_datalist).replace("_ESHS_DATALIST_",esh_datalist)

@app.route("/eshexplorer/eshexplorer",methods=["GET","POST"])
def esh_search_two():
    
    subtree_options = get_subtree_options()
    sections_datalist = get_sections_datalist() 
    esh_datalist = get_eshs_datalist()
    options = get_options()
    return ESH_TEMPLATE.replace("_UNSELECTED_POWERFORM_SECTIONS_",options).replace("_SUBTREES_",subtree_options).replace("_SECTIONS_DATALIST_",sections_datalist).replace("_ESHS_DATALIST_",esh_datalist)

@app.route("/",methods=["GET","POST"])
def esh_search_three():
    
    subtree_options = get_subtree_options()
    sections_datalist = get_sections_datalist() 
    esh_datalist = get_eshs_datalist()
    options = get_options()
    return ESH_TEMPLATE.replace("_UNSELECTED_POWERFORM_SECTIONS_",options).replace("_SUBTREES_",subtree_options).replace("_SECTIONS_DATALIST_",sections_datalist).replace("_ESHS_DATALIST_",esh_datalist)

@app.route("/eshexplorer/",methods=["GET","POST"])
def esh_search_four():
    
    subtree_options = get_subtree_options()
    sections_datalist = get_sections_datalist() 
    esh_datalist = get_eshs_datalist()
    options = get_options()
    return ESH_TEMPLATE.replace("_UNSELECTED_POWERFORM_SECTIONS_",options).replace("_SUBTREES_",subtree_options).replace("_SECTIONS_DATALIST_",sections_datalist).replace("_ESHS_DATALIST_",esh_datalist)

@app.route("/eshexplorer/get_powerform_info",methods=["GET","POST"])
def get_powerform_info():
    j = request.get_json()
    powerform = ""
    if "powerform" in j:
        powerform = j["powerform"]
    code = ""
    print(powerform)
    print(powerform in R_SECTION_DESCRIPTIONS)
    if powerform and powerform in R_SECTION_DESCRIPTIONS:
        code = R_SECTION_DESCRIPTIONS[powerform]
    eshs = powerform_to_eshs_map[code]
    eshs_local = {}
    for esh in eshs:
        eshs_local[DESCRIPTIONS[esh]] = esh
    esh_names = list(eshs_local.keys())
    esh_names.sort()
    link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",code)
    link = "<a target=\"blank\" href=\"" + link_target + "\">" + powerform + "</a>"
    outstring = ""
    if "row_number" in j:
        outstring += "<tr><th>" + link + "</th></tr>"
    outstring += "<tr style=\"background-color:lightgreen;\">"
    i = 0
    for esh_name in esh_names:
        i += 1
        if i == 12:
            i = 0
            outstring += "</tr><tr style=\"background-color:lightgreen;\">"
        esh = eshs_local[esh_name]
        placeholder_string = ""
        if esh in PLACEHOLDERS:
            placeholder_string = "<p style=\"font-size: 9px;\">placeholder</p>"
        outstring += "<th>"
        link_target = LINK_TARGET.replace("_CODE_",esh)
        link = "<a onclick=\"show_selected_esh_by_id(" + esh + ",this);\" target=\"blank\" href=\"" + link_target + "\">" + esh_name + "</a>"
        outstring += link
        outstring += placeholder_string
        outstring += "</th>"
    outstring += "</tr>"


    return outstring 

@app.route("/eshexplorer/get_esh_info",methods=["GET","POST"])
def get_esh_info():
    j = request.get_json()
    esh = ""
    esh_name = ""
    first = False
    if "row_number" in j:
        first = True
    if "esh" in j:
        esh = str(j["esh"])
        esh_name = DESCRIPTIONS[esh] 
    elif "esh_name" in j:
        esh_name = j["esh_name"]
    print(esh_name)
    print("#######################")
    print(j)
    print("#######################")
    print(esh_name)
    if not esh:
        esh = esh_names[esh_name]
    print(esh)
   
    if not esh:
        return ""
    link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",esh)

    link = "<a target=\"blank\" href=\"" + link_target + "\">" + esh_name + "</a>"
    if not esh in esh_to_powerforms_map:
        return "<tr><th>" + link + "</th></tr>"

    powerforms = esh_to_powerforms_map[esh]
    powerforms_local = {}
    for powerform in powerforms:
        powerforms_local[SECTION_DESCRIPTIONS[powerform]] = powerform
    powerform_names = list(powerforms_local.keys())
    powerform_names.sort()
    outstring = ""
    if first:
        outstring += "<tr><th>" + link + "</th></tr>"
    outstring += "<tr style=\"background-color: lightblue;\">"
    i = 0
    for powerform_name in powerform_names:
        i += 1
        if i == 12:
            i = 0
            outstring += "</tr>"
            outstring += "<tr style=\"background-color: lightblue;\">"
        powerform = powerforms_local[powerform_name]
        outstring += "<th>"
        link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",powerform)
        link = "<a onclick=\"show_selected_powerform_by_name('" + powerform_name + "',this);\" target=\"blank\" href=\"" + link_target + "\">" + powerform_name + "</a>"
        outstring += link
        outstring += "</th>"
    outstring += "</tr>"


    return outstring


@app.route("/eshexplorer/display_duplicates",methods=["GET","POST"])
def get_duplicates():
    j = request.get_json()
    post_obj = {}
    
    if "text" in j:
        text = j["text"]
        post_obj["text"] = text
    else:
        return ""
    if "powerforms" in j:
        pf_names = j["powerforms"]
        print(pf_names)
        post_obj["powerforms"] = pf_names
    if "subtree" in j:
        subtree = j["subtree"]
    else:
        subtree = "CLINICAL INFO"

    headers = {'Content-Type': 'application/json'}
    url = "https://halsted.compbio.buffalo.edu/anf_viewer/esh_service"
    response = requests.post(url,data=json.dumps(post_obj),headers=headers)
    
    r = []
    try: 
        r = response.json()
    except:
        pass
    
    print(post_obj)
    event_sets = []
    if "event_sets" in r:
        event_sets = r["event_sets"]
    print(r)
    print(event_sets)
    dup_string = DUPES_TABLE_TEMPLATE.replace("_DUPES_",get_dupes_list(event_sets,subtree))

    print("---!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(dup_string)
    
    return dup_string 

@app.route("/eshexplorer/display_groupers",methods=["GET","POST"])
def get_groupers():
    j = request.get_json()
    post_obj = {}
    pf_names = []
    subtree = "CLINICAL INFO"
    maxn = 10 
    
    print(j)
    if "text" in j:
        text = j["text"]
        post_obj["text"] = text
    else:
        return ""
    if "powerforms" in j:
        pf_names = j["powerforms"]
        print(pf_names)
        post_obj["powerforms"] = pf_names
    if "subtree" in j:
        subtree = j["subtree"]

    
    print(text)
    pf_codes = []
    if pf_names:
        print("asdfasdfasdf")
        print(pf_names)
        pf_codes = get_pfs_codes(pf_names)
        
    print(subtree)
    if not subtree:
        subtree = "CLINICAL INFO"
    
    headers = {'Content-Type': 'application/json'}
    
    url = "https://halsted.compbio.buffalo.edu/anf_viewer/esh_service"
    response = requests.post(url,data=json.dumps(post_obj),headers=headers)
    j = []
    try: 
        j = response.json()
    except:
        pass
    groupers = []
    if "groupers" in j:
        groupers = j["groupers"]
    event_sets = []
    if "event_sets" in j:
        event_sets = j["event_sets"]
    output_groupers = groupers[:10]
    esh_details = get_groupers_list(output_groupers,subtree)

    return GROUPERS_TABLE_TEMPLATE.replace("_GROUPERS_",esh_details)


@app.route("/eshexplorer/display_grouper_analysis",methods=["GET","POST"])
def get_grouper_analysis():
    j = request.get_json()
    
    post_obj = {}
    pf_names = []
    subtree = "CLINICAL INFO"
    maxn = 10 
    
    print(j)
    if "text" in j:
        text = j["text"]
        post_obj["text"] = text
    else:
        return ""
    if "powerforms" in j:
        pf_names = j["powerforms"]
        print(pf_names)
        post_obj["powerforms"] = pf_names
    if "subtree" in j:
        subtree = j["subtree"]
    
    headers = {'Content-Type': 'application/json'}
    url = "https://halsted.compbio.buffalo.edu/anf_viewer/esh_service"
    response = requests.post(url,data=json.dumps(post_obj),headers=headers)
    j = []
    try: 
        j = response.json()
    except:
        pass
    groupers = []
    if "groupers" in j:
        groupers = j["groupers"]

    output_groupers = groupers[:10]
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
            link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",esh)
            link = "<a onclick=\"show_selected_esh_by_id('" + esh + "',null)\" target=\"blank\" href=\"https://osler.compbio.buffalo.edu/webprotege//#projects/" + ESH_PRIMARY + "/perspectives/69df8fa8-4f84-499e-9341-28eb5085c40b?selection=Class(%3Chttp://www.semanticweb.org/oracleRDFBot/ontologies/2026/01/P0630%23EC" + esh + "%3E)\">" + esh_name + "</a>"
            child_snomeds = ""
            for snomed in esh_with_codes[1][0]:
                child_snomeds += EVENT_SET_SNOMED_TEMPLATE_GREEN.replace("EVENT_SET_SNOMED",snomed)
            child_pfs = ""
            for powerform in esh_with_codes[1][2]:
                if not powerform in R_SECTION_DESCRIPTIONS:
                    continue
                powerform_id = R_SECTION_DESCRIPTIONS[powerform]
                link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",powerform_id)
                powerform_link = "<a onclick=\"show_selected_powerform_by_name('" + powerform + "',null);\" target=\"blank\" href=\"" + link_target + "\">" + powerform + "</a>"
                child_pfs += EVENT_SET_POWERFORM_TEMPLATE_BLUE.replace("EVENT_SET_POWERFORM",powerform_link)
            for powerform in esh_with_codes[1][3]:
                if not powerform in R_SECTION_DESCRIPTIONS:
                    continue
                powerform_id = R_SECTION_DESCRIPTIONS[powerform]
                link_target = LINK_TARGET_TEMPLATE.replace("_CODE_",powerform_id)
                powerform_link = "<a onclick=\"show_selected_powerform_by_name('" + powerform + "',null);\" target=\"blank\" href=\"" + link_target + "\">" + powerform + "</a>"
                child_pfs += EVENT_SET_POWERFORM_TEMPLATE.replace("EVENT_SET_POWERFORM",powerform_link)
            event_sets_out += EVENT_SET_TEMPLATE.replace("EVENT_SET_SNOMEDS",child_snomeds).replace("EVENT_SET_POWERFORMS",child_pfs).replace("EVENT_SET_NAME",link).replace("EVENT_SET_CODE","m"+esh)
        
        grouper_outputs += GROUPER_TEMPLATE.replace("EVENT_SETS",event_sets_out).replace("GROUPER_NAME",grouper_name).replace("_STYLE_",style).replace("__ID__",grouper_code)
    

    return grouper_outputs 
   


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8887)
