const images = ["/static/img/coding-hero-first.jpg", "/static/img/coding-hero-second.jpg", "/static/img/coding-hero-third.png"];
const heroImage = document.querySelector(".image-container img")

document.addEventListener("DOMContentLoaded", () => {
    let currentImg = 0
    const changeImg = () => {
        currentImg++
        heroImage.style.opacity = 0

        if (currentImg >= images.length) {
            currentImg = 0
        }

        setTimeout(() => {
            heroImage.src = images[currentImg]
            heroImage.style.opacity = 1
        }, 1000)
        
        
    }
    const imagesInterval = setInterval(changeImg, 5000)
})




const dataUserDropdown = document.querySelector(".user-data-block")
const dataUserDropdownActivator = document.querySelector(".user-data-link-desktop")

const showDataUser = () => {
    if (dataUserDropdown.dataset.active == "disabled") {
        dataUserDropdown.style.display = "block"
        dataUserDropdownActivator.classList.add("user-data-link-active")
        dataUserDropdown.dataset.active = "active"
    } else if (dataUserDropdown.dataset.active == "active") {
        dataUserDropdown.style.display = "none"
        dataUserDropdownActivator.classList.remove("user-data-link-active")
        dataUserDropdown.dataset.active = "disabled"
    }
}


dataUserDropdownActivator.addEventListener("click", showDataUser)