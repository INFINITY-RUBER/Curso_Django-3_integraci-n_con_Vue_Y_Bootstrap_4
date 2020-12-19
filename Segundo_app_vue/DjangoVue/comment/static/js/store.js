
function setSizeShoppingCart(){
    fetch("/cart_size")
    .then(res => res.json())
    .then(data => {
        count = document.querySelector("#shoppingCart .count")
        if(data.size > 0){
            count.textContent=data.size
            count.classList.remove("d-none")
            // console.log("hola mundo")

        }
    })

    setTimeout(setSizeShoppingCart, 5000);
}

setSizeShoppingCart()

function changeQuantityEvent(){

    
    changeQuantityMinus = document.querySelector(".changeQuantityMinus")    
    
    if(changeQuantityMinus){
        changeQuantityMinus.addEventListener('click',() => {
            id = changeQuantityMinus.getAttribute('data-id')    
            e_quantity = document.querySelector("#e_quantity_"+id);
            res = parseInt(e_quantity.value) - 1
            if(res < 1){
                res = 1
            }
            console.log("hola" +id+" " + res)
            e_quantity.value = res
        })
    }


    changeQuantityPlus = document.querySelector(".changeQuantityPlus")    
    
    
    if(changeQuantityPlus){
        changeQuantityPlus.addEventListener('click',() => {
            id = changeQuantityPlus.getAttribute('data-id')    
            e_quantity = document.querySelector("#e_quantity_"+id);
            res = parseInt(e_quantity.value) + 1
            console.log("hola" +id+" " + res)
            e_quantity.value = res
        })
    }
}

changeQuantityEvent()