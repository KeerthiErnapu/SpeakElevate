from flask import Flask, render_template, request, jsonify
import language_tool_python
from flask_pymongo import PyMongo
import random
import bcrypt
# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SpeakElevate"
mongo = PyMongo(app)

# Initialize LanguageTool API for grammar and spelling checks
tool = language_tool_python.LanguageTool('en-US')

# Set of 20 predefined topics
predefined_topics = [
    "The impact of climate change on global agriculture",
    "The role of social media in modern communication",
    "How artificial intelligence is transforming industries",
    "The importance of mental health awareness in schools",
    "The future of renewable energy sources",
    "How to reduce waste and promote sustainability",
    "The effects of technology on human relationships",
    "The benefits and challenges of online education",
    "The role of women in leadership positions",
    "The influence of music on emotions and well-being",
    "The importance of financial literacy in the modern world",
    "Exploring the impact of fast fashion on the environment",
    "The role of artificial intelligence in healthcare",
    "The significance of space exploration for humanity",
    "How sports can promote teamwork and discipline",
    "The ethical implications of gene editing",
    "The rise of automation and its effects on jobs",
    "The impact of social media on self-esteem",
    "The importance of cybersecurity in the digital age",
    "The challenges of living in a multicultural society"
]

# Function to generate a random topic from predefined list
def generate_random_topic():
    return random.choice(predefined_topics)

@app.route('/')
def index():
    # Render the main page with buttons for navigation
    return render_template('index.html')
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Retrieve email only if it's a POST request (form submission)
        email = request.form['email']
        
        # Check if the email exists in the database
        user = mongo.db.demo.find_one({'email': email})

        if user:
            # If email exists, render reset password page
            return render_template('reset-pwd.html', email=email)
        else:
            # If email does not exist, show error message on the same page
            return render_template('forgot-password.html', error="Email not found, register first")

    # If it's a GET request, just render the forgot password form
    return render_template('forgot-password.html')

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form['email']  # Get the email passed from forgot-password route
    new_password = request.form['password']
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    # Update the password in the database
    mongo.db.demo.update_one(
        {'email': email},
        {'$set': {'password': hashed_password}}  # Update the user's password
    )

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get data from the signup form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        existing_user = mongo.db.demo.find_one({'email': email})

        if existing_user:
            # Email already exists, show error message
            return render_template('signup.html', error="Email already exists.")

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create a new user and insert it into the database
        mongo.db.demo.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        })

        # Redirect to the login page with a success message
        return render_template('login.html', message="Account created successfully! Please log in.")

    # Render the signup page if it's a GET request
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Check if email exists in the database
        user = mongo.db.demo.find_one({'email': email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return render_template('sample.html')
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')



@app.route('/interview-tests')
def interview_tests():
    # Render the Interview Tests page with the GD, Technical, HR options
    return render_template('interview-tests.html')

@app.route('/gd-practice')
def gd_practice():
    # Render the Group Discussion practice page
    return render_template('gd-practice.html')

@app.route('/technical-practice')
def technical_practice():
    # Render the Technical Interview practice page
    return render_template('technical-practice.html')
@app.route('/sql-practice')
def sql_practice():
    return render_template('sql-practice.html')
@app.route('/os-practice')
def os_practice():
    return render_template('os-practice.html')
@app.route('/cn-practice')
def cn_practice():
    return render_template('cn-practice.html')
@app.route('/java-practice')
def java_practice():
    return render_template('java-practice.html')
@app.route('/node-practice')
def node_practice():
    return render_template('node-practice.html')
@app.route('/python-practice')
def python_practice():
    return render_template('python-practice.html')

@app.route('/sample')
def sample():
    # Render the Technical Interview practice page
    return render_template('sample.html')
@app.route('/hr-practice')
def hr_practice():
    # Render the HR Interview practice page
    return render_template('hr-practice.html')

@app.route('/generate-topic', methods=['GET'])
def generate_topic_route():
    try:
        # Fetch random topic from predefined list
        topic = generate_random_topic()
        return jsonify({'topic': topic})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        # Get the transcribed text from the request
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Check for grammar and spelling mistakes using LanguageTool
        matches = tool.check(text)

        # Create a list for feedback
        grammar_issues = []
        spelling_feedback = []
        word_suggestions = []

        for match in matches:
            if "MORFOLOGIK_RULE_EN_US" in match.ruleId or "SPELLER" in match.ruleId:
                # This is a spelling mistake
                spelling_feedback.append(f"Spelling mistake: '{match.context}' should be corrected to '{match.replacements}'")
            else:
                # This is a grammar issue
                grammar_issues.append(match.message)
            
            # Check if replacements exist for the words that are wrongly used
            if match.replacements:
                for replacement in match.replacements:
                    word_suggestions.append(f"{match.context} -> use {replacement}")

        # Prepare the feedback
        feedback = {
            'grammar_issues': grammar_issues if grammar_issues else ["No grammar issues found"],
            'spelling_feedback': spelling_feedback if spelling_feedback else ["No spelling issues found"],
            'word_suggestions': word_suggestions if word_suggestions else ["No word usage errors found"],
            'corrected_text': language_tool_python.utils.correct(text, matches)
        }

        return jsonify(feedback)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)