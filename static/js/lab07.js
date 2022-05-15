const toggleFollow = ev => {
    console.log(ev)
    const elem = ev.currentTarget;
    console.log(elem.dataset)
    console.log(elem.dataset.userId)
    console.log(elem.innerHTML);
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

    fetch("https://photo-app-acd.herokuapp.com/api/following/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)   
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
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

    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
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
        console.log(users);
        const html = users.map(user2Html).join('\n');
        document.querySelector('#suggestions').innerHTML = html;
    });
};

getSuggestions();
