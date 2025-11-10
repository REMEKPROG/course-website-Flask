const loginInput = document.getElementById("login")
const passwordInput = document.getElementById("password")
const email = document.getElementById("email")
const age = document.getElementById("age")

const inputsValidateList = [loginInput, passwordInput, email, age]
const loginRegex = /^[0-9A-Za-z]{4,16}$/
const passwordRegex = /[A-Za-z0-9@#$%^&+=]{8,}/
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

const loginWarningText = document.getElementById("login-warning")
const passwordWarningText = document.getElementById("password-warning")
const emailWarningText = document.getElementById("email-warning")
const ageWarningText = document.getElementById("age-warning")

const submitButton = document.querySelector(".submit-button button")

let flag = false
const dataFlags = {
    "loginFlag" : false,
    "passwordFlag" : false,
    "emailFlag" : false,
    "ageFlag" : false
}
const validateInputData = (e) => {
    if (e.target.id == "login") {
        if (!loginRegex.test(e.target.value)) {
            loginWarningText.style.display = "block"
            dataFlags.loginFlag = false
        } else {
            loginWarningText.style.display = "none"
            dataFlags.loginFlag = true
        }
    }
    if (e.target.id == "password") {
        if (!passwordRegex.test(e.target.value)) {
            passwordWarningText.style.display = "block"
            dataFlags.passwordFlag = false
        } else {
            passwordWarningText.style.display = "none"
            dataFlags.passwordFlag = true
        }
    }
    if (e.target.id == "email") {
        if (!emailRegex.test(e.target.value)) {
            emailWarningText.style.display = "block"
            dataFlags.emailFlag = false
        } else {
            emailWarningText.style.display = "none"
            dataFlags.emailFlag = true
        }
    }
    if (e.target.id == "age") {
        if ((Number(e.target.value) < 13 || Number(e.target.value) > 100)) {
            ageWarningText.style.display = "block"
            dataFlags.ageFlag = false
        } else {
            ageWarningText.style.display = "none"
            dataFlags.ageFlag = true
        }
    }

    function releaseButton() {
        let i = 0;
        for (const key in dataFlags) {
            if (dataFlags[key]) {
                i++
            }
        }

        if (i == Object.getOwnPropertyNames(dataFlags).length) {
            flag = true 
        } else {
            flag = false
        }
    
    }
    releaseButton()

    if (!flag) {
        submitButton.disabled = true
    } else {
        submitButton.disabled = false
    }
}

inputsValidateList.forEach((input) => {
    input.addEventListener("input", validateInputData)
})