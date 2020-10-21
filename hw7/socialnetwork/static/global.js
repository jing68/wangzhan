// Sends a new request to update the to-do list
function getList() {
    $.ajax({
        url: "/social/get-list",
        dataType : "json",
        success: updatePage,
        error: updateError
    });
}

function refreshGlobal() {
    $.ajax({
        url: "/social/refresh-global",
        dataType: "json",
        success: updatePage2,
        error:updateError
    });
}

function refreshFollower() {
    $.ajax({
        url:"/social/refresh-follower",
        dataType:"json",
        success:updatePage3,
        error:updateError
    });
}

function updatePage(response) {
    if (Array.isArray(response)) {
        updateList(response)
    } else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } else {
        displayError(response)
    }
}
function updatePage2(response) {
    if (Array.isArray(response.response_posts)) {
        updateListPosts(response.response_posts,response.login_user_id)
    } else if (response.response_posts.hasOwnProperty('error')) {
        displayError(response.response_posts.error)
    } else {
        displayError(response.response_posts)
    }
    console.log('the post update page is done')
    if (Array.isArray(response.response_comments)) {
        updateListComments(response.response_comments,response.login_user_id)

    } else if (response.response_comments.hasOwnProperty('error')) {
        displayError(response.response_comments.error)
    } else {
        displayError(response.response_comments)
    }   
}

function updatePage3(response) {
    if (Array.isArray(response.response_posts)) {
        updateFollowerPosts(response.response_posts,response.login_user_id,response.followlist)
    } else if (response.response_posts.hasOwnProperty('error')) {
        displayError(response.response_posts.error)
    } else {
        displayError(response.response_posts)
    }
    console.log('the post update page is done')
    if (Array.isArray(response.response_comments)) {
        updateFollowerComments(response.response_comments,response.login_user_id,response.followlist)

    } else if (response.response_comments.hasOwnProperty('error')) {
        displayError(response.response_comments.error)
    } else {
        displayError(response.response_comments)
    }   
}

function updateError(xhr, status, error) {
    displayError('Status=' + xhr.status + ' (' + error + ')')
}

function displayError(message) {
    $("#error").html(message);
}

function updateList(items) {
    // Removes items from todolist if they not in items
    $("li").each(function() {
        let my_id = parseInt(this.id.substring("id_item_".length))
        
        let id_in_items = false
        $(items).each(function() {
            if (this.id == my_id) id_in_items = true
        })
        if (!id_in_items) this.remove()
    })
    console.log("update list is called")

    // Adds each new todolist item to the list (only if it's not already here)
    $(items).each(function() {
        let my_id = "id_item_" + this.id
        console.log("my id is",my_id)
        if (document.getElementById(my_id) == null) {
            console.log("comment input text is ",this.comment_input_text)
            $("#comment-list_"+ this.mypost_id).prepend(
                '<p id="id_item_' + this.id + '">' +
               "comment by " + this.comment_profile + " - " +
                sanitize(this.comment_input_text) + " -- " + 
                // parse_datetime(this.comment.date_time) +
                '</p>'
            )
        }
    })
}
function updateListPosts(items,login_user_id,followlist) {   
    $(items).each(function() {
        console.log("login user id is",login_user_id)
        console.log('followlist are ',followlist)
        let post_item_id = "id_post_item_" + this.id
        console.log("post item id is",post_item_id)
        console.log("hello",post_item_id)
        // cur_user =document.getElementById("cur_user_id").innerHTML       
        // console.log("current user is :",cur_user)
        if (document.getElementById(post_item_id) == null) {
                $("#post_container").prepend(
                    '<p id="post-list_'+this.id+'"></p>'+
                    '<p id="comment-list_'+this.id+'"></p>'+
                    '<div class ="new-post">' +
                    '<label>Comment:</label>'+
                    '<input id="id_comment_input_text_'+this.id+'" type="text" name="item">'+
                    '<button onclick="addComment(this)" value="'+this.id+'">Submit</button> </div>'
                )

            // create post list
                if (this.user_id == login_user_id) {
                    $("#post-list_"+this.id).append(          
                        '<p id="id_post_item_'+this.id+'">'+                       
                        // ' <span class="details"></span>'+    
                        '<p class="post_content">Post by '+               
                        '<a href="profile" id="id_post_profile_' + this.id+'">'+ 
                        this.user_fullname+'</a> -- '+
                        sanitize(this.post_input_text)+ '--'+
                        this.datetime+'</p>'+
                        '</p>'              
                    )  
                    console.log('post user id is',this.user_id)
                    console.log('current user id is',login_user_id)
                    console.log("they are same")
                    }
                else {
                    $("#post-list_"+this.id).append(          
                        '<p id="id_post_item_'+this.id+'">'+                       
                        // ' <span class="details"></span>'+    
                        '<p class="post_content">Post by '+               
                        '<a href="otherprofile/'+ this.user_id+'" id="id_post_profile_' + this.id+'">'+ 
                        this.user_fullname+'</a> -- '+
                        sanitize(this.post_input_text)+ '--'+
                        this.datetime+'</p>'+
                        '</p>' 
                    )             
                    console.log('post user id is',this.user_id)
                    console.log('current user id is',login_user_id)
                    console.log("they are not same")
                    }                   
        }   
    })
}

