function voted(sourceId, action) {
    fetch(`vote/${sourceId}/${action}`)
    .then(response => response.json())
    .then(votes => {
        document.querySelector(`.votes-of-${(sourceId)}`).innerHTML = votes.votes;
    });
}

function saved(sourceId, action) {
    fetch(`save/${sourceId}/${action}`)
    .then(response => response.json())
    .then(save => {
        if (save.button === "Unsave") {
            document.querySelector(`.save${(sourceId)}`).innerHTML = "bookmark";
        }
        else if (save.button === "Save") {
            document.querySelector(`.save${(sourceId)}`).innerHTML = "bookmark_border";
        }
        
    });
}

function deleting(sourceId) {
    fetch(`delete/${sourceId}`)
    .then(response => response.json())
    .then(deleted => {
        console.log(deleted.done);
        if (deleted.done === "Deleted!") {
            delete_source = document.querySelector(`.source${sourceId}`);
            delete_source.remove();
        }
        else {
            alert(deleted.done);
        }
    });
}


function check_save(sourceId) {
    fetch(`checksave/${sourceId}`)
    .then(response => response.json())
    .then(saved => {
        if (saved.save === "Unsave") {
            document.querySelector(`.save${(sourceId)}`).innerHTML = "bookmark";
        }
        
    });
}


function check_vote(sourceId) {
    fetch(`checkvote/${sourceId}`)
    .then(response => response.json())
    .then(voted => {
        if (voted.vote === "up") {
            document.querySelector(`.up${(sourceId)}`).style.color = "#BBC8BA";
            document.querySelector(`.upicon${(sourceId)}`).style.background = "#00419c";
            disableVote = document.querySelector(`.downicon${(sourceId)}`);
            disableVote.disabled = true;
            disableVote.classList.remove("vote-icons");
            disableVote.classList.add("vote-icons-disabled");
            document.querySelector(`.down${(sourceId)}`).style.color = "grey";
        }

        else if (voted.vote === "down") {
            document.querySelector(`.down${(sourceId)}`).style.color = "#BBC8BA";
            document.querySelector(`.downicon${(sourceId)}`).style.background = "#00419c";
            disableVote = document.querySelector(`.upicon${(sourceId)}`);
            disableVote.disabled = true;
            disableVote.classList.remove("vote-icons");
            disableVote.classList.add("vote-icons-disabled");
            document.querySelector(`.up${(sourceId)}`).style.color = "grey";
        }
    });
}


function voting(action, sourceId, vote, isLoggedIn) {
    var acting;
    var opp;

    // Set classes for query selectors based on whether upvoting or downvoting

    if (action === "upvote") {
        acting = "up";
        opp = "down";
    }

    else if (action === "downvote") {
        acting = "down";
        opp = "up";
    }
    
    if (isLoggedIn === "True") {
        const voteBtn = document.querySelector(`.${(opp)}icon${(sourceId)}`);
        // Undo Vote
        if (voteBtn.disabled === false) {
            vote.style.background = "#00419c";
            document.querySelector(`.${(acting)}${(sourceId)}`).style.color = "#BBC8BA";
            voteBtn.disabled = true;
            voteBtn.classList.remove("vote-icons");
            voteBtn.classList.add("vote-icons-disabled");
            document.querySelector(`.${(opp)}${(sourceId)}`).style.color = "grey";
            voted(sourceId, acting);
            
        }

        // Vote
        else {
            vote.style.background = "transparent";
            document.querySelector(`.${(acting)}${(sourceId)}`).style.color = "#00419c";
            voteBtn.disabled = false;
            voteBtn.classList.remove("vote-icons-disabled");
            voteBtn.classList.add("vote-icons");
            document.querySelector(`.${(opp)}${(sourceId)}`).style.color = "#00419c";
            voted(sourceId, `undo_${(acting)}`);
        }
    }

    else {
        alert("Login to vote.");
    }

}

function saving(save, sourceId, isLoggedIn) {
    if (isLoggedIn === "True") {
        // Save
        if (save.innerHTML === "bookmark_border") {
            saved(sourceId, 'save');
        }
        // Unsave 
        else {
            saved(sourceId, 'unsave');
        }
    }

    else {
        alert("Login to save.")
    }
}


function deleteModal(sourceId) {
    const modal = document.querySelector(".delete-modal");
    modal.showModal();
    document.querySelector(".cancel-delete").onclick = () => {
        modal.close();
    }
    document.querySelector(".confirm-delete").onclick = () => {
        modal.close();
        deleting(sourceId);
    }
} 

document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav');
    
    navToggle.addEventListener('click', () => {
        nav.classList.toggle('nav--visible');
    })


    // Prevent Form Resubmission
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
})