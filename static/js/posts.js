let likePost = function() {
    const likeButton = document.getElementById('like');
    likeButton.classList.toggle('active');
};

let likeComment = function() {
    const likeCommentButton = document.getElementById('like-comment');
    likeCommentButton.classList.toggle('active');
};

let toggleComments = function(postID) {
    const commentBlock = document.getElementById('comment-section-to-' + postID);
    commentBlock.classList.toggle('expanded');
};