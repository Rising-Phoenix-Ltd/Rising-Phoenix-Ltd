// for Gallery Uploaded Files
let fileValue = document.getElementById('file');
let fileText = document.getElementById('txt');
fileValue.addEventListener('change', ()=>{
	fileText.innerText = fileValue.value.replace(/C:\\fakepath\\/, '');;
})
