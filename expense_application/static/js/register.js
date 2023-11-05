const usernameField = document.querySelector('#userNameField');
const feedbackArea = document.querySelector('.invalid-feedback');
const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.invalid-emailfeedback');
const passwordField = document.querySelector('#passwordField');
const showPassword = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn');

const toggleShowPassword = () => {
    if(showPassword.textContent === 'Show Password'){
        showPassword.textContent = 'Hide Password'
        passwordField.setAttribute('type', 'text')
    }else{
        showPassword.textContent = 'Show Password'
        passwordField.setAttribute('type', 'password')
    }
}

showPassword.addEventListener('click', toggleShowPassword)

emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;
    emailField.classList.remove('is-invalid')
    emailFeedbackArea.style.display='none'
    emailFeedbackArea.innerHTML = `<p>${''}</p>`
    
    if(emailValue){
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailValue }),
            method: "POST",
          })
            .then((res) => res.json())
            .then((data) => {
                if(data.email_error){
                    submitBtn.disabled = true;
                    emailField.classList.add('is-invalid')
                    emailFeedbackArea.style.display='block'
                    emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`
            }else{
                submitBtn.removeAttribute('disabled')
            }
        })
    }
})

usernameField.addEventListener('keyup', (e) => {
    const userNameValue = e.target.value;
    usernameField.classList.remove('is-invalid')
    feedbackArea.style.display='none'
    feedbackArea.innerHTML = `<p>${''}</p>`
    
    if(userNameValue){
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: userNameValue }),
            method: "POST",
          })
            .then((res) => res.json())
            .then((data) => {
                if(data.username_error){
                    submitBtn.disabled = true;
                    usernameField.classList.add('is-invalid')
                    feedbackArea.style.display='block'
                    feedbackArea.innerHTML = `<p>${data.username_error}</p>`
            }else{
                submitBtn.removeAttribute('disabled')
            }
        })
    }
})