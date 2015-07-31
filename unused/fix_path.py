def fix_path():
    # credit:  Nick Johnson of Google
    sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

def main():
    url_map = [ ('/', views.IndexHandler),] # etc.
    app = webapp.WSGIApplication(url_map, debug=False)
    wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
    fix_path()
    main()
