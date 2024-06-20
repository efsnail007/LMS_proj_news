window.onload = function() {
    // обработка чекбокса очистки
    const checkbox = document.getElementById('photo-clear_id');
    const button = document.getElementById('id_photo');
    button.addEventListener("change", (e) => addFile(e.target.files));
    const span = document.getElementById('id_photo_');
    if (checkbox) {
        checkbox.addEventListener('change', () => {
          button.disabled = checkbox.checked;
          span.classList.toggle("disabled-span");
        });
    }

    // показ загружаемой фотографии и видео
    function addFile(files) {
      let loaded_container = document.querySelector(".loaded-container");
      for (let i = 0; i < files.length; i++) {
          if (files[i]) {
              let column = document.createElement('div');
              column.classList.add("mt-4");
              let del = document.createElement('button');
              del.type = "button";
              del.classList.add("btn");
              del.classList.add("btn-danger");
              del.textContent = "Удалить";
              del.style.float = "right";
              del.classList.add("mb-2");
              column.classList.add("col");
              if (files[i].type.startsWith('video/')) {
                let video = document.createElement('video');
                video.controls = true;
                let url = URL.createObjectURL(files[i]);
                video.src = url;
                video.muted = true;
                document.body.appendChild(video);
                video.play();
                video.loop = "loop";
                video.classList.add("video-border");
                video.classList.add("img-thumbnail");
                video.classList.add("img-fluid");
                column.appendChild(del);
                column.appendChild(video);
              } else {
                  let fr = new FileReader();
                  fr.addEventListener("load", function () {
                    let load_photo = document.createElement('img');
                    load_photo.src = fr.result;
                    load_photo.classList.add("photo-border");
                    load_photo.classList.add("img-thumbnail");
                    load_photo.classList.add("img-fluid");
                    load_photo.classList.add("rounded");
                    load_photo.classList.add("d-block");
                    load_photo.addEventListener('click', (e) => image_block_func(load_photo));
                    column.appendChild(del);
                    column.appendChild(load_photo);
                  }, false);
                  fr.readAsDataURL(files[i]);
              }
              loaded_container.appendChild(column);
              del.addEventListener("click", () => del_media(files, files[i], column));
          }
        }
    }

    // обработка удаления из добавленных фото и видео
    function del_media(files, del_file, column) {
      let input = document.getElementById('id_photo');
      let dataTransfer = new DataTransfer()
      for(const file of input.files)
        if (file != del_file)
            dataTransfer.items.add(file);
      input.files = dataTransfer.files;
      column.remove();
    }

    // показ окна с фото
    var image_block = document.getElementById('image-block-id');
    var image_block_photo = document.getElementById('image-block-photo-id');
    var images = document.querySelectorAll('.photo-border');
    for (let i = 0; i < images.length; i++) {
        images[i].addEventListener('click', function() {
            image_block_func(images[i]);
        });
    }
    function image_block_func(image) {
        image_block.style.top = window.pageYOffset + "px";
        image_block.classList.add("image-block");
        image_block.classList.remove("hidden-elem");
        image_block_photo.classList.remove("hidden-elem");
        image_block_photo.src = image.src;
        document.body.style.overflow = "hidden";
    }
    // закрытие окна с фото
    image_block.addEventListener("click", function(e) {
        if (e.target.id != 'image-block-photo-id') {
            image_block.classList.add("hidden-elem");
            image_block_photo.classList.add("hidden-elem");
            image_block.classList.remove("image-block");
            document.body.style.overflow = "auto";
        }
    });
}