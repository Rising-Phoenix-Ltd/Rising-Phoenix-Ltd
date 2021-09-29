// CLICK SOUND EFFECT FOR BUTTTONS
let btn = document.getElementsByClassName('btn');
let sound = document.getElementById('sound');

for (i = 0; i < btn.length; i++) {
  btn[i].addEventListener('click', () => {
    sound.play();
    sound.playbackRate = 1;
  });
}

// this is for password validation
{
  let password = document.getElementById("password");
  let confirm_password = document.getElementById("confirm_password");

  function validatePassword() {
    if (password.value != confirm_password.value) {
      confirm_password.setCustomValidity("Please enter same password");
    }
    else {
      confirm_password.setCustomValidity('');
    }
  }
}

// this is for  hamburger Menubar
let hamburger = {
  menu : document.querySelector('.menuBar'),
  nav : document.querySelector('.navHide'),
  menuIcon : document.getElementById('icon')
}
hamburger.menu.addEventListener('click', ()=>{
  hamburger.menuIcon.classList.toggle('fa-xmark');
  hamburger.nav.classList.toggle('navShow');
})


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
// when user scroll outside of form, close it
window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    popUp.form.style.cssText = `
    transform: translateX(-50%) scale(0);
    opacity: 0;`
  }
})

let list = document.querySelectorAll('.mainBox .list ');

for (let i = 0; i < list.length; i++) {
	list[i].addEventListener('click', ()=>{
		list[i].classList.toggle('openPlayer');
	})
}