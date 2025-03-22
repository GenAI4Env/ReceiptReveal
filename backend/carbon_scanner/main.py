from flask import Flask, request, jsonify
from carbon_scanner.authentication.auth_manager import AuthManager
from carbon_scanner.genai.gemini_handler import text_resp, image_resp
from carbon_scanner.database.db_manager import DatabaseManager
from PIL import Image

app = Flask(__name__)
app.config["SECRET_KEY"] = "some_secret_key"
auth_manager = AuthManager(app)


@app.route("/auth/register", methods=["POST"])
async def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = await auth_manager.register_user(email, password)
    return (
        (jsonify({"message": "User registered"}), 201)
        if user
        else (jsonify({"error": "User exists"}), 400)
    )


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


@app.route("/db/prompts", methods=["POST"])
async def store_prompt():
    data = request.get_json()
    async with DatabaseManager() as db:
        await db.store_prompt_context(
            data["user_id"], data["prompt"], data.get("context")
        )
    return jsonify({"message": "Prompt stored"}), 201


@app.route("/db/prompts", methods=["GET"])
async def get_prompts():
    user_id = request.args.get("user_id", type=int)
    async with DatabaseManager() as db:
        prompts = await db.get_prompts_for_user(user_id)
    return jsonify(prompts)


if __name__ == "__main__":
    app.run(debug=True)
