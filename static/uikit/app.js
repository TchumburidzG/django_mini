// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});

let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

if (alertWrapper) {
  alertClose.addEventListener('click', () => alertWrapper.style.display = 'none')
}
// იდეაშ ამ ზედა 4 ხაზს HTML-ის ერორ მესიჯებზე გათიშვის x  რომ არის ეგ უნდა აემუშავებია მარა ჩემი ფეხები, არ მუშაობს.
// ამ ეტაპისთვის ეს ფაილი დალინკულია base.html-ში ბოლოში.