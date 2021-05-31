const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const imageForm = document.getElementById('image-form')
const confirmBtn = document.getElementById('confirm-btn')
const input = document.getElementById('id_file')
const user_name = document.getElementById('user_name').innerHTML;

// var desc = '';

const csrf = document.getElementsByName('csrfmiddlewaretoken')

        input.addEventListener('change', ()=>{
            alertBox.innerHTML = ""
            confirmBtn.classList.remove('not-visible')
            const img_data = input.files[0]
            const url = URL.createObjectURL(img_data)

            imageBox.innerHTML = `<img src="${url}" id="image" width="700px" height="700px">`
            var $image = $('#image')
            // console.log($image)

            $image.cropper({
                aspectRatio: 9 / 9,
                crop: function(event) {
                    // console.log(event.detail.x);
                    // console.log(event.detail.y);
                    // console.log(event.detail.width);
                    // console.log(event.detail.height);
                    // console.log(event.detail.rotate);
                    // console.log(event.detail.scaleX);
                    // console.log(event.detail.scaleY);
                }
            });
            
            var cropper = $image.data('cropper');

            confirmBtn.addEventListener('click', ()=>{
                cropper.getCroppedCanvas().toBlob((blob) => {
                    // console.log('confirmed')
                    const fd = new FormData();
                    fd.append('csrfmiddlewaretoken', csrf[0].value)
                    fd.append('profilePicture', blob, 'my-image.jpg');

                    $.ajax({
                        type:'POST',
                        url: 'profilePicture',
                        enctype: 'multipart/form-data',
                        data: fd,
                        success: function(response){
                            window.location.href = `/profile/${user_name}`;
                        },
                        error: function(error){
                            // console.log('error', error)
                            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                                                        Ups...something went wrong
                                                    </div>`
                        },
                            cache: false,
                            contentType: false,
                            processData: false,
                        })
                    })
                })






        })    