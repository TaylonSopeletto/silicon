

const urlParams = new URLSearchParams(window.location.search)
const currentParam = urlParams.get('order')

const button = document.getElementById('price')


if (button) {

    button.addEventListener('click', () => {
        setFilter(button.value)
    })

    if (currentParam === 'price_asc') button.classList.add('up')
    if (currentParam === 'price_desc') button.classList.remove()
}

const setFilter = (value) => {

    const urlParams = new URLSearchParams(window.location.search)
    const currentParam = urlParams.get('order')

    if (currentParam === `${value}_asc`) {
        urlParams.set('order', `${value}_desc`)
    } else {
        urlParams.set('order', `${value}_asc`)
    }

    window.location.search = urlParams

}

















