let play = document.getElementsByClassName('iPlayer');
let list = document.querySelectorAll('#pic .list')
let mainBox = document.querySelector('#pic')


for (let i = 0; i < list.length; i++) {
  list[i].addEventListener('click', ()=>{
    OverlayDisplayItem(play[i]);
  })
}



let galleryNav = document.querySelectorAll('.galleryNav a');

let video = document.getElementById('vid');
let image = document.getElementById('pic');


galleryNav[1].addEventListener('click', ()=>{
  image.style.display = 'grid';
  video.style.display = 'none';
  
  galleryNav[1].classList.add('active');
  galleryNav[0].classList.remove('active');
})

galleryNav[0].addEventListener('click', ()=>{
  video.style.display = 'grid';
  image.style.display = 'none';
  
  galleryNav[0].classList.add('active');
  galleryNav[1].classList.remove('active');
})
