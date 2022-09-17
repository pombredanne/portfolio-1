function follow(username, action) {
    fetch(`/follow/${username}/${action}`)
    .then(response => response.json())
    .then(followed => {
        document.querySelector("#followers").innerHTML = followed.followers;
    });        
}

function liked(postId, action){
    fetch(`/like/${postId}/${action}`)
    .then(response => response.json())
    .then(likes => {
        document.querySelector(`.likes-of-${(postId)}`).innerHTML = `${likes.likes} Likes`;
    });
}

function editing(postId) {
    document.querySelector(`.save${postId}`).onclick = () => {
        fetch(`/edit/${postId}`, {
            method: 'POST',
            body: JSON.stringify({
                content: document.querySelector(`.editedcontent${postId}`).value
            })
        })
        .then(response => response.json())
        .then(result => {
            document.querySelector(`.content${postId}`).innerHTML = result.content;
        });
        document.querySelector(`.editForm.${CSS.escape(postId)}`).style.display = 'none';
        document.querySelector(`.post.${CSS.escape(postId)}`).style.display = 'flex';
        var elems = document.getElementsByClassName('edithide');
        for (var i = 0; i < elems.length; i += 1) {
            elems[i].style.display = 'block';
        }
        return;
    } 
}