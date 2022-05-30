// console.log('USER:', user) // from base/base.html

// using 'update-cart' class to perform the action 'add to cart'
let updateBtns = document.getElementsByClassName('update-cart')

for(let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        let productId = this.dataset.product
        let action = this.dataset.action
        // console.log('productId:', productId, 'action:', action)

        if(user === 'AnonymousUser') {
            alert('To add items into cart. Please Login/Register First')
        } else {
        updateUserOrder(productId, action)
        }
    })
}


// API for updating items to the cart
function updateUserOrder(productId, action) {
    // console.log('User logged in. sending data....')

    let url = '/update_item/' // this is where we want to send the data
    
    // fetch(url where we want to send the data, what kind of data we going to send to backend)
    fetch(url, {
        method: 'POST',  
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    // response after we send data to backend (view) - returning promise
    .then((response) => {
        return response.json() // HttpResponse from views.py
    })
    .then((data) => {
        // console.log('Data:', data)
        location.reload()
    });
}


// To perform the action when someone clicks 'view' button on item
let viewBtns = document.getElementsByClassName('expand-view')

