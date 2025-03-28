from flask import Flask, request, jsonify
from carbon_scanner.authentication.auth_manager import AuthManager
from carbon_scanner.genai.gemini_handler import text_resp, image_resp, reciept_resp
from carbon_scanner.database.db_manager import DatabaseManager
from carbon_scanner.database.sqllite_manager import insert_user, get_coins, inc_coins
from PIL import Image
from carbon_scanner.config import config
from carbon_scanner.images import ImageUploader
from flask_cors import CORS, cross_origin
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

app = Flask(__name__)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"
app.config["UPLOAD_FOLDER"] = "uploads"  # Configure upload folder
app.config["SECRET_KEY"] = config.SECRET_KEY

# Create upload folder if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Initialize database manager
db_manager = DatabaseManager()
db_manager.init_app(app)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


auth_manager = AuthManager(app)


@app.route("/auth/register", methods=["POST"])
async def register():
    data = request.get_json()
    email = data.get("email")
    print(email, type(email))
    insert_user(email, 0)
    return jsonify({"message": "User registered successfully"}), 201
#    password = data.get("password")
#    user = await auth_manager.register_user(email, password)
#    return (
#        (jsonify({"message": "User registered"}), 201)
#        if user
#        else (jsonify({"error": "User exists"}), 400)
#    )


@app.route("/auth/login", methods=["POST"])
async def login():
    data = request.get_json()
    user = await auth_manager.login(data.get("email"), data.get("password"))
    return (
        jsonify({"message": "Logged in"})
        if user
        else (jsonify({"error": "Invalid credentials"}), 401)
    )


@app.route("/auth/logout", methods=["POST"])
def logout():
    auth_manager.logout()
    return jsonify({"message": "Logged out"})


@app.route("/genai/text", methods=["POST"])
def genai_text():
    prompt = request.json.get("prompt", "")
    response = text_resp(prompt)
    return jsonify({"response": response})


@app.route("/genai/image", methods=["POST"])
def genai_image():
    file = request.files.get("image")
    prompt = request.form.get("prompt", "")
    if not file:
        return jsonify({"error": "No image provided"}), 400
    image_file = Image.open(file)
    return jsonify({"response": image_resp(prompt, image_file)})


@app.route("/genai/reciept", methods=["POST"])
def genai_reciept():
    print(f"i have recieved a reciept : {request.files}")
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No image provided"}), 400
    image_file = Image.open(file)
    return jsonify({"response": reciept_resp(image_file)})


@app.route("/db/prompts", methods=["POST"])
async def store_prompt():
    data = request.get_json()
    async with DatabaseManager() as db:
        await db.store_prompt_context(
            data["user_id"], data["prompt"], data.get("context")
        )
    return jsonify({"message": "Prompt stored"}), 201


@app.route("/db/coinsget", methods=["POST"])
async def get_prompts():
    data = request.get_json()
#        prompts = await db.get_prompts_for_user(user_id)
    return get_coins(data.get("email"))
    #return jsonify(prompts/)


@app.route("/db/coins", methods=["POST"])
async def update_coins():
    data = request.get_json()
    #user = await auth_manager.login(data.get("email"), data.get("password"))
    if coins := data.get("coins"):
        inc_coins(data.get("email"), coins)
#        result = await db_manager.update_coins_by_id(user_id=user.id, amount=coins)
#        return (
#            (jsonify({"message": "Coins updated"}), 201)
#            if result
#            else (jsonify({"message": "Failed to update coins"}), 400)
#        )
#
#    coins = await db_manager.get_coins_by_id(user.id)
    print("HELLLL YEA3")
    return jsonify({"coins": get_coins(data.get("email"))})


@app.route("/api/upload", methods=["POST"])
@login_required
async def upload_image():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files["image"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            # Save the image
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            # Process the image with Gemini
            response = await image_resp(
                "Analyze this receipt and extract the total amount and items purchased.",
                file_path,
            )

            # Increment user's coins by 10
            await db_manager.change_coins(current_user.id, 10)

            return jsonify(
                {"message": "Image uploaded successfully", "response": response}
            )
        else:
            return jsonify({"error": "Invalid file type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def main():
    app.run(debug=True)


if __name__ == "__main__":
    print(config.DATABASE_URL)
    main()