function updateListComments(items,login_user_id) {
    console.log("update list comments is called")
    // Adds each new comment-list item to the list (only if it's not already here)
    $(items).each(function() {
        let my_id = "id_item_" + this.id
        console.log("my id is",my_id)

        // cur_user =document.getElementById("cur_user_id").innerHTML
        // console.log("current user is :",cur_user)

        if (document.getElementById(my_id) == null) {
            if (this.user_id == login_user_id) {                  
                // console.log("comment input text is ",this.comment_input_text)
                // create comment list
                $("#comment-list_"+ this.mypost_id).prepend(
                    '<p id="id_item_' + this.id + '">' +
                "Comment by " + 
                '<a href="profile"'+'id="id_post_profile_' + this.id+'">'+
                this.comment_profile + '</a> -- ' +
                    sanitize(this.comment_input_text) + " -- " + 
                    this.comment_date_time+
                    // '<span class="details">'+
                    // '(comment_id='+this.id+', user='+this.user+ ')'+
                    // '<span>'+              
                    '</p>'
                )
            }
            else {
                $("#comment-list_"+ this.mypost_id).prepend(
                    '<p id="id_item_' + this.id + '">' +
                "Comment by " + 
                '<a href="otherprofile/'+ this.user_id+'" id="id_post_profile_' + this.id+'">'+
                this.comment_profile + '</a> -- ' +
                    sanitize(this.comment_input_text) + " -- " + 
                    this.comment_date_time +
                    // '<span class="details">'+
                    // '(comment_id='+this.id+', user='+this.user+ ')'+
                    // '<span>'+              
                    '</p>'
                )
            }
        }     
    })
}

function updateFollowerPosts(items,login_user_id,followlist) {   
    $(items).each(function() {
        console.log("login user id is",login_user_id)
        console.log('followlist are ',followlist)
        let post_item_id = "id_post_item_" + this.id
        console.log("post item id is",post_item_id)
        console.log("hello",post_item_id)
        
        if (document.getElementById(post_item_id) == null) { 
            if (followlist.includes(this.user)) {    
                $("#follower_container").prepend(
                    '<p id="post-list_'+this.id+'"></p>'+
                    '<p id="comment-list_'+this.id+'"></p>'+
                    '<div class ="new-post">' +
                    '<label >Comment:</label>'+
                    '<input id="id_comment_input_text_'+this.id+'" type="text" name="item">'+
                    '<button onclick="addComment(this)" value="'+this.id+'">Submit</button> </div>'
                )
                
                $("#post-list_"+this.id).append(          
                    '<p id="id_post_item_'+this.id+'">'+                   
                    // ' <span class="details"></span>'+    
                    '<p class="post_content">Post by '+                                  
                    '<a href="otherprofile/'+ this.user_id+'" id="id_post_profile_' + this.id+'">'+ 
                    this.user_fullname+'</a> -- '+
                    sanitize(this.post_input_text)+ ' -- '+
                    this.datetime+'</p>'+
                    '</p>'              
                )        
            }
                                
        }   
    })
}

function updateFollowerComments(items,login_user_id) {
    console.log("update list comments is called")
    $(items).each(function() {
        let my_id = "id_item_" + this.id
        console.log("my id is",my_id)

        if (document.getElementById(my_id) == null) {
            if (this.user_id == login_user_id) {                  

                $("#comment-list_"+ this.mypost_id).prepend(
                    '<p id="id_item_' + this.id + '">' +
                "Comment by " + 
                '<a href="profile"'+'id="id_post_profile_' + this.id+'">'+
                this.comment_profile + '</a> -- ' +
                    sanitize(this.comment_input_text) + " -- " + 
                    this.comment_date_time+
                    // '<span class="details">'+
                    // '(comment_id='+this.id+', user='+this.user+ ')'+
                    // '<span>'+              
                    '</p>'
                )
            }
            else {
                $("#comment-list_"+ this.mypost_id).prepend(
                    '<p id="id_item_' + this.id + '">' +
                "Comment by " + 
                '<a href="otherprofile/'+ this.user_id+'" id="id_post_profile_' + this.id+'">'+
                this.comment_profile + '</a> -- ' +
                    sanitize(this.comment_input_text) + " -- " + 
                    this.comment_date_time +
                    '<span class="details">'+
                    '(comment_id='+this.id+', user='+this.user+ ')'+
                    '<span>'+              
                    '</p>'
                )
            }
        }     
    })
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function addComment(id) {  //从global.html中接收id值,id为post.id
    let newid= "#id_comment_input_text_" + id.value  //id.value指post.id的值
    console.log('new id is: ',newid) //new id is id_comment_input_text_{{postid}}
    let itemTextElement = $(newid)
    console.log('item text element is: ',itemTextElement)
    let itemTextValue   = itemTextElement.val() // itemTextValue is 输入的comment 
    console.log('the comment text value in addComment is:',itemTextValue)
    // Clear input box and old error message (if any)
    itemTextElement.val('')
    displayError('');

    $.ajax({
        url: "/social/add-comment/"+id.value,  //把post.id的值传给url到view
        type: "POST",
        data: "item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: updatePage2,
        error: updateError
    });
}


function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown";
}
