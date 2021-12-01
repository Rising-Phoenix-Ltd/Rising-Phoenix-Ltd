// CLICK SOUND EFFECT FOR BUTTTONS
const btn = document.getElementsByClassName('btn');
const sound = document.getElementById('sound');

for (i = 0; i < btn.length; i++) {
  btn[i].addEventListener('click', () => {
    sound.play();
  })
}

// this is for  hamburger Menubar
const hamburger = {
  menu: document.querySelector('.menuBar'),
  nav: document.querySelector('.navHide'),
  icon: document.getElementById('menu')
}

hamburger.menu.addEventListener('click', () => {
  hamburger.icon.classList.toggle('fa-xmark');
  hamburger.nav.classList.toggle('navShow');
})


const userbtn = {
  btnMobile: document.querySelector('#mobile'),
  btnDesktop: document.querySelector('#desktop')
}

// this is userbtn for desktop and mobile

let mediaQuery = window.matchMedia('(max-width: 868px)');

mediaQuery.addListener(mediaQuery);

if (mediaQuery.matches) {
  userbtn.btnDesktop.remove();
  userbtn.btnDesktop.removeAttribute('class');
}
else {
  userbtn.btnMobile.remove();
  userbtn.btnMobile.removeAttribute('class');
}

// this block is for popup window
const logpop = {
  form: document.getElementById('loginForm'),
  btnShow: document.querySelector('.user'),
  btnHide: document.getElementById('hideLog'),
}
const userpop = {
  menu: document.querySelector('.user-popup'),
}

let formBox = document.querySelector('.nopopup');

if (formBox) {
  logpop.btnShow.classList = 'user';
  
  if (window.location.href == '/login'){
    logpop.btnShow.addEventListener('click', ()=>{
      window.location.href = '/register'
    })
  }
  else {
    logpop.btnShow.addEventListener('click', ()=>{
      window.location.href = '/login'
    })
  }
}



let showLog = logpop.btnShow.classList.contains('showLog');
let showAcc = logpop.btnShow.classList.contains('showAcc');


if (showLog) {

  let show = `
  transform: translateX(-50%) scale(1); opacity: 1;`
  let hide = `
  transform: translateX(-50%) scale(0); opacity: 0;`


  // when clicked on loginbtn , Open popup
  logpop.btnShow.addEventListener('click', () => {
    logpop.form.style.cssText = show;
  })

  //when clicked on Xmark icons form, Close it
  logpop.btnHide.addEventListener('click', () => {
    logpop.form.style.cssText = hide;
  })
  // When the user clicks anywhere outside of the Form, close it
  window.addEventListener('click', () => {
    if (event.target == logpop.form) {
      logpop.form.style.cssText = hide;
    }
  })
}
else if (showAcc) {
  logpop.btnShow.addEventListener('click', () => {
    userpop.menu.classList.toggle('show');
  })

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      userpop.menu.classList.remove('show');
    }
  })

  hamburger.menu.addEventListener('click', () => {
    userpop.menu.classList.remove('show');
  })
}


let form = document.querySelectorAll('form');

if (form) {
  for (let i = 0; i < form.length; i++) {
    form[i].addEventListener('submit', () => {
      let loading = form[i].querySelector('[type="submit"]');
      loading.remove();


      let newLoading = document.createElement('div');
      newLoading.setAttribute('class', 'fas fa-circle-notch fa-spin')
      newLoading.id = 'btnloading';

      form[i].appendChild(newLoading);

    })
  }
}

// FUNCTIONS



function OverlayDisplayItem(item) {
  let source = item.src;
  let overlay = document.createElement('div');
  let img = document.createElement('img');

  document.body.appendChild(overlay);
  overlay.appendChild(img);

  img.src = source;
  img.classList.add('displayItem');
  overlay.classList.add('overlay');

  overlay.addEventListener('click', () => {
    overlay.remove();
  })
}