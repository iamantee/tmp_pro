import re
from Configuration import Configuration

class HKex_Daily_Quotation_Data_Parser(object):
    """
        HKex daily quotation data parser(file) 
    """
    _CONFIG_SECTION = 'file.reader.hkex.daily.quotations'
    
    _data_file_struct_info = {"categories":{}}

    def __init__(self):
        pass

    def extract_section_info(self, file_path):
        no_of_header_line_to_skip = int(Configuration.get_option(self.__class__._CONFIG_SECTION, 'NoOfHeaderLineToSkip'))
        no_of_tailer_line_to_skip = int(Configuration.get_option(self.__class__._CONFIG_SECTION, 'NoOfTailerLineToSkip'))
        start_point_token = Configuration.get_option(self.__class__._CONFIG_SECTION, 'StartPointToken')
        content_section_cat_pattern = Configuration.get_option(self.__class__._CONFIG_SECTION, 'ContentSectionCatPattern')
        content_section_loc_pattern = Configuration.get_option(self.__class__._CONFIG_SECTION, 'ContentSectionLocPattern')
        tmp_section_anchor_name = None
        tmp_section_anchor_start_line_no = -1


        try:
            with open(file_path, 'r') as data_file:
                for line_no, line in enumerate(data_file):
                    if no_of_header_line_to_skip > 0:
                        no_of_header_line_to_skip-=1
                        continue
                    else:
                        if self.__class__._data_file_struct_info['StartPointToken']:
                            content_section_cat_pattern_matching = re.search(content_section_cat_pattern, line)
                            content_section_loc_pattern_matching = re.search(content_section_loc_pattern, line)
                            if content_section_cat_pattern_matching:
                                self.__class__._data_file_struct_info["categories"][content_section_cat_pattern_matching.group(1)] = [-1, -1]
                            elif content_section_loc_pattern_matching:
                                if tmp_section_anchor_name:
                                    self.__class__._data_file_struct_info["categories"][tmp_section_anchor_name][1] = line_no - 1
                                else:
                                    tmp_section_anchor_name = content_section_loc_pattern_matching.group(1)
                                    self.__class__._data_file_struct_info["categories"][tmp_section_anchor_name][0] = line_no


        except IOError:
            raise 


if __name__ == '__main__':
    test_str = '<a href="#market_highlights">MARKET HIGHLIGHTS</a>'
    m  = re.search('<a\s+href\s*=\s*"#(\w+)">.*<\/a>', test_str)

    print m.group(0)
    print m.group(1)