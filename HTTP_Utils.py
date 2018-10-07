import requests
import os

class HTTP_Utils(object):
    
    """
        HTTP utility functions  
    """

    def download_file(self, src_url, dest_file_path=None):
        http_response = requests.get(src_url)

        if http_response is None:
            return ('ERROR(no response): HTTP request failed to get response. ' % http_response.status_code)
        elif http_response.status_code != 200: 
            return ('ERROR(%d): HTTP request failed to get response. ' % http_response.status_code)
        else: 
            if dest_file_path is None:
                pass
            else:
                if dest_file_path is None:
                    dest_file_path = os.path.join(os.getcwd(), "web_content.txt")

                if not os.path.exists(os.path.dirname(dest_file_path)):
                    os.makedirs(os.path.dirname(dest_file_path))

                with open(dest_file_path, 'w+') as file:
                    file.write(http_response.text)


if __name__ == '__main__':
    data_url = 'https://www.hkex.com.hk/eng/stat/smstat/dayquot/d181002e.htm'
    file_path = '/home/antee/project/collector/data/d181002e.txt'
    hutil = HTTP_Utils()

    hutil.download_file(data_url, file_path)