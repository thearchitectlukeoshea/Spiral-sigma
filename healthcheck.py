# healthcheck.py
def root_route(app):
    @app.route("/", methods=["GET"])
    def root():
        return "SIGMA ONLINE — NODE CONFIRMED"

def attach_health(app):
    root_route(app)
