document.addEventListener("DOMContentLoaded", function() {


    let heart = document.querySelectorAll(".heart_button");
    heart.forEach(element => {

        element.addEventListener("click", function() {
            let post_id_str = this.dataset.id
            let post_id = parseInt(post_id_str)

            fetch(`posts/${post_id}`)
            .then(response => response.json())
            .then(post => {
                is_liked = post.is_liked
                if (is_liked === false) {
                    fetch(`posts/${post_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            is_liked: true
                        })
                      });

                    let heart_css = this.querySelector("#heart_css")
                    heart_css.classList.remove("bi-heart");
                    heart_css.classList.add("bi-heart-fill")

                    //update likes
                    let current_likes = post.likes
                    let new_likes = current_likes + 1
                    fetch(`posts/${post_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            likes: new_likes
                        })
                      });
                    
                    //update html likes
                    let like_count = this.parentElement.querySelector("#like_count")
                    like_count.innerHTML = new_likes;
                } 
                else {
                    fetch(`posts/${post_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            is_liked: false
                        })
                      });

                    let heart_css = this.querySelector("#heart_css")
                    heart_css.classList.remove("bi-heart-fill");
                    heart_css.classList.add("bi-heart")

                    //update likes
                    let current_likes = post.likes
                    let new_likes = current_likes - 1
                    fetch(`posts/${post_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            likes: new_likes
                        })
                      });
                      
                    let like_count = this.parentElement.querySelector("#like_count")
                    like_count.innerHTML = new_likes;
                }
            })
        })
    })
})