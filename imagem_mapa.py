import folium

dot_1 = [-13.30,-46.18]
dot_2 = [-13.30,-45.90]
dot_3 = [-13.46,-46.18]
dot_4 = [-13.46,-45.90]

plant_location = [-13.39, -46.09]

dot_1_status = 0
dot_2_status = 0
dot_3_status = 0
dot_4_status = 1

if dot_1_status == 1:
    dot_1_color = 'lightred'
    dot_1_texto = 'Presença de Esporos'
else:
    dot_1_color = 'lightgreen'
    dot_1_texto = 'Sem Esporos'


if dot_2_status == 1:
    dot_2_color = 'lightred'
    dot_2_texto = 'Presença de Esporos'
else:
    dot_2_color = 'lightgreen'
    dot_2_texto = 'Sem Esporos'


if dot_3_status == 1:
    dot_3_color = 'lightred'
    dot_3_texto = 'Presença de Esporos'
else:
    dot_3_color = 'lightgreen'
    dot_3_texto = 'Sem Esporos'

if dot_4_status == 1:
    dot_4_color = 'lightred'
    dot_4_texto = 'Presença de Esporos'
else:
    dot_4_color = 'lightgreen'
    dot_4_texto = 'Sem Esporos'

folium_map = folium.Map(location=plant_location, zoom_start=12)

folium.Marker(location=plant_location,icon=folium.Icon(color='lightblue'),popup='Experimento').add_to(folium_map)
folium.Marker(location=dot_1,icon=folium.Icon(color=dot_1_color),popup=dot_1_texto).add_to(folium_map)
folium.Marker(location=dot_2,icon=folium.Icon(color=dot_2_color),popup=dot_2_texto).add_to(folium_map)
folium.Marker(location=dot_3,icon=folium.Icon(color=dot_3_color),popup=dot_3_texto).add_to(folium_map)
folium.Marker(location=dot_4,icon=folium.Icon(color=dot_4_color),popup=dot_4_texto).add_to(folium_map)



# ------------------------------------------------------------------------------------------------
# so let's write a custom temporary-HTML renderer
# pretty much copy-paste of this answer: https://stackoverflow.com/a/38945907/3494126
import subprocess
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


PORT = 7788
HOST = 'localhost'
SERVER_ADDRESS = '{host}:{port}'.format(host=HOST, port=PORT)
FULL_SERVER_ADDRESS = 'http://' + SERVER_ADDRESS + '/'


def TemproraryHttpServer(page_content_type, raw_data):
    """
    A simpe, temprorary http web server on the pure Python 3.
    It has features for processing pages with a XML or HTML content.
    """

    class HTTPServerRequestHandler(BaseHTTPRequestHandler):
        """
        An handler of request for the server, hosting XML-pages.
        """

        def do_GET(self):
            """Handle GET requests"""

            # response from page
            self.send_response(200)

            # set up headers for pages
            content_type = 'text/{0}'.format(page_content_type)
            self.send_header('Content-type', content_type)
            self.end_headers()

            # writing data on a page
            self.wfile.write(bytes(raw_data, encoding='utf'))

            return

    if page_content_type not in ['html', 'xml']:
        raise ValueError('This server can serve only HTML or XML pages.')

    page_content_type = page_content_type

    # kill a process, hosted on a localhost:PORT
    subprocess.call(['fuser', '-k', '{0}/tcp'.format(PORT)])

    # Started creating a temprorary http server.
    httpd = HTTPServer((HOST, PORT), HTTPServerRequestHandler)

    # run a temprorary http server
    httpd.serve_forever()


def run_html_server(html_data=None):

    if html_data is None:
        html_data = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Page Title</title>
        </head>
        <body>
        <h1>This is a Heading</h1>
        <p>This is a paragraph.</p>
        </body>
        </html>
        """



    # open in a browser URL and see a result
    webbrowser.open(FULL_SERVER_ADDRESS)

  # run server
    TemproraryHttpServer('html', html_data)

# ------------------------------------------------------------------------------------------------


# now let's save the visualization into the temp file and render it
from tempfile import NamedTemporaryFile
tmp = NamedTemporaryFile()
folium_map.save(tmp.name)
folium_map.save("/home/rodfranco/teste.html")
with open(tmp.name) as f:
    folium_map_html = f.read()

run_html_server(folium_map_html)



