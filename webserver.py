from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import db and allow connection and CRUD ability
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# tells which db engine to talk to
engine = create_engine('sqlite:///restaurantmenu.db')

# connects classes to tables in db
Base.metadata.bind = engine

# link between code execution and engine
DBSession = sessionmaker(bind = engine)

# instance of session allows CRUD executions sql after a commit
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Objective 3 Step 2 - Create /restarants/new page
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body> \
						   <h1>Make a New Restaurant</h1> \
						   <form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'> \
						   <input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > \
						   <input type='submit' value='Create'> \
						   </form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                # Create a Link to create a new Restaurant
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += "<div id='restaurant'>" + restaurant.name
                    output += "</br></br>"
                    # Add Edit and Delete Links
                    output += "<a href='/restaurants/%s/edit-restaurant/'>" % restaurant.id + "Edit</a><br> \
							   </br> \
							   <a href=' #'>Delete</a><br> \
							   </div></br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit-restaurant"):
            	restaurantIDPath = self.path.split("/")[2]
            	restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
            	if restaurant != []:
		        	self.send_response(200)
		        	self.send_header('Content-type', 'text/html')
		        	self.end_headers()
		        	output = ""
		        	output += "<html><body> \
		            		   <h2>Edit your restaurant's name:</h2><br> \
		            		   <form method='POST' enctype='multipart/form-data' action='restaurants/%s/edit-restaurant'>" \
		            		   % restaurantIDPath + \
		            		  "<input name='editName' type='text' placeholder='%s'>" % restaurant.name + \
		            		  "<input type='submit' value='Edit'> \
		            		   </form> \
		            		   </html></body>"

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:
        	# puts new Restuarant name into db
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    content = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=content[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html') 
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            # edits Restaurant name in db
            if self.path.endswith("/edit-restaurant"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    content = fields.get('editName')

                    restaurantIDPath = self.path.split("/")[2]
                    # Create new Restaurant Object
                    restaurant = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    
                    if restaurant != []:
	                    restaurant.name = content[0]
	                    session.add(restaurant)
	                    session.commit()

	                    self.send_response(301)
	                    self.send_header('Content-type', 'text/html') 
	                    self.send_header('Location', '/restaurants')
	                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()