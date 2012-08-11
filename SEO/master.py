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

from quantcast import *
from qcparser import *
import time

def create_quantcast(url):
    '''Create a quantcast object for the specific URL'''
    
    try:
        site_html = get_qc_html(url) # get the html source code of the quantcast page for the URL as a string
            
        qc = Quantcast()             # create a new quantcast object and populate the attributes
        qc.url = url
        qc.rank = get_rank(site_html)
        qc.traffic = get_traffic(site_html)

        qc.categories = get_categories(site_html)
        return qc
    except:                          # if there is no quantcast page for the URL, return a None type object
        return None

def do_the_analysis(url_file, output_file, analytics_file):
    '''Open te URL file, the output file and the analytics file.
    Cross match the categories and the sites and write the results to the files'''
    url_file = open(url_file, "r")
    total_urls = len(url_file.readlines())
    url_file.close()
    url_file = open(url_file.name, "r")
    
    output_file = open(output_file, "a")
    analytics_file = open(analytics_file, "a")

    output_file.write('\n\n' + "=" * 50)
    output_file.write(time.asctime() + "=" * 50 + '\n' * 2)

    es_obj = create_quantcast("http://www.eshakti.com")
    
    analytics_file.write('\n\n' + "=" * 50)
    analytics_file.write(time.asctime() + "=" * 50 + '\n' * 2)
    analytics_file.write("%s\t%s\t%s\t%s\t%s\t%s\t" % ("URL", "Rank", "Global People", "Global Uniques", "U.S. People", "U.S. Uniques"))

    to_write = ''
    for cat_obj in es_obj.categories:
        to_write += cat_obj.pretty_print() + '\t'
    analytics_file.write(to_write)
    analytics_file.write('\n')
    

    url_no = 0
    for line in url_file:
        url = line.strip()

        url_no += 1
        print "Starting to process URL %d of %d" % (url_no, total_urls )
        
        if url == "http://www.eshakti.com":
            output_file.write(es_obj.pretty_print())
            continue
        
        qco = create_quantcast(url)
        if qco == None:
            print "%s could not be profiled!\n" % url
            continue
        
        output_file.write(qco.pretty_print())
        analytics_file.write(url + '\t')

        analytics_file.write(str(qco.rank) + '\t' + qco.traffic.pretty_print() + '\t')

        for cat_obj in es_obj.categories:
            if qco.has_category(cat_obj.name):
                analytics_file.write("Yes\t")
            else:
                analytics_file.write("No\t")

            for site in cat_obj.sites:
                if qco.has_site(site):
                    analytics_file.write("Yes\t")
                else:
                    analytics_file.write("No\t")
            

        analytics_file.write('\n')
        print "Finished processing URL %d of %d" % (url_no, total_urls )

    url_file.close()     
    output_file.close()
    analytics_file.close()
    print "All Done! Now take a look at the Output and Analytics Files"

if __name__ == '__main__':
    import picture
    from random import randint

    messages = ["Okay, now go get some coffee while I work my magic...", "Why do I have to do all the work around here?", \
                "Never send a man to do a machine's job. A woman maybe, but NEVER a man!", "I've got a lovely bunch of coconuts...", \
                "Buy me some ice cream if you wanna see any output...", "*Yawn* Here we go again...", \
                "If I were a superhero who could fly AND be invisible, that would be the best...", \
                "What?! That's it?? At least give me a challenge!", "Humans.. yeeuck!!", \
                "I'm afraid that's easier said than done, but let me give it a try...", "Are you sure you're ready for this?", \
                "What else you got?", "Grr.. Fine!"]

    creation_info = "This program was created by Ashwin Panchapakesan: The God of Gods. Cross him, and you incur his wrath\
    or maybe you could just buy him a Ferrari and call it even..."
    print creation_info
    print "Please select the URL file: "
    url_file = picture.pick_a_file()
    #url_file = 'C:/Documents and Settings/Administrator/Desktop/Ashwin/ES/Programming/Website Makeover/Build 6/URLs.txt'

    print "Please select the output file: "
    output_file = picture.pick_a_file()
    #output_file = 'C:/Documents and Settings/Administrator/Desktop/Ashwin/ES/Programming/Website Makeover/Build 6/output_file.txt'

    print "Please select the analytics file: "
    analytics_file = picture.pick_a_file()
    #analytics_file = 'C:/Documents and Settings/Administrator/Desktop/Ashwin/ES/Programming/Website Makeover/Build 6/analytics_file.txt'

    print messages[randint(0, len(messages) -1)]
    do_the_analysis(url_file, output_file, analytics_file)
