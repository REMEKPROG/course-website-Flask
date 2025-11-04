const hamburgerMenuIcon = document.querySelector(".nav-container .hamburger-menu-icon")
const sideMenu = document.querySelector(".nav-container .side-nav")

const dropdownElementActivator = document.querySelector(".left-nav-side-elements .activator")
const dropdownSideMenu = document.querySelector(".menu-side-dropdown-element .menu-side-dropdown")



const showSideDropdownMenu = () => {
    if (dropdownSideMenu.dataset.active == "disable") {
        dropdownSideMenu.style.display = "block"
        dropdownSideMenu.dataset.active = "active"
    } else if (dropdownSideMenu.dataset.active == "active"){
        dropdownSideMenu.style.display = "none"
        dropdownSideMenu.dataset.active = "disable"
    }
}


const showSideMenu = () => {
    if (sideMenu.dataset.active == "disable") {
        sideMenu.style.width = "50%"
        sideMenu.dataset.active = "active"
    } else if (sideMenu.dataset.active == "active"){
        sideMenu.style.width = "0"
        sideMenu.dataset.active = "disable"
    }
}

hamburgerMenuIcon.addEventListener("click", showSideMenu)
dropdownElementActivator.addEventListener("click", showSideDropdownMenu)