const inputFile = document.querySelector(".img-container .image-input")

const changeImage = (e) => {
  const file = inputFile.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function(event) {
      const label = document.querySelector(".img-container .image-label");
      label.style.backgroundImage = `url(${event.target.result})`;
    };

    reader.readAsDataURL(file); // Konwertuje plik do base64
  }
};

inputFile.addEventListener("change", changeImage)