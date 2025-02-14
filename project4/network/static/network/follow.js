document.addEventListener('DOMContentLoaded', ()=> {

    const followContainer = document.querySelector('.followContainer');

    if (followContainer){
        const followButton = document.querySelector('.followButton');
        let followStatus; 
    
        const loggedUser= document.querySelector('#loggedUser').innerHTML;
    
        if (followButton.innerHTML === 'Follow'){
    
            followStatus = false;
    
        } else{
    
            followStatus = true;
        };
    
        followButton.addEventListener('click', () =>{
    
            followStatus = !followStatus;
    
            followButton.innerHTML = followStatus ? 'Unfollow':'Follow';
    
            follow(loggedUser, followStatus);
        })

    }

})

function follow(loggedUser, followStatus){

    // Sending an API call 

    fetch(`/profile/${loggedUser}`, {
        method:'PUT',
        headers:{'Content-Type':'application/json'},
        mode:'same-origin',
        body:JSON.stringify({
            follow:followStatus
        })
    })
    .then(response =>{
        if (!response.ok){
            throw new Error(`Error in the request ${response.status}`)
        }
        return response.json();
    })

    .then(data => {
        
        // Update the UI based on the API call 
        
        document.querySelector('#follower_count').innerHTML= data.follower_count;
    })

    .catch(error => {
        console.error('Error', error);
    })

}