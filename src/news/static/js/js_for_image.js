window.onload = function() {
    // обработка чекбокса очистки
    const checkbox = document.getElementById('photo-clear_id');
    const button = document.getElementById('id_photo');
    button.addEventListener("change", (e) => addFile(e.target.files[0]));
    const span = document.getElementById('id_photo_');
    if (checkbox) {
        checkbox.addEventListener('change', () => {
          button.disabled = checkbox.checked;
          span.classList.toggle("disabled-span");
        });
    }

    // показ загружаемой фотографии
    function addFile(file) {
      let load_photo = document.getElementById('load-photo');
      if (file) {
          var fr = new FileReader();
          fr.addEventListener("load", function () {
            load_photo.src = fr.result;
            load_photo.classList.add("photo-border");
            load_photo.addEventListener('click', (e) => image_block_func(load_photo));
            load_photo.classList.remove("hidden-elem");
          }, false);
          fr.readAsDataURL(file);
      }
    }

    // показ окна с фото
    var image_block = document.getElementById('image-block-id');
    var image_block_photo = document.getElementById('image-block-photo-id');
    var body = document.body,
    html = document.documentElement;
    var height = Math.max( body.scrollHeight, body.offsetHeight,
                       html.clientHeight, html.scrollHeight, html.offsetHeight );
    image_block.style.height = height+"px";
    var images = document.querySelectorAll('.photo-border');
    for (let i = 0; i < images.length; i++) {
        images[i].addEventListener('click', function() {
            image_block_func(images[i]);
        });
    }
    function image_block_func(image) {
        image_block.classList.add("image-block");
        image_block.classList.remove("hidden-elem");
        image_block_photo.src = image.src;
        document.body.style.overflow = "hidden";
    }
}