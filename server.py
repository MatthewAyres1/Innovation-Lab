from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests
import json

data = {}
ip = "192.168.1.23"
ip = "172.23.129.18"

class WebServerHandler(BaseHTTPRequestHandler):
    
    def set_common_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()
    
    def do_GET(self):
        global data
        if self.path == "/":
            try:
                with open('index.html', 'r') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.set_common_headers()
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.set_common_headers()
                self.wfile.write(b'Index file not found')
        elif self.path.endswith("/styles.css"):
            try:
                with open('styles.css', 'r') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css')
                    self.set_common_headers()
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.set_common_headers()
                self.wfile.write(b'CSS file not found')

        elif self.path.endswith("/client.js"):
            try:
                with open('client.js', 'r') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/javascript')
                    self.set_common_headers()
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.set_common_headers()
                self.wfile.write(b'JS file not found')

        elif self.path.endswith("/table.js"):
            try:
                with open('table.js', 'r') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/javascript')
                    self.set_common_headers()
                    self.wfile.write(f.read().encode())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.set_common_headers()
                self.wfile.write(b'JS file not found')
        elif self.path.endswith("/read"):
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.set_common_headers()
            self.wfile.write(json.dumps(data).encode())
        elif self.path.startswith("/recipe"):
            # Parse the URL
            parsed_url = urlparse(self.path)
            
            # Extract the query parameters
            params = parse_qs(parsed_url.query)
            
            # Now you can access the parameters as a dictionary
            ingredients =          params.get('ingredients',          ['[]'])[0].replace("[", "").replace("]", "").split(",")
            mandatoryIngredients = [params.get('must', [])[0]]

            url = 'https://realfood.tesco.com/api/ingredientsearch/getrecipes'
            
            data = {
                # These are a harcoded example. Anything is fine, but make to use at least 3 ingredients and only use terms defined
                # in ingredients.txt
                'ingredients': ingredients,
                'mandatoryIngredients': mandatoryIngredients,
                'dietaryRequirements': []
            }
            response = requests.post(url, json=data)

            json_data = response.json()
            #print(json.dumps(json_data, indent=2))

            # Just names
            response = ""
            for recipe in json_data['results']:
                name = recipe['recipeName']
                response += f"<p>{name}</p>"
                #print(f"{name}")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.set_common_headers()
            self.wfile.write(json.dumps(json_data).encode())

    def do_POST(self):
        global data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        if self.path.endswith("/update"):
            json_data = json.loads(post_data)

            # Update data.json with the new data
            with open('data.json', 'w') as f:
                json.dump(json_data, f)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.set_common_headers()
            self.wfile.write(b'Data updated successfully')
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.set_common_headers()


    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.set_common_headers()




def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
