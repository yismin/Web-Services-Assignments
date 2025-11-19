from flask import Flask
from flask_smorest import Api
from resources.course_item import blp as CourseItemBlueprint
from resources.specializations import blp as SpecializationBlueprint

app = Flask(__name__)

# Flask-Smorest / Swagger configuration
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Specialization REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"                  # Base path for OpenAPI
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


# Initialize API
api = Api(app)

# Register blueprints
api.register_blueprint(CourseItemBlueprint)
api.register_blueprint(SpecializationBlueprint)

# Minimal test route to verify container is working
@app.route("/ping")
def ping():
    return {"message": "pong"}

# Run the app directly (works reliably in Docker)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)