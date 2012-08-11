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

def create_quantcast(url):
    site_html = get_qc_html(url)
        
    qc = Quantcast()
    qc.url = url
    qc.rank = get_rank(site_html)
    qc.traffic = Traffic()

    qc.traffic.GP = 100
    qc.traffic.GU = 101
    qc.traffic.UP = 200
    qc.traffic.UU = 201

    category1 = Category()
    category2 = Category()
    category3 = Category()

    category1.name = 'CAT1'
    category2.name = 'CAT2'
    category3.name = 'CAT3'

    if url == "http://www.eshakti.com":
        category1.sites = ['site 1.1', 'site e.2', 'site 1.3', 'site 1.4']
        category2.sites = ['site e.1', 'site 2.2', 'site 2.3', 'site 2.4']
        category3.sites = ['site 3.1', 'site e.2', 'site 3.3', 'site 3.4']

    else:
        category1.sites = ['site 1.1', 'site 2.2', 'site 1.3', 'site 1.4']
        category2.sites = ['site 1.1', 'site 2.2', 'site 2.3', 'site 2.4']
        category3.sites = ['site 3.1', 'site 2.2', 'site 3.3', 'site 3.4']
        
    qc.categories = [category1, category2, category3]
    return qc
