// STORIES 

const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('https://photo-app-acd.herokuapp.com/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};

// USER

const self2Html = user => {
    return `<div class = "me"> 
                <img src = "${user.thumb_url}">
                <h1> ${user.username} </h1>
            </div>
            <h2> Suggestions for you </h2>`
}


const displaySelf = () => {
    fetch('https://photo-app-acd.herokuapp.com/api/profile')
        .then(response=> response.json())
        .then(prof => {
            const html = self2Html(prof);
            document.querySelector('.self').innerHTML = html;
        });
};


// SUGGESTED

const toggleFollow = ev => {
    const elem = ev.currentTarget;
    if (elem.innerHTML === 'follow') {
        followUser(elem.dataset.userId, elem);
    }
    else {
        unfollowUser(elem.dataset.followingId, elem)
    }
}

const followUser = (userId, elem) => {
    const postData = {
        "user_id": userId
    };

    fetch('https://photo-app-acd.herokuapp.com/api/following/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
        body: JSON.stringify(postData)   
    })
    .then(response => response.json())
    .then(data => {
        elem.innerHTML = 'unfollow'
        elem.classList.add('unfollow');
        elem.classList.remove('follow');
        elem.setAttribute('aria-checked', 'true');
        elem.setAttribute('data-following-id', data.id);
    });
};

const unfollowUser = (followingId, elem) => {
    const deleteURL = `https://photo-app-acd.herokuapp.com/api/following/${followingId}`;
    fetch(deleteURL, {
        method: "DELETE",
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
    })
    .then(response => response.json())
    .then(data => {
        elem.innerHTML = 'follow'
        elem.classList.add('follow');
        elem.classList.remove('unfollow')
        elem.removeAttribute('data-following-id');
        elem.setAttribute('aria-checked', 'false');
    });
}

const user2Html = user => {
    return `
    <div class="suggestion">
                    <img src = "${user.thumb_url}">
                    <div>
                        <p class="username">${user.username}</p>
                        <p class="suggestion-text">suggested for you</p>
                    </div>
                    <div>
                        <button class="follow" 
                        aria-label = "Follow" 
                        aria-checked = "false" 
                        data-user-id ="${user.id}" onclick = "toggleFollow(event);">follow</button>
                    </div>
                </div>
    `;
}

const getSuggestions = () => {
    fetch('https://photo-app-acd.herokuapp.com/api/suggestions/')
    .then(response => response.json())
    .then(users => {
        const html = users.map(user2Html).join('\n');
        document.querySelector('.suggestions').innerHTML = html;
    });
};


// POSTS

const displayPosts = () => {
    fetch('https://photo-app-acd.herokuapp.com/api/posts/')
    .then(response => response.json())
    .then(posts => {
            posts.splice(10);
            const html = posts.map(posts2Html).join('\n');
            document.querySelector('#posts').innerHTML = html;
    });
};

var lastFocus;

const toggleOpenModal = ev => {
    const elem = ev.currentTarget;
    lastFocus = document.activeElement;
    let modal = elem.nextSibling;
    modal.style.display = "flex";
    modal.getAttribute('aria-hidden') = "false";

    currentId = elem.id;
    closeButton =  document.querySelector("#close" + String(currentId));
    console.log("toggleOpenModel");
    console.log(closeButton);
    closeButton.innterHTML = "focus(event);";

    document.addEventListener("focus", function(event) {
        dialog = closeButton;
        
        if (dialog && !dialog.contains(event.target)) {
            event.stopPropagation();
            dialog.focus();
        }
    
    }, true);

    closeButton.tabIndex = -1;
    closeButton.focus();
    
    let bod = document.querySelector("body");
    bod.style.overflow = "hidden";
};



const toggleCloseModal = ev => {
    const elem = ev.currentTarget;
    lastFocus.focus();
    let modal = elem.parentNode;
    modal.style.display = "none";
    let bod = document.querySelector("body");
    bod.style.overflow = "auto";
};

const toggleLike = (ev) => {
    const elem = ev.currentTarget;
    console.log(elem.getAttribute('aria-check'));
    if (elem.getAttribute('aria-check') === "true") {
        
        unlikePost(Number(elem.getAttribute('data-postLikeId')))
        
    }
    else {
        likePost(Number(elem.id));
    }

};

const likePost = (postId) => {
    const postData = {
        "post_id": postId
    };
    fetch("https://photo-app-acd.herokuapp.com/api/posts/likes/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
        body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayPosts();
        }); 
};

const unlikePost = (postLikeId) => {
    const url = `https://photo-app-acd.herokuapp.com/api/posts/likes/${postLikeId}`;
    fetch(url, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayPosts();
        });
};


const toggleBookmark = (ev) => {
    const elem = ev.currentTarget;
    if (elem.getAttribute('aria-check') === "true") {
        
        unbookmarkPost(Number(elem.getAttribute('data-postBookmarkId')))
        
    }
    else {
        bookmarkPost(Number(elem.id));
    }

};

const unbookmarkPost = (postBookmarkId) => {
    const url = `https://photo-app-acd.herokuapp.com/api/bookmarks/${postBookmarkId}`;
    fetch(url, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayPosts();
        });
};

