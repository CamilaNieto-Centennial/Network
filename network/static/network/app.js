
// Get cookie function useful for 'submitEdit' function
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}

// Submit Edit Post
function submitEdit(id) {
    let textareaEdit = document.getElementById(`textarea${id}`);
    console.log(textareaEdit.value);

    let descriptionPost = document.getElementById(`description${id}`)
    let modal = document.getElementById(`editPost${id}`)

    fetch(`/editPost/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({
            description: textareaEdit.value
        })
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            // Update automatically the description from the post card
            descriptionPost.innerHTML = data.data;
        })
}

// Like button from the Main page on each post
function likeHandler(id, postsLiked, postLike) {
    let heartButton = document.getElementById(`heartButton${id}`);

    //heartButton.remove
    heartButton.innerHTML = ''

    let liked = false;
    if (postsLiked.indexOf(id) >= 0) {
        liked = true;
    }

    if (liked === true) {
        fetch(`/unlike/${id}`)
            .then((response) => response.json())
            .then((data) => {
                console.log('Unlike: ' + id);
                console.log(data);
                //up
                heartButton.innerHTML =
                    `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                </svg>
                <strong>${postLike}</strong>
                `
                console.log(heartButton.innerHTML)
                location.reload();
            })
    }
    else {
        fetch(`/like/${id}`)
            .then((response) => response.json())
            .then((data) => {
                console.log('Like: ' + id);
                console.log(data);
                //down
                heartButton.innerHTML =
                    `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                class="bi bi-heart-fill" viewBox="0 0 16 16">
                    <path fill-rule="evenodd"
                        d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z" />
                </svg>
                <strong>${postLike}</strong>
                `
                console.log(heartButton.innerHTML)
                location.reload();
            })
    }
    liked = !liked
}

