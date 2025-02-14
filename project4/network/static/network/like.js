document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.likeButton').forEach(button => {
        const postID = button.getAttribute('data-id');

        const likeCount = document.querySelector(`#likeCount_${postID}`)

        let likeStatus;

        if (button.innerHTML === 'Unlike'){
            console.log('The User liked the post');
            likeStatus = true;


        } else{
            console.log('The User needs to like this post')
            likeStatus = false;
        };

        button.addEventListener('click', () =>{

            likeStatus = !likeStatus;

            button.innerHTML = likeStatus ? 'Unlike': 'Like';

            like(postID, likeStatus, likeCount)
        })
        
    })
})

function like(postID, likeStatus, likeCount){
        //Sending an API call to update like/dislike

        fetch(`/like/${postID}`, {
            method:'PUT',
            headers:{
                'Content-Type':'application/json'},
            mode:'same-origin',
            body:JSON.stringify({ like:likeStatus })
    
        })
    
        .then(response =>{
            if (!response.ok){
                throw new Error(`Error in the request ${response.status}`)
            }
            return response.json();
        })
    
        .then(data => {

            likeCount.innerHTML= data.updatedLikes;
        })
    
        .catch(error => {
            console.error('Error', error);
        })
}