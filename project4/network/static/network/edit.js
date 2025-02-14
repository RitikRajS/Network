
document.addEventListener('DOMContentLoaded',function(){


    document.querySelectorAll('.edit_button').forEach(button =>{
        button.addEventListener('click', function(event){

            event.preventDefault();

            const postID= this.getAttribute('data-id');

            const content_post = document.querySelector(`#post_content_${postID}`);

            // Check the inner html 

            if(this.textContent.trim() === 'Edit'){

                const previous_data= content_post.innerHTML;


                const textarea = content_post.innerHTML = `
                <textarea class="editForm" id='new_content_${postID}' rows="3">${previous_data}</textarea>
                `;

                console.log('Textarea HTML:', textarea);

                const insertedTextarea = document.querySelector(`#new_content_${postID}`);
                console.log('Inserted textarea:', insertedTextarea);

                this.textContent = 'Save';

            }else if(this.textContent.trim() === 'Save'){

                const new_content = document.querySelector(`#new_content_${postID}`);

                edit(new_content,postID, content_post, this);
            }


        })
    })
})


function edit(new_content, postID, content_post, button){

    //Sending an API call 

    fetch(`/edit/${postID}`, {
        method:'PUT',
        headers:{
            'Content-Type':'application/json'},
        mode:'same-origin',
        body:JSON.stringify({content:new_content.value})
        
    })

    .then(response =>{
        if(!response.ok){
            throw new Error(`Error in the request ${response.status}`)
        }
        return response.json()
    })

    .then(data =>{
        content_post.innerHTML = data.updated_content;
        button.textContent='Edit';

    })

    .catch(error=>{
        console.error(`Error while updating the post:${error}`);
        alert(`Failed to update the post`)
    });

}
