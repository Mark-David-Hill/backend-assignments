import routes

def register_blueprints(app):
    app.register_blueprint(routes.timers)
    app.register_blueprint(routes.timer)