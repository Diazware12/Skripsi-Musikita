const ddown = document.getElementById('categoryddl')
const ddownInput = document.getElementById('category')

const ddownSub = document.getElementById('subcategoryddl')
const ddownInputSub = document.getElementById('subcategory')

const subCatText = document.getElementById('subCategoryText')

const pName = document.getElementById('productName').innerHTML;
const brand = document.getElementById('brand').innerHTML;


$.ajax({
    type: 'GET',
    url: `${pName}/cat-json/`,
    success: function(response){
        console.log(response);
        const catData = response.data
        catData.map(item=>{
            const option = document.createElement('option')
            option.textContent = item.categoryName
            option.setAttribute('class','item')
            option.setAttribute('data-value',item.categoryId)
            ddown.appendChild(option)
        })
    },  
    error: function (error) {
        console.log(error);
    }
})

ddownInput.addEventListener('change', e=>{
    console.log(e.target.value)
    const selectedCategory = e.target.value

    ddownSub.innerHTML = ""
    subCatText.textContent = "---------"
    subCatText.classList.add("default")

    $.ajax({
        type: 'GET',
        url: `${pName}/subCat-json/${selectedCategory}`,
        success: function(response){
            console.log(response)
            const subCategoryData = response.data
            subCategoryData.map(item=>{
                const option = document.createElement('option')
                option.textContent = item.subCategoryName
                option.setAttribute('class','item')
                option.setAttribute('data-value',item.subCategoryId)
                ddownSub.appendChild(option)
            })
        },
            error: function (error) {
        console.log(error);
    }
    })

})