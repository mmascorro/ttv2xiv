
//from bulma navbar example 
const navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

navbarBurgers.forEach( el => {
  el.addEventListener('click', () => {
    const targetId = el.dataset.target;
    const target = document.getElementById(targetId);
    el.classList.toggle('is-active');
    target.classList.toggle('is-active');
  });
});


document.getElementById('contact-button').addEventListener('click', e => {
  const addr = "e`m`.`n`o`t`o`r`p`@`v`i`x`2`v`t`t" .split('`').reverse().join('');
  console.log(addr)
  window.location.href = `mailto:${addr}`
})
