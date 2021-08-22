import './sass/style.scss';

const removeButton = document.getElementById('removeProductButton')

removeButton.addEventListener('click', () => {
    removeProduct(removeButton.value)
})

const removeProduct = value => {
    window.location.href = `/remove_product?id=${value}`
}
