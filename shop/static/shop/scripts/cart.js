const addToCartBtn = document.getElementsByClassName('update-cart');
const viewProductBtn = document.getElementsByClassName('view-product');
const removeProductBtn = document.getElementsByClassName('remove-product');

for (let i = 0; i<addToCartBtn.length; i++){
    addToCartBtn[i].addEventListener('click', ()=>{
        let productID = addToCartBtn[i].dataset.product_id;
        let action = addToCartBtn[i].dataset.action;
        console.log(productID, action)
        
        if(user === 'AnonymousUser'){
            updateNotLoggedInUserOrder(productID, action)
        }else{
            
            updateUserOrder(productID, action)
        }
    })
}

for (let i=0; i < viewProductBtn.length; i++){
    viewProductBtn[i].addEventListener('click', ()=>{
        const productID = viewProductBtn[i].dataset.product_id
        const action = viewProductBtn[i].dataset.action
        if (action === 'view'){
            window.location.href='/shop/'+ productID + '/'
        }
    })
}

for (let i = 0; i<removeProductBtn.length; i++){
    removeProductBtn[i].addEventListener('click', ()=>{
        let productID = removeProductBtn[i].dataset.product_id;
        let action = removeProductBtn[i].dataset.action;
        console.log(productID, action)
        
        if(user === 'AnonymousUser'){
            updateNotLoggedInUserOrder(productID, action)
        }else{
            
            updateUserOrder(productID, action)
        }
    })
}

const updateNotLoggedInUserOrder = (productID, action)=>{
    console.log("Unanuthorised User")
    console.log(productID + " " + action)
    if(action == 'add'){
        if(cart[productID] == undefined){
            cart[productID] = {'quantity': 1}

        }else{
            cart[productID]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productID]['quantity'] -= 1

        if (cart[productID]['quantity'] <=0){
            console.log("remove item")
            delete cart[productID]
        }
    }
    console.log(cart)
    document.cookie= 'cart='+ JSON.stringify(cart) + ';domian=;path=/'
    location.reload()
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