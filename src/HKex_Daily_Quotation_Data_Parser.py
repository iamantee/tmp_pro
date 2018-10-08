import re
import os
from Configuration import Configuration

class HKex_Daily_Quotation_Data_Parser(object):
    """
        HKex daily quotation data parser(file) 
    """
    _CONFIG_SECTION = 'file.reader.hkex.daily.quotations'
    
    _date = ''
    _data_file_base_path = ''
    _data_file_struct_info = {'StartPointToken': None, 'categories':{}}

    def __init__(self, date):
        try:
            self._date = date
            self._data_file_base_path = Configuration.get_option('global', 'DataFileBasePath')
        except:
            raise


    def extract_section_info(self):
        file_path = os.path.join(self._data_file_base_path, ''.join(['d', self._date, 'e', '.txt'])) 
        no_of_header_line_to_skip = int(Configuration.get_option(self.__class__._CONFIG_SECTION, 'NoOfHeaderLineToSkip'))
        no_of_tailer_line_to_skip = int(Configuration.get_option(self.__class__._CONFIG_SECTION, 'NoOfTailerLineToSkip'))
        start_point_token_pattern = Configuration.get_option(self.__class__._CONFIG_SECTION, 'StartPointToken')
        content_section_cat_pattern = Configuration.get_option(self.__class__._CONFIG_SECTION, 'ContentSectionCatPattern')
        content_section_loc_pattern = Configuration.get_option(self.__class__._CONFIG_SECTION, 'ContentSectionLocPattern')
        tmp_section_anchor_name = None
        tmp_section_anchor_start_line_no = -1

        try:
            with open(file_path, 'r') as data_file:
                last_line_no = -1
                for line_no, line in enumerate(data_file):
                    last_line_no = line_no
                    if no_of_header_line_to_skip > 0:
                        no_of_header_line_to_skip-=1
                        continue
                    else:
                        if self.__class__._data_file_struct_info['StartPointToken']:
                            content_section_cat_pattern_matching = re.search(content_section_cat_pattern, line)
                            content_section_loc_pattern_matching = re.search(content_section_loc_pattern, line)
                            if content_section_cat_pattern_matching:
                                self.__class__._data_file_struct_info['categories'].update({content_section_cat_pattern_matching.group(1) : [-1, -1]})
                            elif content_section_loc_pattern_matching:
                                if tmp_section_anchor_name is None:
                                    tmp_section_anchor_name = content_section_loc_pattern_matching.group(1)
                                    self.__class__._data_file_struct_info['categories'][tmp_section_anchor_name][0] = line_no
                                elif tmp_section_anchor_name != content_section_loc_pattern_matching.group(1):
                                    self.__class__._data_file_struct_info['categories'][content_section_loc_pattern_matching.group(1)][0] = line_no
                                    self.__class__._data_file_struct_info['categories'][tmp_section_anchor_name][1] = line_no - 1
                                    tmp_section_anchor_name = content_section_loc_pattern_matching.group(1)
                        else:
                            start_point_token_pattern_matching = re.search(start_point_token_pattern, line)
                            if start_point_token_pattern_matching:
                                self.__class__._data_file_struct_info['StartPointToken'] = line_no
                
                self.__class__._data_file_struct_info['categories'][tmp_section_anchor_name][1] = last_line_no


        except IOError:
            raise 

    def extract_section_raw_content(self):
        try:
            if len(self.__class__._data_file_struct_info['categories']) > 0:
                for category, line_info in self.__class__._data_file_struct_info['categories'].iteritems():
                    raw_content = []
                    data_file_path = os.path.join(self._data_file_base_path, ''.join(['d', self._date, 'e', '.txt']))
                    cat_data_dir_path = os.path.join(self._data_file_base_path, 'raw')
                    cat_data_file_path = os.path.join(cat_data_dir_path, '.'.join([category, 'raw', 'txt']))
                    with open(data_file_path, 'r') as data_file:
                        for line_no, line in enumerate(data_file):
                            if line_info[0] <= line_no <= line_info[1]:
                                raw_content.append(line)
                    
                    if not os.path.exists(cat_data_dir_path):
                        os.makedirs(cat_data_dir_path)

                    with open(cat_data_file_path, 'w+') as cat_data_file:
                        cat_data_file.writelines(raw_content)
        except IOError:
            raise
        
    def extract_quotation_data(self):
        try:
            security_data_set = []
            security_data = []
            is_continue_for_same_sec = False
            data_file_path = os.path.join(self._data_file_base_path, 'raw', 'quotation.txt')
            suspended_security_info_pattern = re.compile(Configuration.get_option('.'.join([self.__class__._CONFIG_SECTION, category]), 'SuspendedSecurityInfoPattern'))
            normal_security_first_line_pattern = re.compile(Configuration.get_option('.'.join([self.__class__._CONFIG_SECTION, category]), 'NormalSecurityFirstLinePattern'))
            normal_security_second_line_pattern = re.compile(Configuration.get_option('.'.join([self.__class__._CONFIG_SECTION, category]), 'NormalSecuritySecondLinePattern'))

            if os.path.exists(data_file_path):
                with open(data_file_path, 'r') as data_file:
                    for line in data_file:
                        normal_security_first_line_pattern_matching = re.search(line)
                        if normal_security_first_line_pattern_matching:
                           is_continue_for_same_sec = True
                           security_data = [None] * 13 
                           security_data[0:normal_security_first_line_pattern.groups] = [normal_security_first_line_pattern_matching.group(i) for i in range(2, normal_security_first_line_pattern.groups+1)]
                           security_data[-2] = '*' == normal_security_first_line_pattern_matching.group(1) ? 'Y' : 'N'
                        elif is_continue_for_same_sec:
                            is_continue_for_same_sec = False
                            normal_security_second_line_pattern_matching = re.search(line)
                            security_data[normal_security_first_line_pattern.groups:-2] = [normal_security_second_line_pattern_matching.group(i) for i in range(1, normal_security_second_line_pattern.groups+1)]
                            security_data_set.append(security_data)
                            security_data = []
                        else:
                            suspended_security_info_pattern_matching = re.search(line)
                            if suspended_security_info_pattern_matching:



                        else:
                            pass

            else:
                raise Exception(''.join(['No such file: ', data_file_path]))


        except:
            raise

if __name__ == '__main__':
    parser = HKex_Daily_Quotation_Data_Parser('181002')

    parser.extract_section_info()
    print parser._data_file_struct_info
    
    parser.extract_section_raw_content()
