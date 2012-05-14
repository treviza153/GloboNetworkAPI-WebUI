# -*- coding:utf-8 -*-
"""
Title: Infrastructure NetworkAPI
Author: avanzolin / S2it
Copyright: ( c )  2009 globo.com todos os direitos reservados.
"""

import re
from random import choice
from django.utils.cache import add_never_cache_headers
from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext


def check_regex(string, regex):
    pattern = re.compile(regex)
    return pattern.match(string) is not None

def make_random_password(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'):
        "Generates a random password with the given length and given allowed_chars"
        return ''.join([choice(allowed_chars) for i in range(length)])

class DataTablePaginator():
    
    @property
    def sColumns(self):
        return self.sColumns
    
    @property
    def sEcho(self):
        return self.sEcho
    
    @property
    def start_record(self):
        return self.start_record
    
    @property
    def end_record(self):
        return self.end_record
    
    @property
    def asorting_cols(self):
        return self.asorting_cols
    
    @property
    def searchable_columns(self):
        return self.searchable_columns
    
    @property
    def custom_search(self):
        return self.custom_search
    
    def __init__(self, request, columnIndexNameMap):
        self.request = request
        self.columnIndexNameMap = columnIndexNameMap
    
    def build_server_side_list(self):
        """
        Build all params to send to API
        """
        
        # Datatable params
        cols = int(self.request.GET.get('iColumns',0))
        iDisplayLength =  min(int(self.request.GET.get('iDisplayLength',10)),100)
        self.start_record = int(self.request.GET.get('iDisplayStart',0))
        self.end_record = self.start_record + iDisplayLength
        
        # Pass sColumns
        keys = self.columnIndexNameMap.keys()
        keys.sort()
        colitems = [self.columnIndexNameMap[key] for key in keys]
        self.sColumns = ",".join(map(str, colitems))
        
        # Ordering data
        iSortingCols =  int(self.request.GET.get('iSortingCols',0))
        self.asorting_cols = []
        
        if iSortingCols:
            for sortedColIndex in range(0, iSortingCols):
                sortedColID = int(self.request.GET.get('iSortCol_'+str(sortedColIndex),0))
                if self.request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':
                    sortedColName = self.columnIndexNameMap[sortedColID]
                    sortingDirection = self.request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
                    if sortingDirection == 'desc':
                        sortedColName = '-'+sortedColName
                    self.asorting_cols.append(sortedColName)
                    
        # Determine which columns are searchable
        self.searchable_columns = []
        for col in range(0,cols):
            if self.request.GET.get('bSearchable_{0}'.format(col), False) == 'true':
                self.searchable_columns.append(self.columnIndexNameMap[col])
                
        # Apply filtering by value sent by user
        self.custom_search = self.request.GET.get('sSearch', '').encode('utf-8');
        
        self.sEcho = int(self.request.GET.get('sEcho',0))
        
    def build_response(self, data, total, json_template, request):
        """
        Build the response to ajax
        """
        
        # Build return json
        response_dict = dict()
        response_dict["aaData"] = data
        response_dict["sEcho"] = self.sEcho
        response_dict["iTotalRecords"] = total
        response_dict["iTotalDisplayRecords"] = total
        response_dict["sColumns"] = self.sColumns
        
        response = HttpResponse(loader.render_to_string(json_template, response_dict, context_instance=RequestContext(request)), mimetype='application/javascript')
        response.status_code = 200
        
        # Prevent from caching datatables result
        add_never_cache_headers(response)
        
        # Returns JSON
        return response