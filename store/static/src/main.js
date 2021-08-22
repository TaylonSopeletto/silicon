import './sass/style.scss';

const urlParams = new URLSearchParams(window.location.search)
const currentParam = urlParams.get('order')

const button = document.getElementById('price')

if(button){
    button.addEventListener('click', () => {
    
        setFilter(button.value)
    })
    
    if(currentParam === 'price_asc') button.classList.add('up')
    if(currentParam === 'price_desc') button.classList.remove()
}

const setFilter = (value) => {
    const urlParams = new URLSearchParams(window.location.search)
    const currentParam = urlParams.get('order')

    if(currentParam === `${value}_asc`){
        urlParams.set('order', `${value}_desc`)
    }else{
        urlParams.set('order', `${value}_asc`)
    }

    window.location.search = urlParams
    
}

/* add product to card */

const rawProduct = JSON.parse(document.getElementById('product_data').textContent);
const jsonProduct = JSON.parse(rawProduct)

const addProductButton = document.getElementById('addProductButton')
const removeProductButton = document.getElementById('removeProductButton')

addProductButton.addEventListener('click', () => {
   window.location.href = `/add_product?id=${jsonProduct[0].pk}`
})

removeProductButton.addEventListener('click', () => {
    window.location.href = `/remove_product?id=${jsonProduct[0].pk}`
})














