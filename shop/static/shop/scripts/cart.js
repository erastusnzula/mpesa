const addToCartBtn = document.getElementsByClassName('update-cart');
const viewProductBtn = document.getElementsByClassName('view-product');
const removeProductBtn = document.getElementsByClassName('remove-product');

for (let i = 0; i<addToCartBtn.length; i++){
    addToCartBtn[i].addEventListener('click', ()=>{
        let productID = addToCartBtn[i].dataset.product_id;
        let action = addToCartBtn[i].dataset.action;
        console.log(productID, action)
        
        if(user === 'AnonymousUser'){
            console.log("Not logged in")
        }else{
            
            updateUserOrder(productID, action)
        }
    })
}

for (let i = 0; i<removeProductBtn.length; i++){
    removeProductBtn[i].addEventListener('click', ()=>{
        let productID = removeProductBtn[i].dataset.product_id;
        let action = removeProductBtn[i].dataset.action;
        console.log(productID, action)
        
        if(user === 'AnonymousUser'){
            console.log("Not logged in")
        }else{
            
            updateUserOrder(productID, action)
        }
    })
}

const updateUserOrder = (productID, action)=>{
    console.log(`Logged in as ${user}`)
    const url = '/shop/add_to_cart/'
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({'product_id': productID, 'action': action}),
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        location.reload()
    })
    
}