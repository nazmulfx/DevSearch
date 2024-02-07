// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});

let alertwrapper = document.querySelector('.alert') 
let alertClose = document.querySelector('.alert_close')
  
if (alertwrapper) {
  alertClose.addEventListener('click', () =>
    alertwrapper.style.display = 'none'
  )
}