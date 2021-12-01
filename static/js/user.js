let account = document.querySelector('.account');
let setting = document.querySelector('.settingContent');



// Account Page

let profilePic = document.querySelector('.profilePic');

if (account) {
  profilePic.addEventListener('click', () => {
    OverlayDisplayItem(profilePic);
  })
}


// Setting Page

let settingNav = document.querySelectorAll('.settingNav a');

let settingContent = document.querySelectorAll('.settingContent');

let uploadPic = document.getElementById('uploadedPic');
let inputPic = document.getElementById('uploadPic');
let btnDelete = document.getElementById('btnDelete');
let file;


if (setting) {
 
  // Profile uploaded image from user
  inputPic.addEventListener("change", function() {

    file = this.files[0];
    showFile();
  });



  btnDelete.addEventListener('click', () => {
    let Overlay = document.createElement('div');
    let item = document.createElement('div');

    Overlay.classList = 'overlay';
    item.classList = 'deleteConfirm';

    document.body.appendChild(Overlay);
    Overlay.appendChild(item);

    let itemHTML = `
      <i class="fas fa-exclamation"></i>
      <i class="fas fa-circle-xmark cancel"></i>
	    <h2>Confirm</h2>
	    <p>it will permanently delete this, are you u want to remove this?</p>
	  
	    <div class="utility">
	      <a class="btn" href="{{ url_for('delete') }}">Delete</a>
	    </div>
    `;



    item.innerHTML = itemHTML;

    let btnHide = document.querySelector('i + .cancel');

    if (item) {
      btnHide.addEventListener('click', () => {
        Overlay.remove();
      })

    }


    Overlay.addEventListener('click', () => {
      if (event.target === Overlay) {
        Overlay.remove();
      }
    });

  })
}






// function

function settingFunction(itemShow, itemHide, btnShow, btnHide) {

  for (let i = 0; i < itemHide.length; i++) {
    btnHide[i].classList.remove('active');
    btnShow.classList.add('active');

    itemHide[i].style.display = 'none';
    itemShow.style.display = 'flex';

  }
}


// ShowPic Function

function showFile() {
  let fileType = file.type;
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"];

  if (validExtensions.includes(fileType)) {

    let fileReader = new FileReader();

    fileReader.onload = () => {
      let fileURL = fileReader.result;

      uploadPic.setAttribute('src', `${fileURL}`);
    }
    
    fileReader.readAsDataURL(file);
  }
  else {
    uploadPic.setAttribute('src', '/static/img/user.svg');
  }
  
}