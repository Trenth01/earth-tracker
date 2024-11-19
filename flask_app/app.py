from web import init_app

if __name__ == '__main__':
    app = init_app()
    current_host = app.config.get('HOST')
    current_port = app.config.get('PORT')
    app.run(host='0.0.0.0', port=5000, debug=True)