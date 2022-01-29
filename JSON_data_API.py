"""Get the data from the Json file to the browser"""

import os
import sys
from http.server import HTTPServer, \
    BaseHTTPRequestHandler
import logging
import cgi
import json

logging.basicConfig(filename='JSON_data_API.log',
                    level=logging.INFO,
                    format='%(asctime)s: %(levelname)s:'
                           ' %(filename)s->'
                           ' %(funcName)s->'
                           ' Line %(lineno)d-> %(message)s')


class HttpRequestToResponse(BaseHTTPRequestHandler):
    """Start the basic HTTP SERVER to read the data from the file"""

    def do_GET(self):
        print("inside get")
        if self.path.endswith('/'):
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            output = 'Documentation coming soon'
            self.wfile.write(output.encode())
        if self.path.endswith('efs'):
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()

            filename = 'metropolitan_museum_api.json'
            with open(f'efs{filename}', mode='r', encoding='utf-8-sig') as file_obj:
                json_data = json.load(file_obj)
            self.wfile.write(json.dumps(json_data).encode())
        if self.path.endswith('ebs'):
            print("nothing much here")
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()

            filename = 'metropolitan_museum_api.json'
            # MyCRUDFolder
            with open(f'{filename}', mode='r', encoding='utf-8-sig') as file_obj:
                json_data = json.load(file_obj)
            self.wfile.write(json.dumps(json_data).encode())

    def do_POST(self):
        try:
            """Perform CRUD operation on the JSON data"""
            if self.path.endswith('ebs/add'):
                c_type, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                if c_type == 'multipart/form-data':
                    fields_to_insert = cgi.parse_multipart(self.rfile, pdict)
                    fields_to_insert = {key: fields_to_insert[key][0] for key in fields_to_insert}
                    filename = 'metropolitan_museum_api.json'
                    for key in fields_to_insert:
                        if fields_to_insert[key].isdigit():
                            fields_to_insert[key] = int(fields_to_insert[key])
                        else:
                            if fields_to_insert[key].count('.') == 1:
                                if fields_to_insert[key].replace('.', '').isdigit():
                                    fields_to_insert[key] = float(fields_to_insert[key])
                            else:
                                fields_to_insert[key] = fields_to_insert[key].replace('"', '')
                    with open(f'{filename}', 'r', encoding="utf-8-sig") as json_file:
                        json_data = json.load(json_file)
                        json_data_columns = list(json_data[0].keys())
                        json_data.append({key: fields_to_insert[key] for key in json_data_columns})
                    with open(f'{filename}', 'w', encoding="utf-8-sig") as json_file:
                        json.dump(json_data, json_file, ensure_ascii=False, indent=2)
                        json_file.truncate()

            if self.path.endswith('ebs/update'):
                c_type, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                filename = 'metropolitan_museum_api.json'
                if c_type == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    fields_to_update = {key: fields[key] for key in fields}
                    set_value = fields_to_update['set_value'][0]
                    set_value = json.loads(set_value)
                    set_value = list(set_value.items())
                    target_value = fields_to_update['target_value'][0]
                    target_value = json.loads(target_value)
                    target_value = list(target_value.items())
                    with open(f'{filename}', mode='r', encoding="utf-8-sig") as json_file:
                        json_data = json.load(json_file)
                        for dict_data in json_data:
                            for fields in target_value:
                                if str(fields[1]).isdigit():
                                    if dict_data[fields[0]] == int(fields[1]):
                                        for set_value_fields in set_value:
                                            if str(set_value_fields[1]).isdigit():
                                                dict_data[set_value_fields[0]] = int(set_value_fields[1])
                                            else:
                                                dict_data[set_value_fields[0]] = set_value_fields[1]

                                else:
                                    if dict_data[fields[0]] == fields[1]:
                                        for set_value_fields in set_value:
                                            if set_value_fields[1].isdigit():
                                                dict_data[set_value_fields[0]] = int(set_value_fields[1])
                                            else:
                                                dict_data[set_value_fields[0]] = set_value_fields[1]

                    with open(f'{filename}', mode='w', encoding='utf-8-sig') as json_file:
                        json_updated_data = json.dumps(json_data, ensure_ascii=False, indent=2)
                        json_file.write(json_updated_data)
                        json_file.truncate()
            self.send_response(301)
            self.send_header('content-type', 'application/json')
            self.send_header('Location', '/ebs')
            self.end_headers()
        except Exception as err:
            logging.error('%s: %s', err.__class__.__name__, err)
            return f"{err.__class__.__name__} error"

    def do_DELETE(self):
        try:
            if self.path.endswith('ebs'):
                c_type, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                content_len = int(self.headers.get('Content-length'))
                pdict['CONTENT-LENGTH'] = content_len
                if c_type == 'multipart/form-data':
                    delete_json_data = cgi.parse_multipart(self.rfile, pdict)
                    delete_json_data = {key: delete_json_data[key][0] for key in delete_json_data}
                    expression = list(delete_json_data.items())[0]
                    filename = 'metropolitan_museum_api.json'
                    with open(file=f'{filename}', mode='r', encoding='utf-8-sig') as json_file:
                        json_data = json.load(json_file)
                        for dict_data in json_data:
                            if expression[1].isdigit():
                                if dict_data[expression[0]] == int(expression[1]):
                                    json_data.remove(dict_data)

                            else:
                                if dict_data[expression[0]] == expression[1]:
                                    json_data.remove(dict_data)

                    with open(f'{filename}', mode='w', encoding='utf-8-sig') as json_file:
                        json_updated_data = json.dumps(json_data, ensure_ascii=False, indent=2)
                        json_file.write(json_updated_data)
                        json_file.truncate()

                self.send_response(301)
                self.send_header('content-type', 'application/json')
                self.send_header('Location', '/ebs')
                self.end_headers()
        except Exception as exc:
            logging.error('%s: %s', exc.__class__.__name__, exc)
            return f"{exc.__class__.__name__} error"


def main(domain_ip, port):
    """Function to start the HTTP server using python script"""

    server = HTTPServer((domain_ip, port), HttpRequestToResponse)
    print(f"Server started on {domain_ip}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    try:
        main(domain_ip=sys.argv[1], port=int(sys.argv[2]))
    except TypeError as type_err:
        logging.error("%s: %s", type_err.__class__.__name__, type_err)
