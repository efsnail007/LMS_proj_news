window.onload = function() {
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
    function addFile(file) {
      let load_photo = document.getElementById('load-photo');
      if (file) {
          var fr = new FileReader();
          fr.addEventListener("load", function () {
            load_photo.src = fr.result;
            load_photo.classList.add("photo-border-color");
            load_photo.classList.remove("hidden-elem");
          }, false);
          fr.readAsDataURL(file);
      }
    }
}