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