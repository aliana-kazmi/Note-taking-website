from Project_I import create_app

app=create_app()

if __name__=='__main__':
    app.run(debug=True)
    #to stop the web server from running if this program is imported