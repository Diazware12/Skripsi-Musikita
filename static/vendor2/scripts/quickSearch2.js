const url = window.location.href
const searchForm = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultBox = document.getElementById('result-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendSearchData = (product) =>{
    $.ajax({
        type: 'POST',
        url:'/search/',
        data:{
            'csrfmiddlewaretoken': csrf[0].value,
            'product':product
        },
        success: (res) => {
            const data = res.data
            if(Array.isArray(data)){
                resultBox.innerHTML = ""
                data.forEach(product=>{
                    resultBox.innerHTML += `
                        <a href="/product/${product.productBrand}/${product.productName}/" class"item" style="text-decoration: none;color:black;">
                            <div class="row mt-2 mb-2">
                                <div class="col-2">
                                    <img src="${product.productIMG}" alt="Admin" width="90">
                                </div>
                                <div class="col-10">
                                    <h6>${product.productName}</h6>
                                    <p>${product.productBrand}</p>
                                </div>
                            </div>
                        </a>
                    `
                })
            }else{
                if (searchInput.value.length > 0){
                    resultBox.innerHTML = `<b>${data}</b>`
                } else {
                    resultBox.classList.add('not-visible')
                }
            }
        },
        error: (err) => {
            console.log(err)
        }
    })
}

searchInput.addEventListener('keyup', e=>{

    if (resultBox.classList.contains('not-visible')){
        resultBox.classList.remove('not-visible')
    }

    sendSearchData(e.target.value)
})