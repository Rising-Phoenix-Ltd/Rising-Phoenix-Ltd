// this is for password validation
{
  let password = document.getElementById("password");
  let confirm_password = document.getElementById("confirm_password");

  function validatePassword() {
    if (password.value != confirm_password.value) {
      confirm_password.setCustomValidity("Passwords  not matched. try Again");
    }
    else {
      confirm_password.setCustomValidity('');
    }
  }
}

// this block is for popup window
let popUp = {
  showBtn: document.getElementById('showbtn'),
  form: document.getElementById('form'),
  hideBtn: document.getElementById('hidebtn'),
}

// when clicked on loginbtn , Open popup
popUp.showBtn.addEventListener('click', () => {
  popUp.form.style.cssText = `
  transform: translateX(-50%) scale(1);
  opacity: 1;`
})

//when clicked on Xmark icons form, Close it
popUp.hideBtn.addEventListener('click', () => {
  popUp.form.style.cssText = `
  transform: translateX(-50%) scale(0);
  opacity: 0;`
})
// When the user clicks anywhere outside of the Form, close it
window.addEventListener('click', () => {
  if (event.target == form) {
    popUp.form.style.cssText = `
      transform: translateX(-50%) scale(0);
      opacity: 0;`
  }
})