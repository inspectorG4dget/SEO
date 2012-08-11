'''
 Licensed to Ashwin Panchapakesan under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 Ashwin licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
'''

import urllib2
from quantcast import *

def get_html(url):
    '''Return the html code of the URL as a string'''

    html = ''
    for line in urllib2.urlopen(url):
        html += line
    return html

def get_qc_html(url):
    '''Return the html code of the quantcast page relevant to the URL as a string'''
    
    domain_name_end = url.rfind(".")
    domain_name_start = url[: domain_name_end].rfind('.') + 1
    domain_name = url[domain_name_start :].strip()
    return get_html("http://www.quantcast.com/" + domain_name)

def get_rank(site_html):
    '''Extract and return the quantcast rank from the html code of a quantcast page'''
    
    rank_block_start = site_html.find("(rank ")
    rank_block_end = site_html.find(")", rank_block_start)
    rank_block = site_html[rank_block_start : rank_block_end]

    rank_str_start = rank_block.find(" ")
    rank_str = rank_block[rank_str_start + 1 :]

    rank = rank_str.replace(',', '').strip()
    return int(rank)

def extract_sites(category_block):
    '''Extract and return (as a list) the sites that pertain to a certain category'''
    
    sites = []
    while True:
#    for i in range(0, 4):   # just for safety reasons
            a_href_start = category_block.find('<a href="/')
            if a_href_start == -1:
                break
            
            site_start = a_href_start + len('<a href="/')
            site_end = category_block.find('" class="', site_start)

            site_name = category_block[site_start : site_end].strip()
            sites.append(site_name)
            category_block = category_block[site_end : ].strip()

    return sites

def get_categories_block(site_html):
    '''Extract and return the block of html code that contains all the categories and their respective sites'''
    
    categories_block_start = site_html.find('<ul class="categories">')
    categories_block_end = site_html.find('</ul>', categories_block_start)
    return site_html[categories_block_start : categories_block_end]

def get_categories(site_html):
    '''Create a category object. Populate it with its name and the list of its relavent sites.
    Repeat until all the categories have been extracted. Return a list of all category objects'''
    
    categories_block = get_categories_block(site_html)
    categories = []

    while len(categories_block) > 0:
        cat_obj = Category()

        category_block_start = categories_block.find("<li><h6>")
        category_block_end = categories_block.find("<div>&nbsp;</div>", category_block_start)
        category_block = categories_block[category_block_start : category_block_end]

        category_name_start = category_block.find("<h6>") + len("<h6>")
        category_name_end = category_block.find("</h6>")
        cat_obj.name = category_block[category_name_start : category_name_end].strip()

        cat_obj.sites = extract_sites(category_block)
        categories.append(cat_obj)
        
        next_category_start = category_block_end + len("<div>&nbsp;</div>")
        categories_block = categories_block[next_category_start : ].strip()
   
    return categories

def html_find(html, text):
    '''Return the index of the character that follows the end of the text being search for in the html'''
    
    return html.find(text) + len(text)

def conv2int(traffic):
    '''Return an integer after converting 'M' to million and 'K' to thousand and 'B' to billion'''
    
    traffic_int = -1
    traffic = traffic.replace(",", "")
    
    if traffic[-1] == 'K':
        traffic_int = float(traffic[:-1]) * (10 ** 3)
    elif traffic[-1] == 'M':
        traffic_int = float(traffic[:-1]) * (10 ** 6)
    elif traffic[-1] == 'B':
        traffic_int = float(traffic[:-1]) * (10 ** 9)
    else:
        traffic_int = float(traffic)

    return traffic_int    
        
    
def get_traffic(site_html):
    '''Create a traffic object.
    Extract the traffic information from the html code and populate the traffic object with that data.
    Return the traffic object'''
    
    traffic = Traffic()

    traffic_block_start = site_html.find('<table class="trafficstats">') + len('<table class="trafficstats">')
    if traffic_block_start == -1:
        return traffic
    
    traffic_block_end = site_html.find("</table>", traffic_block_start)
    traffic_block = site_html[traffic_block_start : traffic_block_end]
    
    traffic_map = {}
    traffic_map["Global People"] = -1
    traffic_map["Global Cookies"] = -1
    traffic_map["US People"] = -1
    traffic_map["US Cookies"] = -1

    for i in range(4):
        td_start = html_find(traffic_block, "<td>")
        td_end = traffic_block.find("</td>", td_start)
        td = traffic_block[td_start : td_end]

        strong_start = td.find("<strong>")
        if strong_start != -1:
            strong_start += len("<strong>")
            strong_end = td.find("</strong>")
            traffic_str = td[strong_start : strong_end].strip()
            
            traffic_name_start = strong_end + len("</strong>")
            traffic_name = td[traffic_name_start : ].strip()
            
            traffic_map[traffic_name] = conv2int(traffic_str)

        traffic_block = traffic_block[td_end : ]

    traffic.GP = int(traffic_map["Global People"])
    traffic.GU = int(traffic_map["Global Cookies"])
    traffic.UP = int(traffic_map["US People"])
    traffic.UU = int(traffic_map["US Cookies"])
    return traffic