const bookmarkPost = (postId) => {
    const postData = {
        "post_id": postId
    };
    fetch("https://photo-app-acd.herokuapp.com/api/bookmarks/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token')
        },
        body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayPosts();
        }); 
};

const posts2Html = (post) => {
    let likes = post.likes;
    let numOfLikes = likes.length;

    var ariaStuff = "false";
    heartOrNot = `<i class="far fa-heart"></i>`;
    for (let i = 0; i < numOfLikes; i++) {
        if (post.current_user_like_id && likes[i].id === post.current_user_like_id)
        {
            ariaStuff = "true";
            heartOrNot = `<i class="fas fa-heart"></i>`;
        } 
    }

    var userBookmark = post.current_user_bookmark_id;
    var bookmarkedOrNot = `<i class="far fa-bookmark"></i>`;
    var ariaStuffBookmark = "false";

    if (userBookmark) {
        bookmarkedOrNot = `<i class="fas fa-bookmark"></i>`;
        ariaStuffBookmark = "true";
    }

    let allCom = post.comments;
    let allComHtml  = ``;
    let viewComHtml = ``;

    for (let i = 0; i < allCom.length; i++) {
        let com = allCom[i];
        allComHtml += `<div class = "with-heart"> 
                            <div class="com">
                                    <span class="username"> ${com.user.username} </span>
                                    <span class="comment"> ${com.text} </span>
                            </div>
                            <i class="far fa-heart" id="com-heart"></i>
                        </div>
                        <div class="interfacetextcom"> ${com.display_time} </div>
                        `;   
        if (i == allCom.length - 1 && allCom.length != 0) {
            viewComHtml = viewComHtml + 
                        `<div class="com">
                        <span class="username"> ${com.user.username} </span>
                        <span class="comment"> ${com.text} </span>
                        </div>
                        <div class="interfacetextcom"> ${com.display_time} </div>
                        `;   
        }
    }

    if (allCom.length > 1) {
        viewComHtml = `<br>
                        <button class="linkcom" id = ${post.id} onclick = "toggleOpenModal(event);"> View all ${allCom.length} comments </button>`
                        + 
                        `<div class = "modal" aria-hidden = "true" role="dialog">
                            <div class = "focused">
                                <img src="${post.image_url} " id="post-image-focus">
                                <div class = "comment-box-focus"> 
                                    <div class = "post-user"> 
                                        <img src="${post.user.thumb_url} "id="im">
                                        <span class="post-usern"> ${post.user.username} </span>
                                        <hr>
                                    </div>
                                    ${allComHtml}
                                </div>
                            </div>
                            <button class="close" id = close${post.id} onclick = "toggleCloseModal(event);">X</button>
                        </div>`
                        + viewComHtml;
    } 

    viewComHtml = `<div class="com">
                        <span class="username"> ${post.user.username} </span>
                        <span class="comment"> ${post.caption} </span>
                        </div>
                        <div class="interfacetextcom"> ${post.display_time} </div>
                        ` + viewComHtml; 

    return `<div class="post"> 
                <div class="top-post">
                    <span class="poster"> ${post.user.username} </span>
                    <i class="fas fa-ellipsis-h"></i>
                </div>

                <img src="${post.image_url} " id="post-image">
                
                <div class="icons"> 
                    <div class="right-icons">
                        <button class="like-heart" id = ${post.id} data-postLikeId = ${post.current_user_like_id} 
                            aria-label = "Like / Unlike button" aria-check = ${ariaStuff}
                            onclick = "toggleLike(event);" >${heartOrNot}</button>
                        <i class="far fa-comment"></i>
                        <i class="far fa-paper-plane"></i>
                    </div>
                    <div class="left-icon">
                        <button class="bookmark-bookmark" id = ${post.id} onclick = "toggleBookmark(event);" 
                        data-postBookmarkId = ${post.current_user_bookmark_id} aria-label = "Bookmark / Unbookmark button" aria-check = ${ariaStuffBookmark}
                        >${bookmarkedOrNot}</button>
                    </div>
                </div>
                
                <div class="like">
                    <span class="likecount"> ${numOfLikes} likes </span>
                </div>
                
                ${viewComHtml}

                <hr>

                <div class="comment-box">
                    <div class="left-comment-box">
                        <div class="smiley">
                            <i class="far fa-smile"></i>
                        </div>
                        <input type = "text" placeholder = "Add a comment...">
                    </div>
                    <button class="link" id = ${post.id} onclick = "toggleComment(event);"> Post </button>
                </div> 
            </div>`
};


// COMMENTS
const toggleComment = (ev) => {
    const elem = ev.currentTarget;
    var currentComment = elem.previousSibling.previousSibling.lastChild.previousElementSibling;
    if (currentComment.value)
    {
        postComment(Number(elem.id), currentComment.value);
    }
};

const postComment = (postId, text) => {
    const postData = {
        "post_id": postId,
        "text": text
    };
    
    fetch("https://photo-app-acd.herokuapp.com/api/comments", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token')
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            displayPosts();
        });
};

const initPage = async () => {
    displaySelf();
    displayStories();
    getSuggestions();
    displayPosts();
};

// invoke init page to display stories:
initPage();