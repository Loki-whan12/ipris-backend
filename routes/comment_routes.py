from flask import Blueprint, request, jsonify
from db_init import db
from models import Comment


comment_bp = Blueprint('comment_bp', __name__)

# Create a new comment
@comment_bp.route('/create', methods=['POST'])
def create_comment():
    data = request.get_json()
    new_comment = Comment(comment=data['comment'], rate=data['rate'], username=data['username'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully'}), 201


# Get all comments
@comment_bp.route('/all', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    if comments:
        return jsonify([{'id': comment.id, 'comment': comment.comment, 'rate': comment.rate, 'username': comment.username} for comment in comments])
    return jsonify({'message': 'No comments found'}), 404


# Get a comment by id
@comment_bp.route('/<int:id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        return jsonify({'message': 'Comment not found'}), 404
    return jsonify({'id': comment.id, 'comment': comment.comment, 'rate': comment.rate, 'username': comment.username})


# Delete a comment
@comment_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        return jsonify({'message': 'Comment not found'}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200


# Update a comment
@comment_bp.route('/update/<int:id>', methods=['PUT'])
def update_comment(id):
    data = request.get_json()
    comment = Comment.query.get(id)
    if comment is None:
        return jsonify({'message': 'Comment not found'}), 404
    comment.comment = data['comment']
    comment.rate = data['rate']
    db.session.commit()
    return jsonify({'message': 'Comment updated successfully'}), 200