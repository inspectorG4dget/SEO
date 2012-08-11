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

class Quantcast:

    def __init__(self):
        self.url = None
        self.rank = None
        self.traffic = Traffic()
        self.categories = []

    def get_categories(self):
        output = []
        for cat_obj in self.categories:
            output.append(cat_obj.name)
        output.sort()
        return output

    def has_category(self, cat):
        '''Return True if the quantcast object has the given category. False if it doesn't'''

        for cat_obj in self.categories:
            if cat_obj.name == cat:
                return True
        
        return False

    def has_site(self, site):
        '''Return True if the quantcast object has the given site in any of its categories. False if it doesn't'''
        
        for cat_obj in self.categories:
            if site in cat_obj.sites:
                return True

        return False

    def pretty_print(self):
        '''Return a string with all the relevant data in an excel-friendly format'''
        
        cat_sites_str = ''
        for cat_obj in self.categories:
            cat_sites_str += cat_obj.name + '\t'

            for site in cat_obj.sites:
                cat_sites_str += site + '\t'
                
        return self.url + '\t' + str(self.rank) + '\t' + self.traffic.pretty_print() + '\t' + cat_sites_str + '\n'

# ===================== quantcast OBJECT FINISHED =====================

class Category:

    def __init__(self):
        self.name = None
        self.sites = []

    def pretty_print(self):
        '''Return a string with all the relevant data in an excel-friendly format'''
        
        output_str = ''
        output_str += self.name

        for site in self.sites:
            output_str += '\t' + site

        return output_str

# ===================== category OBJECT FINISHED ======================

class Traffic:

    def __init__(self):
        self.GP = -1
        self.GU = -1
        self.UP = -1
        self.UU = -1

    def pretty_print(self):
        '''Return a string with all the relevant data in an excel-friendly format'''
        
        return "%d\t%d\t%d\t%d" % (self.GP, self.GU, self.UP, self.UU)
