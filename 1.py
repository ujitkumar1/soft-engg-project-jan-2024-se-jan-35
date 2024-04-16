from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post(title='{self.title}', description='{self.description}', tags='{self.tags}')"

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags')

    if not (title and description and tags):
        return jsonify({"error": "Title, description, and tags are required"}), 400

    # Save the post to the database
    post = Post(title=title, description=description, tags=tags)
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created successfully", "postId": post.id}), 201

@app.route('/search_users', methods=['GET'])
def search_users():
    search_term = request.args.get('search_term')

    if not search_term:
        return jsonify({"error": "Search term is required"}), 400

    # Dummy data for demonstration purposes
    users = [
        {"id": "1", "username": "user1"},
        {"id": "2", "username": "user2"},
        {"id": "3", "username": "user3"},
    ]

    results = [user for user in users if search_term.lower() in user['username'].lower()]

    if not results:
        return jsonify({"message": "No users found"}), 404

    return jsonify(results), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
